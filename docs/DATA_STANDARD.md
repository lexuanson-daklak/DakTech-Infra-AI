# Chuẩn dữ liệu Asset Registry – MVP v0.2

## Trường bắt buộc
- `module`: road / cemetery / water / drain.
- `asset_code`: mã định danh duy nhất.
- `asset_name`: tên tài sản/công trình.
- `asset_type`: loại tài sản.
- `locality`: địa bàn.
- `management_unit`: đơn vị quản lý/chịu trách nhiệm dữ liệu.
- `status`: ACTIVE / REVIEW / RESTRICTED / LIMITED / CLOSED / PLANNED / INACTIVE.
- `source_id`: mã nguồn dữ liệu.
- `updated_at`: ngày cập nhật, định dạng YYYY-MM-DD.

## Trường khuyến nghị
- `latitude`, `longitude` hoặc hình học GIS.
- `investment_need`.
- `geometry_type`.

## Truy vết dữ liệu
MVP v0.2 sinh `record_hash` từ các trường lõi để phát hiện thay đổi. Khi triển khai thực tế cần có lịch sử phiên bản/audit log trong CSDL, không chỉ dựa trên CSV.

## Nguyên tắc
1. Giữ nguyên dữ liệu nguồn.
2. Không ghi đè lịch sử.
3. Một tài sản có một mã định danh ổn định.
4. Mọi bản ghi phải xác định nguồn và thời điểm cập nhật.
5. Dữ liệu mâu thuẫn phải được gắn cờ để người có trách nhiệm xử lý.
