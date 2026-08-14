# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
Phiên bản: **MVP v0.3**

DakTech Infra AI là nền tảng mẹ phát triển từ tư duy và kiến trúc của **DakRoad AI**. Mục tiêu là dùng một lõi chung để quản trị nhiều lĩnh vực hạ tầng kỹ thuật, thay vì tạo nhiều phần mềm rời rạc.

## Các phân hệ
- 🛣️ **DakRoad AI** – kết cấu hạ tầng đường bộ; phân hệ khởi nguồn và tiếp tục giữ thương hiệu riêng.
- ⚱️ **DakCemetery AI** – nghĩa trang và cơ sở hỏa táng.
- 💧 **DakWater AI** – cấp nước sạch.
- 🌧️ **DakDrain AI** – thoát nước và xử lý nước thải.

## Trọng tâm MVP v0.3: DakCemetery AI
MVP v0.3 chuyển từ dữ liệu nghĩa trang mô phỏng đơn giản sang **khung quản trị dữ liệu báo cáo thực tế**.

### 1. Hồ sơ nghĩa trang 360°
Mỗi nghĩa trang có thể quản lý theo 6 nhóm:
1. Định danh – địa điểm.
2. Chủ thể quản lý – trạng thái.
3. Quỹ đất – công suất.
4. Quy hoạch – đất đai – môi trường – hạ tầng kỹ thuật.
5. Đầu tư – kiến nghị.
6. Nguồn báo cáo – trạng thái xác minh – lịch sử cập nhật.

### 2. Nạp báo cáo nghĩa trang đang có
Trang **Nạp báo cáo nghĩa trang** cho phép:
- đọc CSV/XLSX;
- chọn sheet cần đọc;
- xem nguyên dữ liệu nguồn;
- ghép các cột của báo cáo vào bộ trường chuẩn;
- tạo mã tạm khi báo cáo chưa có mã tài sản;
- phát hiện lỗi/cảnh báo dữ liệu;
- tải ra bản chuẩn hóa chờ cán bộ xác minh.

Hệ thống **không tự ghi đè** vào kho dữ liệu chính thức.

### 3. Bộ kiểm tra dữ liệu nghĩa trang
Ví dụ các kiểm tra đã có:
- thiếu tên nghĩa trang hoặc mã nguồn;
- diện tích đã sử dụng lớn hơn tổng diện tích;
- diện tích còn lại không khớp với tổng trừ đã sử dụng;
- trùng mã;
- mã tài sản tạm;
- tín hiệu quỹ đất còn lại thấp để cán bộ ưu tiên rà soát.

Tín hiệu quản lý **không phải kết luận pháp lý**.

### 4. Biểu mẫu Excel chuyên ngành
`templates/DakCemetery_Bieu_mau_du_lieu_v0.3.xlsx` gồm 7 sheet:
1. Danh mục nghĩa trang.
2. Quy hoạch – đất đai – quỹ đất.
3. Công suất – khả năng đáp ứng.
4. Hạ tầng kỹ thuật – môi trường.
5. Đầu tư – kiến nghị.
6. Nguồn báo cáo – hồ sơ.
7. Hướng dẫn.

## Nguyên tắc quản trị
- AI và Rule Engine chỉ hỗ trợ tổng hợp, cảnh báo, checklist và đề xuất.
- Không thay thế thẩm quyền của cơ quan nhà nước hoặc người có thẩm quyền.
- Không tự động coi dự thảo, đề án hoặc tài liệu tham khảo là quy định có hiệu lực.
- Giữ dữ liệu nguồn, không ghi đè lịch sử; dữ liệu mâu thuẫn phải được gắn cờ.
- Không nhập thông tin cá nhân người đã mất trong MVP v0.3.
- Dữ liệu báo cáo thực chỉ được đưa vào kho chính thức sau khi xác minh nguồn và trách nhiệm cập nhật.

## Chạy thử
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Kiểm thử
```bash
python tests/smoke_data.py
python tests/test_registry_v02.py
python tests/test_rules_v02.py
python tests/test_import_v02.py
python tests/test_cemetery_v03.py
```

## Cấu trúc mới
```text
streamlit_app.py
core/
  cemetery_service.py       # chuẩn hóa, mapping, KPI, kiểm tra dữ liệu nghĩa trang
pages/
  dakcemetery.py            # dashboard + hồ sơ nhanh
  cemetery_import.py        # nạp báo cáo nghĩa trang
config/
data/
  cemetery_master.csv       # dữ liệu mẫu mở rộng
  cemetery_raw/             # chỗ lưu bản sao làm việc khi thử nghiệm cục bộ
templates/
  DakCemetery_Bieu_mau_du_lieu_v0.3.xlsx
docs/
  DAKCEMETERY_DATA_STANDARD_v0.3.md
  NEXT_V0.4.md
legacy_dakroad/             # giữ mốc DakRoad AI v0.6.3
```

## Việc tiếp theo ngay khi có báo cáo thực tế
1. Đọc từng báo cáo và giữ nguyên cấu trúc nguồn.
2. Xác định cột nào tương ứng với trường dữ liệu chuẩn.
3. Gắn `source_id` cho từng báo cáo/hồ sơ.
4. Tách dữ liệu nguồn, dữ liệu chuẩn hóa và dữ liệu đã xác minh.
5. Chỉ sau đó mới cập nhật dashboard cấp Phòng/Sở.

## Tác giả/nguồn phát triển
DakTech Infra AI được phát triển tiếp từ sản phẩm **DakRoad AI** của tác giả **Lê Xuân Sơn – Sở Xây dựng tỉnh Đắk Lắk**.
