# DakTech Infra AI

**AI quản trị hạ tầng kỹ thuật Đắk Lắk**  
**Phiên bản: MVP v0.5**

DakTech Infra AI là nền tảng mẹ phát triển từ tư duy và kiến trúc của **DakRoad AI**. MVP v0.5 tập trung sâu vào **DakCemetery AI – quản lý nghĩa trang**.

## Trọng tâm v0.5: từ báo cáo đến danh mục nghĩa trang có kiểm soát

Dữ liệu đã thu thập gồm 03 tệp RAR với 36 gói hồ sơ. Lớp làm việc nội bộ đã tách sơ bộ 303 bản ghi từ 32 nguồn. Hệ thống **không coi 303 bản ghi là 303 nghĩa trang chính thức**.

v0.5 tổ chức ba lớp:

1. **Hồ sơ nguồn** – giữ nguyên báo cáo, quyết định, hồ sơ quy hoạch/mở rộng và nguồn khác.
2. **Danh mục ứng viên chưa xác minh** – dữ liệu tách từ báo cáo, có khóa kỹ thuật và cờ chất lượng.
3. **Danh mục quản lý chính thức** – chỉ hình thành sau khi cán bộ đối chiếu nguồn, xác định đối tượng, cấp mã và xác minh.

## Chức năng mới

- **Dashboard nghĩa trang**: tiến độ hình thành danh mục, trạng thái nguồn, hàng đợi làm sạch.
- **Danh mục nghĩa trang**: tách rõ dữ liệu chính thức / ứng viên / dữ liệu mẫu.
- **Bản đồ nghĩa trang**: chỉ đưa dữ liệu thật lên khi có tọa độ và đã xác minh; hiện dùng bản đồ mẫu để kiểm chứng giao diện.
- **Kho báo cáo nghĩa trang**: theo dõi 36 gói hồ sơ, 303 bản ghi dẫn xuất và tình trạng xác minh.
- **Phát hiện khả năng trùng**: dùng khóa kỹ thuật tên + địa bàn, nhưng **không tự động gộp**.
- **Bộ kiểm tra quy tắc dữ liệu**: dùng thuật ngữ tiếng Việt trên giao diện; quy tắc pháp lý chuyên ngành vẫn khóa.

## Bản vá giao diện v0.5.1

- Việt hóa bảng **Tài sản đang cần theo dõi**.
- Chuẩn hóa nhãn trạng thái hiển thị cho người dùng.
- Đưa bản đồ điều hành về góc nhìn mặc định tập trung vào phạm vi Đắk Lắk sau sắp xếp địa giới.
- Thay tham số Streamlit `use_container_width` đã bị cảnh báo bằng `width="stretch"` trong phần mã đang vận hành.
- Chưa thay đổi dữ liệu nghĩa trang, chưa xác minh thêm bản ghi nào và chưa đưa dữ liệu nội bộ lên GitHub Public.

## Bản GitHub Public

Gói này **không chứa**:
- 03 tệp RAR báo cáo gốc;
- danh sách chi tiết 303 bản ghi;
- tên/địa bàn chi tiết của lớp dữ liệu dẫn xuất nội bộ;
- chức năng nạp dữ liệu nội bộ thật lên website demo.

Dữ liệu chi tiết được đóng gói riêng trong **DakCemetery Local DataPack v0.5** và không được đưa lên GitHub Public trước khi rà soát/cho phép.

## Tác giả/nguồn phát triển

DakTech Infra AI được phát triển tiếp từ sản phẩm **DakRoad AI** của tác giả **Lê Xuân Sơn – Sở Xây dựng tỉnh Đắk Lắk**.
