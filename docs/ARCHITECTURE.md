# Kiến trúc DakTech Infra AI MVP v0.2

## 1. Nền tảng mẹ
DakTech Infra AI là lớp điều hướng và quản trị dùng chung.

## 2. Phân hệ
- DakRoad AI: kết cấu hạ tầng đường bộ.
- DakCemetery AI: nghĩa trang và cơ sở hỏa táng.
- DakWater AI: cấp nước sạch.
- DakDrain AI: thoát nước và xử lý nước thải.

## 3. Lõi dùng chung v0.2
```text
DakTech Infra AI
│
├── Asset Registry        → một mã tài sản dùng chung
├── Asset 360             → hồ sơ vòng đời tài sản
├── Data Import           → CSV/Excel + kiểm tra trước nhập
├── Data Quality Rules    → rule có mã, giải thích được
├── Legal Version Control → nguồn, hiệu lực, phạm vi, liên kết
├── GIS/Map               → vị trí tài sản
└── Executive Dashboard   → tín hiệu điều hành
```

## 4. Hồ sơ tài sản 360°
```text
Định danh → Vị trí → Pháp lý → Quy hoạch/đất đai → Đầu tư
        → Vận hành → Bảo trì → Sự cố → Lịch sử thay đổi
```

## 5. Kiến trúc kỹ thuật MVP
Streamlit + Python + pandas + PyDeck + CSV/Excel.

Giai đoạn thí điểm thực tế phải chuyển dữ liệu nghiệp vụ sang CSDL tập trung phù hợp, bổ sung phân quyền, audit, sao lưu và an toàn thông tin.
