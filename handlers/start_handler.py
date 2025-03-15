from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    keyboard = [
        ["💎 Trở thành đại lý", "🔥 Mua lệnh"],
        ["🔋 Kiểm tra số dư", "☎ Chăm sóc khách hàng"],
        ["💱 Đổi TRX <> USDT", "🔔 Bật thông báo số dư"],
        ["🆕 Tạo ví TRX", "💰 Kiểm tra số dư ví"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text("🔽 Chọn chức năng bạn muốn:", reply_markup=reply_markup)
