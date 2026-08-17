# locales.py — chuỗi đa ngôn ngữ cho bot (vi / en / zh)

LOCALES = {
    "vi": {
        "lang_name": "Tiếng Việt",
        "need_voice_channel": "Bạn cần vào một voice channel trước đã nhé.",
        "song_not_found": "Không tìm được bài hát này: `{error}`",
        "added_to_queue": "Đã thêm vào hàng chờ: **{title}**",
        "spotify_not_configured": "Bot chưa được cấu hình Spotify API (thiếu SPOTIFY_CLIENT_ID/SECRET trong .env).",
        "spotify_unsupported_link": "Link Spotify này chưa được hỗ trợ (chỉ hỗ trợ link bài hát, không hỗ trợ playlist/album).",
        "resolving_spotify": "Đang tra bài từ Spotify...",
        "no_query_or_file": "Cho mình tên bài / link YouTube / link Spotify, hoặc đính kèm file nhạc nhé. Vd: `!play bang bang`",
        "unsupported_attachment": "File đính kèm này không phải định dạng âm thanh mình hỗ trợ ({exts}).",
        "skipped": "Đã bỏ qua bài hiện tại.",
        "nothing_playing": "Hiện không có bài nào đang phát.",
        "paused": "Đã tạm dừng.",
        "resumed": "Tiếp tục phát.",
        "stopped": "Đã dừng và xoá hàng chờ.",
        "left_channel": "Đã rời voice channel.",
        "queue_empty": "Hàng chờ đang trống.",
        "queue_now_playing": "▶️ Đang phát: **{title}**",
        "volume_set": "Âm lượng: {level}%",
        "lang_changed": "Đã đổi ngôn ngữ sang **{lang}**.",
        "lang_invalid": "Ngôn ngữ không hợp lệ. Chọn: `vi`, `en`, `zh`.",
        "help_title": "🎵 Trợ giúp Bot Nhạc",
        "help_body": (
            "**!play <tên bài / link YouTube / link Spotify>** hoặc đính kèm file nhạc — phát/thêm vào hàng chờ\n"
            "**!skip** — bỏ qua bài hiện tại\n"
            "**!pause** / **!resume** — tạm dừng / tiếp tục\n"
            "**!stop** — dừng và xoá hàng chờ\n"
            "**!queue** — xem hàng chờ\n"
            "**!volume <0-100>** — chỉnh âm lượng\n"
            "**!leave** — rời voice channel\n"
            "**!language <vi|en|zh>** — đổi ngôn ngữ bot"
        ),
    },
    "en": {
        "lang_name": "English",
        "need_voice_channel": "You need to join a voice channel first.",
        "song_not_found": "Couldn't find that song: `{error}`",
        "added_to_queue": "Added to queue: **{title}**",
        "spotify_not_configured": "Spotify API isn't configured on this bot (missing SPOTIFY_CLIENT_ID/SECRET in .env).",
        "spotify_unsupported_link": "This Spotify link isn't supported yet (only track links, not playlists/albums).",
        "resolving_spotify": "Looking up track on Spotify...",
        "no_query_or_file": "Give me a song name / YouTube link / Spotify link, or attach an audio file. E.g. `!play bang bang`",
        "unsupported_attachment": "This attachment isn't a supported audio format ({exts}).",
        "skipped": "Skipped the current song.",
        "nothing_playing": "Nothing is playing right now.",
        "paused": "Paused.",
        "resumed": "Resumed.",
        "stopped": "Stopped and cleared the queue.",
        "left_channel": "Left the voice channel.",
        "queue_empty": "The queue is empty.",
        "queue_now_playing": "▶️ Now playing: **{title}**",
        "volume_set": "Volume: {level}%",
        "lang_changed": "Language switched to **{lang}**.",
        "lang_invalid": "Invalid language. Choose: `vi`, `en`, `zh`.",
        "help_title": "🎵 Music Bot Help",
        "help_body": (
            "**!play <song name / YouTube link / Spotify link>** or attach an audio file — play/queue\n"
            "**!skip** — skip current song\n"
            "**!pause** / **!resume** — pause / resume\n"
            "**!stop** — stop and clear queue\n"
            "**!queue** — show queue\n"
            "**!volume <0-100>** — set volume\n"
            "**!leave** — leave voice channel\n"
            "**!language <vi|en|zh>** — change bot language"
        ),
    },
    "zh": {
        "lang_name": "中文",
        "need_voice_channel": "请先加入一个语音频道。",
        "song_not_found": "找不到这首歌：`{error}`",
        "added_to_queue": "已加入队列：**{title}**",
        "spotify_not_configured": "该机器人尚未配置 Spotify API（.env 中缺少 SPOTIFY_CLIENT_ID/SECRET）。",
        "spotify_unsupported_link": "暂不支持此 Spotify 链接（仅支持单曲链接，不支持播放列表/专辑）。",
        "resolving_spotify": "正在从 Spotify 查询歌曲...",
        "no_query_or_file": "请提供歌曲名称/YouTube 链接/Spotify 链接，或附带一个音频文件。例如：`!play bang bang`",
        "unsupported_attachment": "该附件不是支持的音频格式（{exts}）。",
        "skipped": "已跳过当前歌曲。",
        "nothing_playing": "当前没有正在播放的歌曲。",
        "paused": "已暂停。",
        "resumed": "已继续播放。",
        "stopped": "已停止播放并清空队列。",
        "left_channel": "已离开语音频道。",
        "queue_empty": "队列为空。",
        "queue_now_playing": "▶️ 正在播放：**{title}**",
        "volume_set": "音量：{level}%",
        "lang_changed": "语言已切换为 **{lang}**。",
        "lang_invalid": "无效的语言，请选择：`vi`、`en`、`zh`。",
        "help_title": "🎵 音乐机器人帮助",
        "help_body": (
            "**!play <歌曲名 / YouTube链接 / Spotify链接>** 或附带音频文件 — 播放/加入队列\n"
            "**!skip** — 跳过当前歌曲\n"
            "**!pause** / **!resume** — 暂停 / 继续\n"
            "**!stop** — 停止并清空队列\n"
            "**!queue** — 查看队列\n"
            "**!volume <0-100>** — 设置音量\n"
            "**!leave** — 离开语音频道\n"
            "**!language <vi|en|zh>** — 切换机器人语言"
        ),
    },
}

DEFAULT_LANG = "vi"

# guild_id -> language code, kept in memory (resets on bot restart)
_guild_lang: dict[int, str] = {}


def get_lang(guild_id: int) -> str:
    return _guild_lang.get(guild_id, DEFAULT_LANG)


def set_lang(guild_id: int, lang: str) -> bool:
    if lang not in LOCALES:
        return False
    _guild_lang[guild_id] = lang
    return True


def t(guild_id: int, key: str, **kwargs) -> str:
    lang = get_lang(guild_id)
    template = LOCALES[lang].get(key) or LOCALES[DEFAULT_LANG][key]
    return template.format(**kwargs) if kwargs else template
