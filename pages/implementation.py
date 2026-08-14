import pandas as pd
import streamlit as st

st.title("🧭 Lộ trình triển khai DakTech Infra AI")
st.caption("Mục tiêu: đi từ MVP chạy được → thí điểm nghiệp vụ → hệ thống chính thức; không nhập dữ liệu toàn tỉnh ngay từ đầu.")

plan = pd.DataFrame([
    ["Đã làm", "MVP v0.1", "Khung nền tảng mẹ + 4 phân hệ", "Chứng minh kiến trúc đa phân hệ", "Nhóm phát triển"],
    ["Đã làm", "MVP v0.2", "Asset Registry + hồ sơ 360° + import + Rule Engine dữ liệu", "Chuẩn hóa quản trị dữ liệu dùng chung", "Nhóm phát triển"],
    ["Tiếp theo", "MVP v0.3", "Chuẩn hóa bộ dữ liệu chuyên ngành + workflow", "Thí điểm một số tài sản thật đã được phép sử dụng", "Phòng PTHT + đơn vị quản lý"],
    ["Giai đoạn thí điểm", "Sau v0.3", "CSDL tập trung, phân quyền, audit, sao lưu", "Môi trường cơ quan/đơn vị đủ điều kiện", "Cơ quan có thẩm quyền + CNTT"],
    ["Mở rộng", "Sau thí điểm", "Kết nối hệ thống khác, dashboard cấp tỉnh", "Vận hành chính thức theo đề án/quy chế", "Các cơ quan, đơn vị liên quan"],
], columns=["Trạng thái", "Mốc", "Công việc", "Kết quả cần đạt", "Trách nhiệm chính"])
st.dataframe(plan, use_container_width=True, hide_index=True)

st.markdown("### Việc làm ngay sau v0.2")
st.markdown("""
1. Giữ nguyên **DakRoad AI v0.6.3** như mốc sản phẩm khởi nguồn.
2. Dùng **DakTech Infra AI** làm repository/nền tảng mẹ.
3. Chốt biểu mẫu dữ liệu với Phòng PTHT trước khi yêu cầu xã/phường hoặc đơn vị cập nhật.
4. Chọn một phạm vi nhỏ cho từng lĩnh vực để kiểm chứng: nghĩa trang, cấp nước, thoát nước.
5. Nạp pháp lý chuyên ngành theo Legal Version Control; chưa bật Rule Engine pháp lý nếu chưa rà soát.
6. Dữ liệu nội bộ/dữ liệu cá nhân không đưa lên GitHub công khai hoặc Streamlit Community Cloud khi chưa đáp ứng yêu cầu bảo mật.
""")

st.success("Nguyên tắc triển khai: Nhà nước xác định dữ liệu, tiêu chuẩn, quy trình và thẩm quyền; phần mềm hỗ trợ quản trị; đơn vị quản lý chịu trách nhiệm về dữ liệu do mình cung cấp.")
