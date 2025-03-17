from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN, logger
from handlers.start_handler import start
from handlers.createwallet import create_wallet_command
from handlers.check_wallet_handler import check_balance_command
from handlers.message_handler import handle_message
from database_init import init_database

def main():
    try:
        print("🚀 Đang khởi động bot...")

        # Khởi tạo database và các bảng
        init_database()

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

        # Giữ bot chạy cho đến khi dừng thủ công
        updater.idle()

    except Exception as e:
        logger.error(f"Lỗi khởi động bot: {str(e)}")
        raise

if __name__ == "__main__":
    main()