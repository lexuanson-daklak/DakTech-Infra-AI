# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
Phiên bản: **MVP v0.4**

DakTech Infra AI là nền tảng mẹ phát triển từ tư duy và kiến trúc của **DakRoad AI**. Mục tiêu là dùng một lõi chung để quản trị nhiều lĩnh vực hạ tầng kỹ thuật, thay vì tạo nhiều phần mềm rời rạc.

## Bản GitHub Public

Gói này dùng cho website demo công khai. Không chứa tệp báo cáo gốc, không chứa bộ dữ liệu chi tiết 303 bản ghi và đã ẩn tên đơn vị báo cáo trong bảng kiểm kê nguồn. Dữ liệu làm việc chi tiết phải lưu nội bộ, không đưa lên repository Public.

## Các phân hệ
- 🛣️ **DakRoad AI** – kết cấu hạ tầng đường bộ; phân hệ khởi nguồn và tiếp tục giữ thương hiệu riêng.
- ⚱️ **DakCemetery AI** – nghĩa trang và cơ sở hỏa táng.
- 💧 **DakWater AI** – cấp nước sạch.
- 🌧️ **DakDrain AI** – thoát nước và xử lý nước thải.

## Trọng tâm MVP v0.4: đưa báo cáo nghĩa trang thực tế vào quy trình quản trị dữ liệu

Tác giả đã thu thập **03 tệp RAR với 36 gói hồ sơ**. MVP v0.4 không coi toàn bộ các gói này là một cơ sở dữ liệu chính thức mà phân loại theo loại nguồn, trạng thái sử dụng và mức độ xác minh.

Kết quả sơ bộ của lớp dữ liệu làm việc:
- 36 gói hồ sơ đã tiếp nhận;
- 30 báo cáo hiện trạng cấp xã/phường;
- 01 báo cáo đã xin hủy và bị loại khỏi lớp dữ liệu chính thức;
- các nguồn riêng về triển khai quy định, quy hoạch/mở rộng, đóng cửa, vận hành và bối cảnh KKT;
- 303 bản ghi chi tiết đã tách sơ bộ từ 32 nguồn;
- 56 bản ghi có cờ chất lượng cần đối chiếu;
- riêng Cư Pui có 15 khu mai táng được báo cáo ở mức tổng hợp, chưa tách đủ từng dòng chi tiết.

> Các con số trên là **kết quả kiểm kê nguồn và dữ liệu dẫn xuất**, không phải tổng số nghĩa trang chính thức của toàn tỉnh.

## Chức năng mới v0.4

### 1. Kho báo cáo nghĩa trang
Trang **Kho báo cáo nghĩa trang** hiển thị:
- mức độ thu thập hồ sơ;
- loại nguồn và trạng thái sử dụng;
- số bản ghi đã tách;
- số bản ghi có cờ chất lượng;
- trạng thái xác minh;
- các nguồn phải xử lý riêng.

### 2. Tách dữ liệu công khai và dữ liệu làm việc nội bộ
Repository công khai **không chứa 03 tệp RAR, PDF/DOC/XLSX gốc hoặc bộ dữ liệu chi tiết dẫn xuất**. Kho công khai chỉ chứa số liệu tổng hợp an toàn để kiểm chứng giao diện.

Bộ dữ liệu chi tiết dẫn xuất được đóng gói riêng thành **DakCemetery-Local-DataPack-v0.4** và có cảnh báo không tải lên GitHub Public trước khi rà soát/phê duyệt.

### 3. Hồ sơ nghĩa trang 360°
Mỗi nghĩa trang được định hướng quản lý theo 6 nhóm:
1. Định danh – địa điểm.
2. Chủ thể quản lý – trạng thái.
3. Quỹ đất – công suất.
4. Quy hoạch – đất đai – môi trường – hạ tầng kỹ thuật.
5. Đầu tư – kiến nghị.
6. Nguồn báo cáo – trạng thái xác minh – lịch sử cập nhật.

### 4. Nạp báo cáo nghĩa trang
Trang **Nạp báo cáo nghĩa trang** cho phép đọc CSV/XLSX, ghép cột, tạo mã tạm, kiểm tra dữ liệu và xuất bản chờ xác minh. Hệ thống không tự ghi đè vào kho dữ liệu chính thức.

## Nguyên tắc quản trị
- AI và Bộ kiểm tra quy tắc chỉ hỗ trợ tổng hợp, cảnh báo, checklist và đề xuất.
- Không thay thế thẩm quyền của cơ quan nhà nước hoặc người có thẩm quyền.
- Giữ dữ liệu nguồn, không ghi đè lịch sử; dữ liệu mâu thuẫn/bất thường phải được gắn cờ.
- Không tự sửa số liệu bất thường (ví dụ đơn vị/diện tích chưa rõ) nếu nguồn không đủ căn cứ.
- Không cộng dữ liệu thành tổng số toàn tỉnh khi phạm vi báo cáo chưa đầy đủ.
- Dữ liệu thực chỉ chuyển sang lớp điều hành sau khi xác minh nguồn và trách nhiệm cập nhật.
- Không đưa dữ liệu nội bộ hoặc chưa được phép công khai lên GitHub Public.

## Chạy thử
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
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

## Cấu trúc chính
```text
streamlit_app.py
core/
pages/
  dakcemetery.py
  cemetery_sources.py       # kiểm kê 36 gói báo cáo + chất lượng nguồn
  cemetery_import.py
data/
  cemetery_collection_overview_v0.4.csv
  cemetery_collection_status_v0.4.csv
templates/
docs/
legacy_dakroad/              # giữ mốc DakRoad AI v0.6.3
```

## Tác giả/nguồn phát triển
DakTech Infra AI được phát triển tiếp từ sản phẩm **DakRoad AI** của tác giả **Lê Xuân Sơn – Sở Xây dựng tỉnh Đắk Lắk**.
