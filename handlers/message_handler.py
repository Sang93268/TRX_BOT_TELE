from telegram import Update
from telegram.ext import CallbackContext
from handlers.createwallet import create_wallet_command
from handlers.customer_care import customer_care
from handlers.check_transactions import check_new_transactions

# Dictionary lưu trạng thái thông báo và địa chỉ ví theo user_id
notification_status = {}

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id

    # Ánh xạ giữa tên hiển thị và từ khóa bạn định nghĩa
    mapping = {
        "💎 Trở thành đại lý": "chucNang1",
        "🔥 Mua lệnh": "chucNang2",
        "🔋 Kiểm tra số dư": "chucNang3",
        "☎ Chăm sóc khách hàng": "chucNang4",
        "💱 Đổi TRX <> USDT": "chucNang5",
        "🔔 Bật thông báo số dư": "chucNang6",
        "🆕 Tạo ví TRX": "chucNang7"
    }

    command = mapping.get(text)

    if command == "chucNang7":  # "🆕 Tạo ví TRX"
        create_wallet_command(update, context)
    elif command == "chucNang3":  # "🔋 Kiểm tra số dư"
        update.message.reply_text("📜 *Vui lòng nhập địa chỉ ví TRX để kiểm tra số dư.*\nVí dụ: `/balance Txxxxxx`", parse_mode="Markdown")
    elif command == "chucNang4":  # "☎ Chăm sóc khách hàng"
        customer_care(update, context)
    elif command == "chucNang6":  # "🔔 Bật thông báo số dư"
        update.message.reply_text(
            "🔔  Đây là chức năng thông báo biến động số dư lệnh và thông tin hợp đồng sử dụng dịch vụ mua lệnh\n\n"
            "✨ Sau khi bật chức năng này, bạn sẽ nhận được tin nhắn thông báo biến động số dư lệnh ngay sau mỗi lần thực hiện giao dịch.\n\n"
            "👉 Để bật thông báo, xin vui lòng gửi tin nhắn cho BOT với cú pháp: YES Địa_chỉ_ví_của_bạn\n"
            "✏️ Ví dụ mẫu cú pháp: YES abcdefghik...\n\n"
            "👉 Để tắt thông báo, xin vui lòng gửi tin nhắn cho BOT với cú pháp: NO Địa_chỉ_ví_của_bạn\n"
            "✏️ Ví dụ mẫu cú pháp: NO abcdefghik...\n\n"
            "📌 Nếu bạn có bất kỳ thắc mắc gì về dịch vụ, xin vui lòng liên hệ CSKH để được giải đáp và hỗ trợ kịp thời."
        )
    elif text.startswith("YES "):  # Bật thông báo
        try:
            address = text.split("YES ")[1].strip()
            notification_status[user_id] = {"enabled": True, "address": address}
            update.message.reply_text(f"✅ Đã bật thông báo biến động số dư cho ví: {address}")
            # Thêm job định kỳ
            context.job_queue.run_repeating(
                check_new_transactions,
                interval=30,  # Chạy mỗi 30 giây
                first=0,
                context={"address": address, "user_id": user_id},
                name=str(user_id)  # Tên job để dễ quản lý
            )
        except IndexError:
            update.message.reply_text("⚠ Vui lòng cung cấp địa chỉ ví theo cú pháp: YES Địa_chỉ_ví_của_bạn")
    elif text.startswith("NO "):  # Tắt thông báo
        try:
            address = text.split("NO ")[1].strip()
            if user_id in notification_status and notification_status[user_id]["address"] == address:
                notification_status[user_id]["enabled"] = False
                # Dừng job định kỳ
                for job in context.job_queue.jobs():
                    if job.name == str(user_id):
                        job.schedule_removal()
                update.message.reply_text(f"✅ Đã tắt thông báo biến động số dư cho ví: {address}")
            else:
                update.message.reply_text("⚠ Không tìm thấy thông báo nào để tắt cho ví này!")
        except IndexError:
            update.message.reply_text("⚠ Vui lòng cung cấp địa chỉ ví theo cú pháp: NO Địa_chỉ_ví_của_bạn")
    else:
        update.message.reply_text("⚠ Lệnh không hợp lệ, vui lòng chọn từ menu!")