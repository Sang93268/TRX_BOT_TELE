from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from wallet import create_wallet, get_balance

# Gửi menu bàn phím cố định
def start(update: Update, context: CallbackContext):
    keyboard = [
        ["💎 Trở thành đại lý", "🔥 Mua lệnh"],
        ["🔋 Kiểm tra số dư", "☎ Chăm sóc khách hàng"],
        ["💱 Đổi TRX <> USDT", "🔔 Bật thông báo số dư"],
        ["🆕 Tạo ví TRX", "💰 Kiểm tra số dư ví"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text("🔽 Chọn chức năng bạn muốn:", reply_markup=reply_markup)

# Xử lý tạo ví TRX
def create_wallet_command(update: Update, context: CallbackContext):
    wallet = create_wallet()
    response = (
        "🎉 *Ví TRX mới của bạn đã được tạo!*\n\n"
        f"🆔 *Địa chỉ ví:* `{wallet['address']}`\n"
        f"🔑 *Private Key:* `{wallet['private_key']}`\n"
        "⚠ *Lưu ý:* Không chia sẻ Private Key với ai!\n"
    )
    update.message.reply_text(response, parse_mode="Markdown")

# Xử lý kiểm tra số dư TRX từ API TrongGrid
def check_balance_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❌ Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.\nVí dụ: `/balance Txxxxxx`")
        return

    address = context.args[0]
    balance = get_balance(address)
    update.message.reply_text(f"💰 *Số dư của ví:* `{address}`\n📊 *Số dư:* `{balance} TRX`", parse_mode="Markdown")

# Xử lý tin nhắn từ bàn phím cố định
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "🆕 Tạo ví TRX":
        create_wallet_command(update, context)
    elif text == "💰 Kiểm tra số dư ví":
        update.message.reply_text("📜 *Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.*\nVí dụ: `/balance Txxxxxx`", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠ Lệnh không hợp lệ, vui lòng chọn từ menu!")
