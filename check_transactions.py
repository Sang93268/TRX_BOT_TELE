import requests
import time
import mysql.connector
from config import TRONGRID_API_URL, TRONGRID_API_KEY, BOT_TOKEN, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import telegram
from tronpy.keys import to_base58check_address

# Khởi tạo bot Telegram
bot = telegram.Bot(token=BOT_TOKEN)

# Hàm kết nối database
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Hàm lấy giao dịch mới từ API TrongGrid
def get_transactions(address):
    headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
    url = f"{TRONGRID_API_URL}{address}/transactions"
    response = requests.get(url, headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return data["data"]  # Danh sách giao dịch
    return []

# Hàm lấy danh sách ví từ database
def get_user_wallets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT telegram_id, address FROM users")
    wallets = cursor.fetchall()
    conn.close()
    return wallets

# Hàm kiểm tra xem giao dịch đã tồn tại trong database chưa
def is_transaction_exists(tx_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE tx_id = %s", (tx_id,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

# Hàm lưu giao dịch vào database
def save_transaction(tx_id, address, amount, sender):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (tx_id, address, amount, sender)
        VALUES (%s, %s, %s, %s)
    """, (tx_id, address, amount, sender))
    conn.commit()
    conn.close()

# Hàm kiểm tra và gửi thông báo nếu có giao dịch mới
def check_new_transactions():
    wallets = get_user_wallets()

    for user in wallets:
        telegram_id = user["telegram_id"]
        address = user["address"]
        transactions = get_transactions(address)

        for tx in transactions:
            tx_id = tx["txID"]

            # Kiểm tra nếu giao dịch đã tồn tại thì bỏ qua
            if is_transaction_exists(tx_id):
                continue

            contract = tx.get("raw_data", {}).get("contract", [{}])[0]
            contract_type = contract.get("type", "")

            if contract_type == "TransferContract":
                sender_hex = contract["parameter"]["value"]["owner_address"]
                sender = to_base58check_address(sender_hex)  # Chuyển đổi hex -> TRON Address
                amount = contract["parameter"]["value"]["amount"] / 1e6
            else:
                sender = "Không xác định"
                amount = 0

            # Lưu giao dịch vào database
            save_transaction(tx_id, address, amount, sender)

            # Gửi thông báo
            message = (
                f"📩 *Giao dịch mới phát hiện!*\n"
                f"💰 *Số tiền:* {amount} TRX\n"
                f"👤 *Từ:* {sender}\n"
                f"🔖 *TxID:* `{tx_id}`\n"
                f"🔗 [Xem giao dịch](https://tronscan.org/#/transaction/{tx_id})"
            )

            bot.send_message(chat_id=telegram_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)

# Chạy kiểm tra giao dịch mỗi 1 giây
if __name__ == "__main__":
    while True:
        check_new_transactions()
        time.sleep(2)  # Đợi 30 giây trước khi kiểm tra tiếp
