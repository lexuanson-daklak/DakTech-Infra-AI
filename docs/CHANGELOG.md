# CHANGELOG

## MVP v0.4 – 14/08/2026
- Tiếp nhận 03 tệp RAR gồm 36 gói hồ sơ quản lý nghĩa trang do tác giả thu thập.
- Phân loại 30 báo cáo hiện trạng cấp xã/phường và các nguồn riêng: hủy văn bản, triển khai quy định, quy hoạch/mở rộng, đóng cửa, vận hành, KKT.
- Tách sơ bộ 303 bản ghi chi tiết từ 32 nguồn; 56 bản ghi có cờ chất lượng cần đối chiếu.
- Không đưa báo cáo gốc và dữ liệu chi tiết dẫn xuất lên GitHub Public.
- Bổ sung `cemetery_collection_overview_v0.4.csv` và `cemetery_collection_status_v0.4.csv` ở mức tổng hợp công khai.
- Bổ sung trang **Kho báo cáo nghĩa trang** để theo dõi nguồn, trạng thái xử lý và chất lượng dữ liệu.
- Việt hóa bảng tín hiệu điều hành và đổi KPI thành **Mức đầy đủ của dữ liệu mẫu** để tránh hiểu nhầm.
- Tăng cảnh báo bảo mật và nguyên tắc không tự sửa số liệu nguồn bất thường.

## MVP v0.2 – 14/08/2026
- Chuyển từ dữ liệu phân hệ rời sang Asset Registry dùng chung 36 tài sản mẫu.
- Bổ sung source_id, updated_at và record_hash.
- Bổ sung Hồ sơ tài sản 360°.
- Bổ sung import CSV/Excel + biểu mẫu Excel chuẩn.
- Bổ sung Rule Engine chất lượng dữ liệu; khóa Rule pháp lý chuyên ngành chưa được rà soát.
- Nâng trang tổng quan thành dashboard điều hành.
- Bổ sung các lớp pháp lý, quy hoạch, đầu tư, vận hành, bảo trì, sự cố và lịch sử.

## MVP v0.1
- Tạo nền tảng mẹ DakTech Infra AI.
- Tích hợp 4 phân hệ MVP: DakRoad, DakCemetery, DakWater, DakDrain.
- Giữ nguyên DakRoad AI v0.6.3 trong `legacy_dakroad/`.

## MVP v0.3 – 2026-08-14
- Tập trung phát triển sâu phân hệ DakCemetery AI.
- Bổ sung `cemetery_master.csv` và hồ sơ nghĩa trang 360°.
- Bổ sung trang nạp báo cáo nghĩa trang CSV/XLSX, chọn sheet và mapping cột.
- Bổ sung mã tài sản tạm, kiểm tra quỹ đất/diện tích, tín hiệu quản lý và trạng thái xác minh.
- Bổ sung biểu mẫu Excel 7 sheet cho dữ liệu nghĩa trang.
- Bổ sung tài liệu chuẩn dữ liệu và lộ trình v0.4.
