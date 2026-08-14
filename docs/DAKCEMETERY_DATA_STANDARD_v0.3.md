# Chuẩn dữ liệu DakCemetery AI – MVP v0.3

## Mục tiêu
Chuẩn hóa dữ liệu báo cáo quản lý nghĩa trang theo hướng: **mỗi nghĩa trang là một tài sản quản lý**, có nguồn báo cáo, hiện trạng, quỹ đất, công suất, quy hoạch/đất đai, hạ tầng, đầu tư và trạng thái xác minh.

## 6 nhóm dữ liệu
1. **Định danh – địa điểm**: mã, tên, xã/phường, địa điểm, tọa độ.
2. **Chủ thể quản lý – trạng thái**: đơn vị quản lý, mô hình quản lý, trạng thái hoạt động.
3. **Quỹ đất – công suất**: tổng diện tích, đã sử dụng, còn lại, diện tích dự kiến mở rộng, khả năng tiếp nhận.
4. **Quy hoạch – đất đai – môi trường – hạ tầng**: trạng thái để cán bộ cập nhật từ hồ sơ đã xác minh.
5. **Đầu tư – kiến nghị**: nhu cầu đầu tư, mức ưu tiên, ghi chú.
6. **Nguồn – kiểm chứng**: source_id, số/ngày báo cáo, kỳ báo cáo, trạng thái xác minh, ngày cập nhật.

## Nguyên tắc quan trọng
- Không đưa thông tin cá nhân người đã mất vào MVP v0.3.
- Không tự động coi tên cột hoặc nội dung báo cáo là kết luận pháp lý.
- Không có mã tài sản thì chỉ cấp mã tạm `CEM-TEMP-xxxx`.
- Các chỉ tiêu tính toán (tỷ lệ sử dụng, tín hiệu quỹ đất, năm ước tính đầy) là dữ liệu dẫn xuất và phải tách khỏi số liệu nguồn.
- Dữ liệu thực chỉ được đưa vào kho chính thức sau bước xác minh nguồn và trách nhiệm cập nhật.
