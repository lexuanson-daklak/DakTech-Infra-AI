# QUY CHUẨN BẮT BUỘC – TRUNG TÂM XUẤT DỮ LIỆU
## Áp dụng cho toàn bộ hệ sinh thái GitHub + Streamlit

**Mã quy chuẩn:** DATA-EXPORT-STANDARD-v1.0  
**Trạng thái:** BẮT BUỘC  
**Phạm vi:** Tất cả ứng dụng/phân hệ hiện có và phát triển mới.

## 1. Nguyên tắc nền tảng

GitHub là nơi quản lý mã nguồn, phiên bản và cấu trúc kỹ thuật.  
**GitHub không phải nơi buộc người dùng nghiệp vụ phải vào để lấy dữ liệu.**

Streamlit là cổng sử dụng nghiệp vụ. Mỗi ứng dụng phải có:

> **📤 Trung tâm xuất dữ liệu**

Mục tiêu: người dùng xem, lọc, khai thác và tải dữ liệu trực tiếp từ Streamlit.

## 2. Chức năng tối thiểu bắt buộc

Mỗi Trung tâm xuất dữ liệu phải có:

1. **Xem trước dữ liệu sẽ xuất.**
2. **Bộ lọc trước khi xuất.**
3. **CSV** – dữ liệu bảng, UTF-8.
4. **Excel (.xlsx)** – tối thiểu gồm dữ liệu + thông tin xuất + từ điển dữ liệu.
5. **JSON** – phục vụ trao đổi máy-máy.
6. **GeoJSON** – bắt buộc khi dữ liệu có tọa độ/không gian.
7. **FULL DATA PACKAGE (.zip)** – gói tổng hợp.
8. **Metadata** – thông tin về phân hệ, phiên bản, bộ lọc, thời điểm xuất, số dòng.
9. **Từ điển dữ liệu** – tên trường, nghĩa tiếng Việt, kiểu dữ liệu, ghi chú.
10. **Cảnh báo pháp lý/dữ liệu** – dữ liệu demo, ứng viên, đã xác minh hay chính thức.

## 3. FULL DATA PACKAGE bắt buộc chứa

- CSV cho từng bảng.
- JSON cho từng bảng.
- GeoJSON nếu có tọa độ.
- 01 Excel nhiều sheet.
- `manifest.json`.
- `data_dictionary.csv`.
- `README.txt`.

## 4. Hai chế độ xuất

### A. Dữ liệu đang xem
Xuất đúng dữ liệu sau khi người dùng đã lọc.

### B. Bộ dữ liệu đầy đủ theo quyền
Xuất toàn bộ dữ liệu mà tài khoản hiện tại được phép truy cập.

Không được vượt quyền truy cập chỉ vì chức năng tải xuống.

## 5. Quy tắc tên file

Mẫu:

`<module>_<dataset>_YYYYMMDD_HHMMSS.<ext>`

Ví dụ:

`dakwater-ai_cong_trinh_cap_nuoc_20260818_233000.xlsx`

## 6. An toàn và phân quyền

- Public chỉ được tải dữ liệu mẫu hoặc dữ liệu tổng hợp an toàn.
- Dữ liệu nội bộ phải đặt trong môi trường nội bộ có phân quyền.
- Không đưa dữ liệu cá nhân/nhạy cảm lên Public chỉ để phục vụ tải xuống.
- Nguồn dữ liệu, trạng thái xác minh và phiên bản phải được giữ kèm khi có.
- AI không tự nâng dữ liệu ứng viên thành dữ liệu chính thức.

## 7. Quy chuẩn giao diện

Trong menu của mỗi phân hệ phải có mục:

**📤 Trung tâm xuất dữ liệu**

Tên này dùng thống nhất toàn hệ sinh thái.

## 8. Kiến trúc dùng chung

Ưu tiên dùng một lõi xuất dữ liệu dùng chung:

`core/export_center.py`

Mỗi phân hệ chỉ cấu hình:
- bộ dữ liệu;
- bộ lọc;
- metadata;
- từ điển dữ liệu;
- quyền tải.

Không sao chép logic xuất dữ liệu tùy tiện giữa các ứng dụng.

## 9. Kiểm tra bắt buộc trước khi phát hành

Một phân hệ chưa đạt quy chuẩn nếu:
- không có Trung tâm xuất dữ liệu;
- chỉ tải được một định dạng;
- tải dữ liệu không theo bộ lọc;
- thiếu metadata/từ điển;
- tải vượt quyền;
- buộc người dùng vào GitHub để lấy dữ liệu nghiệp vụ.

## 10. Áp dụng

Quy chuẩn này áp dụng cho DakTech Infra AI và các phân hệ như:
- DakRoad AI;
- DakCemetery AI;
- DakWater AI;
- DakDrain AI;
- các phân hệ phát triển sau này.

Từ phiên bản chuẩn hóa tiếp theo, **Trung tâm xuất dữ liệu là điều kiện bắt buộc để một ứng dụng được coi là hoàn thiện chức năng khai thác dữ liệu.**
