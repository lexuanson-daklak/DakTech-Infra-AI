# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
**Phiên bản: MVP v0.6**

DakTech Infra AI là nền tảng mẹ phát triển từ tư duy và kiến trúc của **DakRoad AI**. MVP v0.6 tập trung sâu vào **DakCemetery AI – xử lý dữ liệu nghĩa trang thực tế**.

## Trọng tâm v0.6: từ 303 bản ghi dẫn xuất đến hàng đợi xác minh

Dữ liệu làm việc nội bộ hiện có **303 bản ghi dẫn xuất từ 32 nguồn**. v0.6 không coi các dòng này là 303 nghĩa trang chính thức.

Hệ thống tổ chức lại thành:

1. **Hồ sơ nguồn** – giữ nguyên báo cáo/quyết định/hồ sơ.
2. **Danh mục ứng viên** – 303 dòng được chuẩn hóa kỹ thuật và gắn cờ.
3. **Nhóm rà soát tên + địa bàn** – 267 nhóm kỹ thuật; 20 nhóm có nhiều dòng, tổng 56 dòng.
4. **Hàng đợi P1/P2/P3** – để cán bộ xử lý theo mức ưu tiên.
5. **Danh mục chính thức** – hiện bằng 0; chỉ hình thành sau xác minh của cán bộ.

## Kết quả xử lý v0.6

- 303 bản ghi ứng viên;
- 267 nhóm kỹ thuật tên + địa bàn;
- 20 nhóm cùng tên + cùng địa bàn có nhiều dòng, tổng 56 dòng;
- 21 dòng P1 cần đối chiếu cờ diện tích;
- 106 dòng P2 cần làm sạch/bổ sung;
- 176 dòng P3 đủ trường cơ bản để cán bộ đối chiếu nguồn;
- 24 dòng thiếu diện tích;
- 51 dòng thiếu đơn vị quản lý;
- 39 dòng chưa rõ loại hình;
- 10 dòng dùng ký hiệu `NT` cần xác minh;
- 0 dòng được hệ thống tự xác minh chính thức.

## Nguyên tắc kiểm soát

- Không tự sửa số liệu nguồn.
- Không tự động gộp các dòng cùng tên.
- Không suy diễn ký hiệu/loại hình ngoài nội dung nguồn.
- Không biến điểm đầy đủ dữ liệu thành kết luận pháp lý.
- Không đưa dữ liệu chi tiết nội bộ lên GitHub Public.
- Chỉ dữ liệu đã được cán bộ xác minh mới chuyển sang danh mục chính thức, bản đồ và dashboard quản lý.

## Bản GitHub Public

Kho Public chỉ chứa mã nguồn và **số liệu tổng hợp an toàn** để kiểm chứng giao diện. Tên/địa bàn chi tiết của 303 bản ghi, báo cáo gốc và bảng rà soát nội bộ được đóng gói riêng trong **DakCemetery Local DataPack v0.6**.

## Tác giả/nguồn phát triển

DakTech Infra AI được phát triển tiếp từ sản phẩm **DakRoad AI** của tác giả **Lê Xuân Sơn – Sở Xây dựng tỉnh Đắk Lắk**.
