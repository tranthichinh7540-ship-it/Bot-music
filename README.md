# Discord Music Bot (Python / discord.py)

Bot phát nhạc trong voice channel — hỗ trợ **tên bài / link YouTube / link Spotify / file nhạc đính kèm**, có **help đa ngôn ngữ** (Việt / English / 中文).

## Lệnh
Tất cả lệnh dùng được cả kiểu gõ `!lệnh` lẫn slash `/lệnh` (bot dùng `discord.py` hybrid commands).

- `!play <tên bài / link YouTube / link Spotify>` (hoặc `!p`) — hoặc **đính kèm file nhạc** vào tin nhắn kèm lệnh `!play`
- `!skip` (`!s`) — bỏ qua bài hiện tại
- `!pause` / `!resume` — tạm dừng / tiếp tục
- `!stop` — dừng và xoá hàng chờ
- `!queue` (`!q`) — xem hàng chờ
- `!volume <0-100>` — chỉnh âm lượng
- `!leave` (`!dc`) — rời voice channel
- `!help` — xem danh sách lệnh (theo ngôn ngữ đang chọn)
- `!language <vi|en|zh>` (`!lang`) — đổi ngôn ngữ bot cho server này

**Lưu ý về nguồn nhạc:**
- **YouTube**: dán link video, hoặc chỉ gõ tên bài (bot tự tìm trên YouTube)
- **Spotify**: chỉ hỗ trợ **link 1 bài hát** (`open.spotify.com/track/...`), không hỗ trợ playlist/album. Vì Spotify không cho tải audio trực tiếp, bot sẽ lấy tên bài + ca sĩ từ Spotify rồi tìm bài tương ứng trên YouTube để phát — cần cấu hình `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` (xem bên dưới)
- **File đính kèm**: đính kèm file `.mp3 .wav .m4a .ogg .flac .opus .webm` vào tin nhắn cùng lệnh `!play`

**Ngôn ngữ** chọn theo server (guild), lưu trong bộ nhớ — sẽ reset về mặc định (Tiếng Việt) khi bot restart.

## 1. Tạo bot trên Discord Developer Portal
1. Vào https://discord.com/developers/applications → **New Application**
2. Vào tab **Bot** → **Add Bot** → copy **Token** (giữ bí mật, không share/commit lên Git)
3. Trong tab **Bot**, bật **Message Content Intent** (cần cho lệnh dạng `!play`)
4. Vào tab **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands` (để dùng được slash `/play`, `/help`...)
   - Bot Permissions: `Connect`, `Speak`, `Send Messages`, `Read Message History`
   - Copy link tạo ra, mở link đó để mời bot vào server của bạn

## 2. (Tùy chọn) Lấy Spotify API key — nếu muốn dùng link Spotify
1. Vào https://developer.spotify.com/dashboard → đăng nhập → **Create app**
2. Điền tên bất kỳ, Redirect URI có thể để `http://localhost:8888/callback` (không thực sự dùng vì bot chỉ cần Client Credentials, không cần user login)
3. Vào **Settings** của app vừa tạo → copy **Client ID** và **Client Secret**

Nếu bỏ qua bước này, bot vẫn hoạt động bình thường với YouTube và file đính kèm — chỉ riêng link Spotify sẽ báo "chưa cấu hình".

## 3. Cài đặt local (để test)
Cần cài **Python 3.10+** và **FFmpeg** (bắt buộc để phát âm thanh):
- Windows: tải từ https://ffmpeg.org/download.html, thêm vào PATH
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

Sau đó:
```bash
pip install -r requirements.txt
cp .env.example .env
# Mở file .env, dán DISCORD_TOKEN (và SPOTIFY_CLIENT_ID/SECRET nếu cần) vào
python bot.py
```

## 4. Host 24/7 (chọn 1 trong các cách sau)

### Cách A — VPS (khuyên dùng, ổn định nhất)
Ví dụ VPS Ubuntu (DigitalOcean, Vultr, Contabo...):
```bash
sudo apt update && sudo apt install -y python3-pip ffmpeg
pip install -r requirements.txt
# Chạy nền bằng screen hoặc tmux:
screen -S musicbot
python3 bot.py
# Nhấn Ctrl+A rồi D để thoát mà bot vẫn chạy nền
```
Muốn tự khởi động lại khi VPS reboot → dùng `systemd` hoặc `pm2`.

### Cách B — Railway / Render (miễn phí giới hạn, dễ deploy)
1. Push code này lên một repo GitHub riêng
2. Tạo project mới trên Railway.app hoặc Render.com, kết nối repo
3. Thêm biến môi trường `DISCORD_TOKEN` (và `SPOTIFY_CLIENT_ID`/`SPOTIFY_CLIENT_SECRET` nếu dùng Spotify) trong phần Settings → Environment
4. Đảm bảo buildpack cài được FFmpeg (Railway: thêm `nixpacks.toml` hoặc dùng Dockerfile có `apt install ffmpeg`)

### Cách C — Máy tính cá nhân
Chạy được nhưng bot sẽ offline khi bạn tắt máy/mất mạng — chỉ hợp để test.

## Lưu ý
- **Không bao giờ** để lộ token/Spotify secret trong code hoặc commit lên GitHub công khai — nếu lộ, reset lại ngay trong Developer Portal tương ứng.
- File `.env` nên nằm trong `.gitignore` (đã có sẵn).
- File đính kèm phát trực tiếp qua link CDN của Discord — link này có thời hạn, nên nếu bài đang trong hàng chờ quá lâu trước khi tới lượt phát, đôi khi có thể lỗi hết hạn link; gặp trường hợp đó chỉ cần `!play` lại file đó.
