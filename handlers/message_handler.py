from telegram import Update
from telegram.ext import CallbackContext
from handlers.createwallet import create_wallet_command
from handlers.customer_care import customer_care
from handlers.notification_balance import handle_notification_balance

# Dictionary lưu trạng thái thông báo và địa chỉ ví theo user_id
notification_status = {}

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id

    # Ánh xạ giữa tên hiển thị và từ khóa bạn định nghĩa
    mapping = {
        "💎 Trở thành đại lý": "chucNang1",
        "🔥 Mua lệnh": "chucNang2",
        "🔋 Kiểm tra số dư": "chucNang3",
        "☎ Chăm sóc khách hàng": "chucNang4",
        "💱 Đổi TRX <> USDT": "chucNang5",
        "🔔 Bật thông báo số dư": "chucNang6",
        "🆕 Tạo ví TRX": "chucNang7"
    }

    command = mapping.get(text)

    if command == "chucNang7":  # "🆕 Tạo ví TRX"
        create_wallet_command(update, context)
    elif command == "chucNang3":  # "🔋 Kiểm tra số dư"
        update.message.reply_text("📜 *Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.*\nVí dụ: `/balance Txxxxxx`", parse_mode="Markdown")
    elif command == "chucNang4":  # "☎ Chăm sóc khách hàng"
        customer_care(update, context)
    elif command == "chucNang6" or text.startswith("YES ") or text.startswith("NO "):  # "🔔 Bật thông báo số dư"
        handle_notification_balance(update, context)
    elif command == "chucNang1":
        update.message.reply_text("💎 *Vui lòng liên hệ *@DZFullStack* để trở thành đại lý")
    else:
        update.message.reply_text("⚠ Lệnh không hợp lệ, vui lòng chọn từ menu!")