# Các phân hệ của DakTech Infra AI

**DakTech Infra AI** là nền tảng mẹ quản trị hạ tầng kỹ thuật Đắk Lắk.

Thư mục `modules/` được tạo để người xem GitHub nhìn ngay cấu trúc sản phẩm theo từng phân hệ.
Tên thư mục kỹ thuật được giữ ngắn gọn bằng tiếng Anh để ổn định đường dẫn và mã nguồn; ngay bên cạnh luôn ghi chú tiếng Việt để cán bộ dễ hiểu.

## Các phân hệ

- `dakcemetery-ai` (**Quản lý nghĩa trang**)
- `dakroad-ai` (**Quản lý kết cấu hạ tầng đường bộ**)
- `dakwater-ai` (**Quản lý cấp nước sạch**)
- `dakdrain-ai` (**Quản lý thoát nước và xử lý nước thải**)

## Nguyên tắc kiến trúc

- `DakTech Infra AI` = nền tảng mẹ.
- Mỗi phân hệ có trang giới thiệu riêng trong `modules/`.
- Mã vận hành hiện tại tiếp tục dùng chung lõi dữ liệu, bản đồ, kiểm tra quy tắc, kho pháp lý và dashboard.
- Không đưa dữ liệu nội bộ, báo cáo gốc hoặc dữ liệu nhạy cảm lên GitHub Public.
- Chưa di chuyển mã đang chạy khỏi `pages/`, `core/`, `data/` ở giai đoạn MVP v0.6 để tránh ảnh hưởng Streamlit.
