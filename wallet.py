import requests
from tronpy.keys import PrivateKey
from config import TRONGRID_API_URL, TRONGRID_API_KEY

# Hàm tạo ví TRX
def create_wallet():
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()
    return {
        "private_key": private_key.hex(),
        "public_key": private_key.public_key.hex(),
        "address": address
    }

# Hàm lấy số dư TRX từ API TrongGrid
def get_balance(address):
    try:
        headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
        response = requests.get(f"{TRONGRID_API_URL}{address}", headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            balance = data["data"][0].get("balance", 0) / 1e6  # Chuyển từ SUN -> TRX
            return balance
        else:
            return "⚠️ Không tìm thấy thông tin ví!"
    except Exception as e:
        return f"❌ Lỗi lấy số dư: {str(e)}"
