import requests
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

def swap(update: Update, context: CallbackContext):
    update.message.reply_text("🌐 Vui lòng sử dụng ví cần chuyển đổi và tiến hành chuyển USDT hoặc TRX tới địa chỉ dưới đây.\n\n"
                             "⏱ Trong vòng 90s, hệ thống sẽ tự động tiến hành quy đổi và chuyển ngược lại TRX hoặc USDT tới địa chỉ của bạn.\n\n"
                             "💰 Mức tối thiếu chuyển đổi là 10 USDT hoặc 50 TRX\n\n"
                             "📋 <code>TMbDuidjfP25hEkJymi8K5z1J7F3ueaPj6</code>",
                             parse_mode=ParseMode.HTML)
