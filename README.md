# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
**Phiên bản: MVP v0.7.2**

## Trọng tâm hiện tại
- DakWater AI – Quản lý cấp nước sạch.
- DakDrain AI – Quản lý thoát nước và xử lý nước thải.

DakCemetery AI tạm dừng tại v0.6.x. DakRoad AI là sản phẩm khởi nguồn.

## Quy chuẩn giao diện
- Tiếng Việt là ngôn ngữ chính.
- Không hiển thị tên file kỹ thuật cho người dùng.
- Dashboard gọi là **Bảng điều hành**.
- Mỗi phân hệ có **Trung tâm xuất dữ liệu**.
- Người dùng tải dữ liệu trực tiếp từ Streamlit, không cần vào GitHub.

## Lưu ý triển khai
Các file của bản cập nhật này phải nằm trực tiếp tại thư mục gốc đúng cấu trúc (`pages/`, `core/`, `docs/`...).
Không được tạo thêm lớp thư mục `UPLOAD_TO_REPO_ROOT/`.
