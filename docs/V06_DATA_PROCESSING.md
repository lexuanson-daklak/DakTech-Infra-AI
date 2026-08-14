# DakCemetery AI – Quy trình xử lý dữ liệu thực tế v0.6

v0.6 xử lý lớp dữ liệu dẫn xuất từ các báo cáo đã thu thập, nhưng **không thay thế báo cáo gốc** và **không tự xác minh**.

## Ba lớp dữ liệu
1. **Hồ sơ nguồn**: PDF/DOC/XLSX/biểu báo cáo gốc, giữ nguyên.
2. **Danh mục ứng viên**: 303 bản ghi dẫn xuất, được chuẩn hóa kỹ thuật và xếp hàng đợi kiểm tra.
3. **Danh mục chính thức**: chỉ hình thành sau khi cán bộ đối chiếu nguồn và xác minh.

## Những việc v0.6 thực hiện
- chuẩn hóa kỹ thuật tên và địa bàn để tìm kiếm/nhóm;
- gợi ý loại hình chỉ từ đúng chữ xuất hiện trong tên nguồn;
- nhóm các dòng **cùng tên + cùng địa bàn** để rà soát;
- giữ nguyên cờ chất lượng diện tích, không tự sửa;
- phát hiện thiếu diện tích, thiếu đơn vị quản lý, chưa rõ loại hình;
- xếp P1/P2/P3 để tổ chức công việc;
- tạo trường trống để cán bộ ghi kết luận xác minh.

## Những việc v0.6 không làm
- không kết luận 303 bản ghi là 303 nghĩa trang;
- không kết luận 267 nhóm kỹ thuật là 267 nghĩa trang;
- không tự gộp 20 nhóm cùng tên;
- không tự giải nghĩa ký hiệu `NT`;
- không tự đổi số liệu diện tích;
- không tự cấp mã chính thức;
- không đưa tên/địa bàn chi tiết của dữ liệu nội bộ lên GitHub Public.
