from telegram import Update
from telegram.ext import CallbackContext
from handlers.get_wallet import create_wallet
from database import check_existing_wallet, save_wallet

def create_wallet_command(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id

    # 🔍 Kiểm tra xem user đã có ví chưa
    existing_wallet = check_existing_wallet(telegram_id)

    if existing_wallet:
        update.message.reply_text(
            f"😡 Ngu ngốc! Mày đã có ví rồi mà còn đòi nữa hả?\n"
            f"🆔 *Địa chỉ ví của mày:* `{existing_wallet['address']}`",
            parse_mode="Markdown"
        )
    else:
        # ✅ Tạo ví mới
        wallet = create_wallet()
        save_wallet(telegram_id, wallet["address"], wallet["private_key"])

        response = (
            "🎉 *Ví TRX mới của bạn đã được tạo!*\n\n"
            f"🆔 *Địa chỉ ví:* `{wallet['address']}`\n"
            f"🔑 *Private Key:* `{wallet['private_key']}`\n"
            "⚠ *Lưu ý:* Không chia sẻ Private Key với ai!\n"
        )
        update.message.reply_text(response, parse_mode="Markdown")
