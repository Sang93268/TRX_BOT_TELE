import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import mysql.connector
from config import TRONGRID_API_URL, TRONGRID_API_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from tronpy.keys import to_base58check_address

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_transactions(address):
    headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
    url = f"{TRONGRID_API_URL}{address}/transactions"
    response = requests.get(url, headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return data["data"]
    return []

def is_transaction_exists(tx_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE tx_id = %s", (tx_id,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def save_transaction(tx_id, address, amount, sender):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (tx_id, address, amount, sender)
        VALUES (%s, %s, %s, %s)
    """, (tx_id, address, amount, sender))
    conn.commit()
    conn.close()

def check_new_transactions(context):
    """Chạy định kỳ để kiểm tra giao dịch mới"""
    job = context.job
    address = job.context.get("address")  # Lấy địa chỉ ví từ context của job
    user_id = job.context.get("user_id")  # Lấy user_id từ context của job
    
    if not address or not user_id:
        return
        
    transactions = get_transactions(address)

    for tx in transactions:
        tx_id = tx["txID"]
        if is_transaction_exists(tx_id):
            continue

        contract = tx.get("raw_data", {}).get("contract", [{}])[0]
        contract_type = contract.get("type", "")

        if contract_type == "TransferContract":
            sender_hex = contract["parameter"]["value"]["owner_address"]
            sender = to_base58check_address(sender_hex)
            amount = contract["parameter"]["value"]["amount"] / 1e6
        else:
            sender = "Không xác định"
            amount = 0

        save_transaction(tx_id, address, amount, sender)

        message = (
            f"📩 *Giao dịch mới phát hiện!*\n"
            f"💰 *Số tiền:* {amount} TRX\n"
            f"👤 *Từ:* {sender}\n"
            f"🔖 *TxID:* `{tx_id}`\n"
            f"🔗 [Xem giao dịch](https://tronscan.org/#/transaction/{tx_id})"
        )
        context.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)