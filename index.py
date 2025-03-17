import logging
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from tronpy.keys import PrivateKey

# 🔹 API Key TrongGrid (Thay thế bằng API Key của bạn)
TRONGRID_API_KEY = "abd3c7d2-212d-498f-b552-acd61ed78fbd"
# TRONGRID_API_URL = "https://api.trongrid.io/v1/accounts/"
TRONGRID_API_URL = "https://nile.trongrid.io/v1/accounts/"

# Thiết lập logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Hàm tạo ví TRX
def create_wallet():
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()
    return {
        "private_key": private_key.hex(),
        "public_key": private_key.public_key.hex(),
        "address": address
    }

# Hàm lấy số dư TRX từ API TrongGrid
def get_balance(address):
    try:
        headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
        response = requests.get(f"{TRONGRID_API_URL}{address}", headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            balance = data["data"][0].get("balance", 0) / 1e6  # Chuyển từ SUN -> TRX
            return balance
        else:
            return "⚠️ Không tìm thấy thông tin ví!"
    except Exception as e:
        return f"❌ Lỗi lấy số dư: {str(e)}"

# Hàm gửi menu bàn phím cố định
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

# Hàm xử lý tin nhắn từ bàn phím cố định
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "🆕 Tạo ví TRX":
        create_wallet_command(update, context)
    elif text == "💰 Kiểm tra số dư ví":
        update.message.reply_text("📜 Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.\nVí dụ: `/balance Txxxxxx`", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠ Lệnh không hợp lệ, vui lòng chọn từ menu!")

# Hàm khởi động bot
def main():
    try:
        TOKEN = "7785074026:AAHJHMQiMKTrsPqpG3DCdWKYep25-YfHcfQ"  # 🔹 Thay bằng token của bạn
        print("🚀 Đang khởi động bot...")

        # Tạo updater
        updater = Updater(TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Đăng ký các lệnh và handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("createwallet", create_wallet_command))
        dispatcher.add_handler(CommandHandler("balance", check_balance_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

        # Bắt đầu bot
        updater.start_polling()
        print("✅ Bot đã sẵn sàng!")

        updater.idle()

    except Exception as e:
        logger.error(f"Lỗi khởi động bot: {str(e)}")

if __name__ == "__main__":
    main()
