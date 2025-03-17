import requests
from telegram import Update
from telegram.ext import CallbackContext

def mua_lenh(update: Update, context: CallbackContext):
    update.message.reply_text("🌐 Chào mừng bạn đến với BOT tự động để mua số lệnh chuyển khoản với mức phí thấp nhất.\n\n"
                              "🔐 Vui lòng nhập mã đại lý tiến hành mua lệnh.")
    return
