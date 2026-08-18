# DakDrain AI (Quản lý thoát nước và xử lý nước thải)

## Quy chuẩn bắt buộc

DakDrain AI áp dụng **Trung tâm xuất dữ liệu** ngay trong Streamlit.

Người dùng không cần vào GitHub để lấy dữ liệu.

### Tối thiểu phải tải được
- CSV – dữ liệu dạng bảng.
- Excel – bảng dữ liệu + thông tin xuất + từ điển dữ liệu.
- JSON – dữ liệu máy đọc.
- GeoJSON – khi có tọa độ.
- ZIP FULL DATA PACKAGE – gói đầy đủ gồm dữ liệu, metadata, manifest và từ điển.

### Chuỗi quản trị
**Lưu vực → Tuyến cống/hố ga → Trạm bơm → Nhà máy xử lý nước thải → Điểm xả**

Điểm ngập phải liên kết được với lưu vực và mạng thoát nước.

### An toàn dữ liệu
GitHub Public/Streamlit Public chỉ dùng dữ liệu mẫu hoặc tổng hợp an toàn.
Dữ liệu thật chỉ xuất theo quyền trong môi trường nội bộ.
