# DakRoad AI — MVP v0.1

Sản phẩm demo dự thi cá nhân về quản trị tài sản kết cấu hạ tầng đường bộ và hỗ trợ xử lý sử dụng tạm thời lòng đường, hè phố.

**Dữ liệu, mức thu, kết quả xử lý và giấy phép đều là mô phỏng, không có giá trị pháp lý.**

## Tài khoản demo

- `nguoidan_demo`
- `canbo_demo`
- `lanhdao_demo`

Mật khẩu chung: `DakRoad@2026`

## Chạy trên máy

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python database/init_database.py
streamlit run streamlit_app.py
```

## Khôi phục dữ liệu

```bash
python -c "from database.init_database import init_db; init_db(reset=True)"
```

## Đưa lên mạng

Đưa thư mục lên GitHub, kết nối với Streamlit Community Cloud và chọn file `streamlit_app.py`.


## Điểm mới phiên bản 0.2

- Bổ sung lớp hỗ trợ tự động có cấu trúc.
- Sinh tóm tắt, cảnh báo, mã quy tắc và checklist cho cán bộ.
- Hoạt động ổn định ngay cả khi không có API AI.
- Bổ sung checklist kiểm thử thủ công.
- Làm rõ ranh giới giữa Rule Engine và quyết định của người có thẩm quyền.


## Phiên bản 0.3

- Bổ sung hướng dẫn GitHub và Streamlit Community Cloud.
- Bổ sung file thông tin truy cập dành cho Ban Giám khảo.
- Bổ sung checklist trước khi nộp.
- Bổ sung thông tin phiên bản trên giao diện.


## Phiên bản 0.5 - cập nhật dữ liệu thực tế

- Bổ sung kho 13 nguồn văn bản và hồ sơ địa phương.
- Chuẩn hóa 2 bộ mức thu chính thức được cung cấp: NQ24/2024 (Đắk Lắk cũ) và NQ35/2022 (Phú Yên cũ).
- Tách đề án/kế hoạch/báo cáo địa phương khỏi dữ liệu mức thu chính thức.
- Bổ sung Legal Version Control Layer và 6 cờ rủi ro pháp lý.
- Bổ sung trang tra cứu mức thu theo đúng đơn vị tính: m2/tháng, m2/đợt, xe/lượt, xe/tháng.
- Không tự động áp dụng tỷ lệ phân bổ nguồn thu khi hồ sơ còn xung đột hoặc đang chờ thẩm định.


## Phiên bản 0.6 - cập nhật dữ liệu đợt 2

- Kho nguồn: 22 hồ sơ/văn bản.
- Đề xuất địa phương: 17 dòng.
- Chi tiết mức thu đề xuất: 61 dòng.
- Vấn đề chất lượng dữ liệu cần xử lý: 8.
- Bổ sung trạng thái `LOCAL_NO_COLLECTION`, `LOCAL_NOT_ELIGIBLE` và `LOCAL_RECOMMEND_CENTRALIZATION`.
- Bổ sung nguyên tắc: không phải địa phương nào cũng bắt buộc phải xây dựng nguồn thu; an toàn giao thông và điều kiện pháp lý là điều kiện tiên quyết.
