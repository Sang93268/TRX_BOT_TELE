from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN, logger
from handlers.start_handler import start
from handlers.createwallet import create_wallet_command
from handlers.check_wallet_handler import check_balance_command
from handlers.message_handler import handle_message

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
        # Lưu ý: CommandHandler("getbalance", get_balance) không hợp lý vì get_balance không phải handler
        # Nếu muốn dùng, hãy tạo một handler riêng thay vì gọi trực tiếp get_balance

        # Bắt đầu bot
        updater.start_polling()
        print("✅ Bot đã sẵn sàng!")

        # Giữ bot chạy cho đến khi dừng thủ công
        updater.idle()

    except Exception as e:
        logger.error(f"Lỗi khởi động bot: {str(e)}")
        raise  # Để dễ debug, bạn có thể raise lỗi lên

if __name__ == "__main__":
    main()