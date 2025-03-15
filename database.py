import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Hàm kết nối đến MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Hàm kiểm tra xem user Telegram đã có ví chưa
def check_existing_wallet(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT address FROM users WHERE telegram_id = %s", (user_id,))
    wallet = cursor.fetchone()
    conn.close()
    return wallet

# Hàm lưu ví mới vào database
def save_wallet(user_id, address, private_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id, address, private_key) VALUES (%s, %s, %s)", 
                   (user_id, address, private_key))
    conn.commit()
    conn.close()
