import asyncio
import os
import re
from collections import deque

import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp

from locales import t, get_lang, set_lang, LOCALES

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# --- yt-dlp / ffmpeg config ---------------------------------------------

YTDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTS)

SUPPORTED_AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".opus", ".webm")
SPOTIFY_TRACK_RE = re.compile(r"open\.spotify\.com/track/([a-zA-Z0-9]+)")

# --- Optional Spotify client (only needed for Spotify links) -----------

spotify_client = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    from spotipy import Spotify
    from spotipy.oauth2 import SpotifyClientCredentials

    spotify_client = Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
        )
    )


class Song:
    def __init__(self, source_url, title, webpage_url, requester, direct=False):
        self.source_url = source_url
        self.title = title
        self.webpage_url = webpage_url
        self.requester = requester
        # direct=True means source_url is already a playable stream/file URL
        # (e.g. a Discord attachment) and should NOT be re-resolved by yt-dlp.
        self.direct = direct


async def fetch_song_from_youtube(query: str, requester) -> Song:
    """Resolve a search query or a YouTube (or other yt-dlp supported) URL."""
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        None, lambda: ytdl.extract_info(query, download=False)
    )
    if "entries" in data:  # search result list
        data = data["entries"][0]
    return Song(
        source_url=data["url"],
        title=data.get("title", "Unknown title"),
        webpage_url=data.get("webpage_url", query),
        requester=requester,
    )


async def fetch_song_from_spotify(url: str, requester, guild_id: int) -> Song:
    """Resolve a Spotify track link by pulling its title/artist, then
    searching that on YouTube (Spotify's API doesn't provide raw audio)."""
    if spotify_client is None:
        raise RuntimeError(t(guild_id, "spotify_not_configured"))

    match = SPOTIFY_TRACK_RE.search(url)
    if not match:
        raise RuntimeError(t(guild_id, "spotify_unsupported_link"))

    track_id = match.group(1)
    loop = asyncio.get_event_loop()
    track = await loop.run_in_executor(None, lambda: spotify_client.track(track_id))
    artist = track["artists"][0]["name"]
    title = track["name"]
    return await fetch_song_from_youtube(f"{artist} - {title} audio", requester)


def song_from_attachment(attachment: discord.Attachment, requester) -> Song:
    return Song(
        source_url=attachment.url,
        title=attachment.filename,
        webpage_url=attachment.url,
        requester=requester,
        direct=True,
    )


# --- Per-guild music state ------------------------------------------------

class GuildMusicState:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.queue: deque[Song] = deque()
        self.voice_client: discord.VoiceClient | None = None
        self.current: Song | None = None
        self.volume = 0.5

    def play_next(self, error=None):
        if error:
            print(f"Player error: {error}")

        if not self.queue:
            self.current = None
            return

        self.current = self.queue.popleft()
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(self.current.source_url, **FFMPEG_OPTS),
            volume=self.volume,
        )
        self.voice_client.play(source, after=self.play_next)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.states: dict[int, GuildMusicState] = {}

    def get_state(self, guild_id) -> GuildMusicState:
        if guild_id not in self.states:
            self.states[guild_id] = GuildMusicState(self.bot, guild_id)
        return self.states[guild_id]

    async def ensure_voice(self, ctx) -> GuildMusicState | None:
        state = self.get_state(ctx.guild.id)

        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send(t(ctx.guild.id, "need_voice_channel"))
            return None

        if state.voice_client is None or not state.voice_client.is_connected():
            state.voice_client = await ctx.author.voice.channel.connect()
        elif state.voice_client.channel != ctx.author.voice.channel:
            await state.voice_client.move_to(ctx.author.voice.channel)

        return state

    @commands.hybrid_command(name="play", aliases=["p"])
    async def play(self, ctx, *, query: str = None):
        """Play from a song name, YouTube link, Spotify link, or attached audio file."""
        gid = ctx.guild.id
        state = await self.ensure_voice(ctx)
        if state is None:
            return

        attachments = ctx.message.attachments if ctx.message else []
        audio_attachment = next(
            (a for a in attachments if a.filename.lower().endswith(SUPPORTED_AUDIO_EXTS)),
            None,
        )

        if audio_attachment is None and attachments and query is None:
            exts = ", ".join(SUPPORTED_AUDIO_EXTS)
            await ctx.send(t(gid, "unsupported_attachment", exts=exts))
            return

        if audio_attachment is None and query is None:
            await ctx.send(t(gid, "no_query_or_file"))
            return

        async with ctx.typing():
            try:
                if audio_attachment is not None:
                    song = song_from_attachment(audio_attachment, ctx.author)
                elif "open.spotify.com" in query:
                    await ctx.send(t(gid, "resolving_spotify"))
                    song = await fetch_song_from_spotify(query, ctx.author, gid)
                else:
                    # Works for plain search terms AND direct YouTube (or
                    # other yt-dlp supported) links.
                    song = await fetch_song_from_youtube(query, ctx.author)
            except Exception as e:
                await ctx.send(t(gid, "song_not_found", error=str(e)))
                return

            state.queue.append(song)
            await ctx.send(t(gid, "added_to_queue", title=song.title))

        if state.voice_client and not state.voice_client.is_playing() and state.current is None:
            state.play_next()

    @commands.hybrid_command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        """Skip the current song."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        if state.voice_client and state.voice_client.is_playing():
            state.voice_client.stop()  # triggers play_next via 'after' callback
            await ctx.send(t(gid, "skipped"))
        else:
            await ctx.send(t(gid, "nothing_playing"))

    @commands.hybrid_command(name="pause")
    async def pause(self, ctx):
        """Pause playback."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        if state.voice_client and state.voice_client.is_playing():
            state.voice_client.pause()
            await ctx.send(t(gid, "paused"))

    @commands.hybrid_command(name="resume")
    async def resume(self, ctx):
        """Resume playback."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        if state.voice_client and state.voice_client.is_paused():
            state.voice_client.resume()
            await ctx.send(t(gid, "resumed"))

    @commands.hybrid_command(name="stop")
    async def stop(self, ctx):
        """Stop playback and clear the queue."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        state.queue.clear()
        state.current = None
        if state.voice_client:
            state.voice_client.stop()
        await ctx.send(t(gid, "stopped"))

    @commands.hybrid_command(name="leave", aliases=["dc", "disconnect"])
    async def leave(self, ctx):
        """Leave the voice channel."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        if state.voice_client:
            await state.voice_client.disconnect()
            state.voice_client = None
            state.queue.clear()
            state.current = None
        await ctx.send(t(gid, "left_channel"))

    @commands.hybrid_command(name="queue", aliases=["q"])
    async def queue_(self, ctx):
        """Show the current queue."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        if not state.current and not state.queue:
            await ctx.send(t(gid, "queue_empty"))
            return

        lines = []
        if state.current:
            lines.append(t(gid, "queue_now_playing", title=state.current.title))
        for i, song in enumerate(state.queue, start=1):
            lines.append(f"{i}. {song.title}")
        await ctx.send("\n".join(lines))

    @commands.hybrid_command(name="volume", aliases=["vol"])
    async def volume(self, ctx, level: int):
        """Set volume (0-100)."""
        gid = ctx.guild.id
        state = self.get_state(gid)
        level = max(0, min(100, level))
        state.volume = level / 100
        if state.voice_client and state.voice_client.source:
            state.voice_client.source.volume = state.volume
        await ctx.send(t(gid, "volume_set", level=level))


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="language", aliases=["lang"])
    async def language(self, ctx, code: str):
        """Change the bot's language: vi, en, or zh."""
        gid = ctx.guild.id
        code = code.lower()
        if set_lang(gid, code):
            await ctx.send(t(gid, "lang_changed", lang=LOCALES[code]["lang_name"]))
        else:
            await ctx.send(t(gid, "lang_invalid"))

    @commands.hybrid_command(name="help")
    async def help(self, ctx):
        """Show the list of commands."""
        gid = ctx.guild.id
        embed = discord.Embed(
            title=t(gid, "help_title"),
            description=t(gid, "help_body"),
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed)


def main():
    if not TOKEN:
        raise SystemExit(
            "Thiếu DISCORD_TOKEN. Tạo file .env với dòng: DISCORD_TOKEN=your_token_here"
        )

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Đã đăng nhập với tên {bot.user} (ID: {bot.user.id})")
        try:
            synced = await bot.tree.sync()
            print(f"Đã đồng bộ {len(synced)} slash command(s).")
        except Exception as e:
            print(f"Lỗi đồng bộ slash command: {e}")

    async def setup():
        await bot.add_cog(MusicCog(bot))
        await bot.add_cog(GeneralCog(bot))

    async def runner():
        await setup()
        await bot.start(TOKEN)

    asyncio.run(runner())


if __name__ == "__main__":
    main()
