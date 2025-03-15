from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN, logger
from handlers import start, create_wallet_command, check_balance_command, handle_message

def main():
    try:
        print("🚀 Đang khởi động bot...")

        # Tạo updater
        updater = Updater(BOT_TOKEN, use_context=True)
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
