import mysql.connector
import os
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, logger

def init_database():
    # Kiểm tra file trạng thái
    state_file = ".db_initialized"
    if os.path.exists(state_file):
        logger.info("✅ Database đã được khởi tạo trước đó!")
        return

    try:
        # Kết nối đến MySQL server (không chọn database)
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Tạo database nếu chưa tồn tại
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        # Tạo bảng users nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                address VARCHAR(255) NOT NULL,
                private_key VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tạo bảng transactions nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tx_id VARCHAR(255) UNIQUE NOT NULL,
                address VARCHAR(255) NOT NULL,
                amount DECIMAL(18,6) NOT NULL,
                sender VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        logger.info("✅ Khởi tạo database thành công!")

        # Tạo file trạng thái để đánh dấu đã khởi tạo
        with open(state_file, 'w') as f:
            f.write('initialized')
        
    except mysql.connector.Error as e:
        logger.error(f"❌ Lỗi khởi tạo database: {str(e)}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close() 