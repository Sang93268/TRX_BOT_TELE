from telegram import Update
from telegram.ext import CallbackContext
from handlers.get_wallet import get_balance

def check_balance_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❌ Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.\nVí dụ: `/balance Txxxxxx`")
        return

    address = context.args[0]
    balance = get_balance(address)
    update.message.reply_text(f"💰 *Số dư của ví:* `{address}`\n📊 *Số dư:* `{balance} TRX`", parse_mode="Markdown")