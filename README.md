# TRX Bot

## Cấu hình môi trường

Để chạy bot, bạn cần tạo file `.env` trong thư mục gốc của dự án với các thông tin sau:

```env
# TRONGRID API Configuration
TRONGRID_API_KEY=your_trongrid_api_key
TRONGRID_API_URL=https://nile.trongrid.io/v1/accounts/

# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_database_password
DB_NAME=trx_bot
```

### Hướng dẫn cấu hình:

1. **TRONGRID API**:
   - Đăng ký tài khoản tại [TRONGRID](https://www.trongrid.io/)
   - Lấy API key từ dashboard
   - Thay `your_trongrid_api_key` bằng API key của bạn

2. **Telegram Bot**:
   - Tạo bot mới thông qua [@BotFather](https://t.me/botfather) trên Telegram
   - Lưu lại token được cấp
   - Thay `your_telegram_bot_token` bằng token của bot

3. **Database**:
   - Đảm bảo MySQL đã được cài đặt
   - Tạo database mới với tên `trx_bot`
   - Điền thông tin kết nối database của bạn vào các trường tương ứng
   - Nếu không có mật khẩu, để trống `DB_PASSWORD`

### Lưu ý:
- Không chia sẻ file `.env` của bạn
- Đảm bảo file `.env` đã được thêm vào `.gitignore`
- Kiểm tra kết nối database trước khi chạy bot