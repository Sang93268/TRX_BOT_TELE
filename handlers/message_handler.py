from telegram import Update
from telegram.ext import CallbackContext
from handlers.createwallet import create_wallet_command

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "🆕 Tạo ví TRX":
        create_wallet_command(update, context)
    elif text == "🔋 Kiểm tra số dư":
        update.message.reply_text("📜 *Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.*\nVí dụ: `/balance Txxxxxx`", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠ Lệnh không hợp lệ, vui lòng chọn từ menu!")
