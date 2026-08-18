# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
**Phiên bản: MVP v0.6.1**

DakTech Infra AI là **nền tảng mẹ**, phát triển từ tư duy và kiến trúc của **DakRoad AI**.  
MVP v0.6.x tập trung sâu vào **DakCemetery AI (Quản lý nghĩa trang)** và đồng thời chuẩn hóa cách nhìn cấu trúc GitHub + Streamlit.

## 1. Cây sản phẩm

```text
DakTech Infra AI
│
├── DakCemetery AI (Quản lý nghĩa trang)
├── DakRoad AI (Quản lý kết cấu hạ tầng đường bộ)
├── DakWater AI (Quản lý cấp nước sạch)
└── DakDrain AI (Quản lý thoát nước và xử lý nước thải)
```

## 2. Cây thư mục GitHub

```text
DakTech-Infra-AI/
│
├── modules/
│   ├── dakcemetery-ai/     (Quản lý nghĩa trang)
│   ├── dakroad-ai/         (Quản lý kết cấu hạ tầng đường bộ)
│   ├── dakwater-ai/        (Quản lý cấp nước sạch)
│   └── dakdrain-ai/        (Quản lý thoát nước và xử lý nước thải)
│
├── pages/                  Các màn hình Streamlit
├── core/                   Lõi xử lý dùng chung
├── data/                   Dữ liệu demo/an toàn công khai
├── config/                 Cấu hình
├── docs/                   Tài liệu kiến trúc, hướng dẫn
├── templates/              Biểu mẫu
├── tests/                  Kiểm thử
├── legacy_dakroad/         Thành phần kế thừa DakRoad AI
├── streamlit_app.py        Điểm khởi động Streamlit
├── requirements.txt        Thư viện Python
└── README.md               Trang giới thiệu chính
```

## 3. Nhiều chế độ xem trên Streamlit

Trong menu **Điều hành → Cấu trúc hệ thống**, có 6 chế độ xem:

1. **Tổng quan hệ sinh thái** – nền tảng mẹ và 4 phân hệ.
2. **Cây sản phẩm** – nhìn theo chức năng quản lý.
3. **Cây thư mục GitHub** – nhìn theo nơi lưu mã.
4. **GitHub ↔ Streamlit** – biết file nào tạo ra màn hình nào.
5. **Luồng dữ liệu nghiệp vụ** – từ hồ sơ nguồn đến danh mục chính thức.
6. **Trạng thái các phân hệ** – biết phân hệ nào đang phát triển đến đâu.

## 4. Trọng tâm DakCemetery AI – MVP v0.6

Dữ liệu làm việc nội bộ hiện có **303 bản ghi dẫn xuất từ 32 nguồn**. Hệ thống **không coi 303 dòng là 303 nghĩa trang chính thức**.

Chuỗi xử lý:

**Hồ sơ nguồn → Danh mục ứng viên → Chuẩn hóa → Kiểm tra → P1/P2/P3 → Cán bộ xác minh → Danh mục chính thức → Bản đồ/Dashboard**

## 5. Nguyên tắc an toàn dữ liệu

- GitHub Public chỉ chứa mã nguồn và số liệu tổng hợp/dữ liệu demo an toàn.
- Không đưa báo cáo gốc, dữ liệu chi tiết nội bộ hoặc dữ liệu nhạy cảm lên GitHub Public.
- AI và bộ quy tắc chỉ hỗ trợ; không thay thế kết luận chuyên môn hoặc quyết định của cơ quan nhà nước.

## 6. Ghi chú tên tiếng Anh

- `dakcemetery-ai` (**Quản lý nghĩa trang**)
- `dakroad-ai` (**Quản lý kết cấu hạ tầng đường bộ**)
- `dakwater-ai` (**Quản lý cấp nước sạch**)
- `dakdrain-ai` (**Quản lý thoát nước và xử lý nước thải**)

Tên thư mục kỹ thuật được giữ ngắn gọn, không dấu để đường dẫn ổn định; nghĩa tiếng Việt luôn được ghi trong tài liệu và giao diện.
