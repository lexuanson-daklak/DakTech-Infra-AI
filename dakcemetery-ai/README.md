# DakCemetery AI (Quản lý nghĩa trang)

**Phân hệ quản lý nghĩa trang thuộc DakTech Infra AI**

**Phiên bản hiện tại:** MVP v0.6

## Mục tiêu

Quản lý dữ liệu nghĩa trang theo chuỗi:
**Hồ sơ nguồn → Danh mục ứng viên → Rà soát → Xác minh → Danh mục chính thức → Bản đồ → Dashboard**

## Chức năng hiện tại

- Dashboard nghĩa trang.
- Danh mục nghĩa trang.
- Hàng đợi rà soát.
- Bản đồ nghĩa trang.
- Hồ sơ nghĩa trang 360°.
- Kho báo cáo nghĩa trang.
- Mô phỏng nạp báo cáo.

## Trọng tâm MVP v0.6

- 303 bản ghi ứng viên từ 32 nguồn.
- 267 nhóm kỹ thuật tên + địa bàn.
- 20 nhóm có nhiều dòng, tổng 56 dòng cần đối chiếu.
- Hàng đợi P1/P2/P3 phục vụ rà soát theo mức ưu tiên.
- Không tự coi dữ liệu ứng viên là danh mục nghĩa trang chính thức.
- Chỉ dữ liệu đã được cán bộ xác minh mới chuyển sang danh mục chính thức.

## Mã vận hành hiện tại

Các trang Streamlit của phân hệ hiện vẫn nằm trong thư mục `pages/`, gồm:
- `cemetery_dashboard.py`
- `cemetery_inventory.py`
- `cemetery_review_queue.py`
- `cemetery_map.py`
- `dakcemetery.py`
- `cemetery_sources.py`
- `cemetery_import.py`

Không di chuyển các file này ở giai đoạn hiện tại để tránh ảnh hưởng ứng dụng đang chạy.
