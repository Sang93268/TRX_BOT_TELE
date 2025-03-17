from telegram import Update
from telegram.ext import CallbackContext

def customer_care(update: Update, context: CallbackContext):
    update.message.reply_text("🔔 Vui lòng liên hệ @DZFullStack để được hỗ trợ !")