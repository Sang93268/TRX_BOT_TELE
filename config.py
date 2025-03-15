import logging

# 🔹 API Key TrongGrid
TRONGRID_API_KEY = "abd3c7d2-212d-498f-b552-acd61ed78fbd"
TRONGRID_API_URL = "https://nile.trongrid.io/v1/accounts/"

# 🔹 Token Telegram Bot
BOT_TOKEN = "7785074026:AAHJHMQiMKTrsPqpG3DCdWKYep25-YfHcfQ"  # 🔹 Thay bằng token của bạn


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "trx_bot"

# Thiết lập logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)