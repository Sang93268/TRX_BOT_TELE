
from telegram import Update
from telegram.ext import CallbackContext

def tro_thanh_day_ly(update: Update, context: CallbackContext):
    update.message.reply_text("💎 *Vui lòng liên hệ @DZFullStack để trở thành đại lý")
    return