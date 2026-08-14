import pandas as pd
import streamlit as st

st.title("🧭 Lộ trình triển khai DakTech Infra AI")
st.caption("Đi từ bản thử nghiệm chạy được → quản trị dữ liệu thực → thí điểm nội bộ → hệ thống chính thức.")

plan = pd.DataFrame([
    ["Đã làm", "MVP v0.1", "Khung nền tảng mẹ + 4 phân hệ", "Chứng minh kiến trúc đa phân hệ"],
    ["Đã làm", "MVP v0.2", "Danh mục tài sản dùng chung + hồ sơ 360° + nhập dữ liệu", "Chuẩn hóa lõi quản trị"],
    ["Đã làm", "MVP v0.3", "DakCemetery AI + biểu mẫu chuyên ngành", "Kiểm chứng cấu trúc nghĩa trang"],
    ["Đã làm", "MVP v0.4", "Kho 36 gói báo cáo + lớp dữ liệu dẫn xuất", "Quản trị nguồn và chất lượng"],
    ["Đang làm", "MVP v0.5", "Danh mục nghĩa trang ứng viên + rà soát trùng + dashboard nghĩa trang", "Chuẩn bị lớp dữ liệu chính thức"],
    ["Tiếp theo", "MVP v0.6", "Xác minh một số nghĩa trang + tọa độ + hồ sơ 360° thực", "Thí điểm nội bộ phạm vi nhỏ"],
    ["Sau thí điểm", "v1.0", "CSDL tập trung, phân quyền, nhật ký, sao lưu, quy chế vận hành", "Hệ thống đủ điều kiện vận hành theo quyết định/đề án"],
], columns=["Trạng thái", "Mốc", "Công việc", "Kết quả cần đạt"])
st.dataframe(plan, use_container_width=True, hide_index=True)

st.markdown("### Việc ưu tiên sau v0.5")
st.markdown(
    "1. Rà soát 20 nhóm có khả năng trùng khóa kỹ thuật; không tự động gộp.\n"
    "2. Bổ sung đơn vị quản lý và diện tích còn thiếu.\n"
    "3. Xử lý các số liệu diện tích có cờ bất thường.\n"
    "4. Chọn một số nghĩa trang có hồ sơ rõ để xác minh thí điểm và cấp mã chính thức.\n"
    "5. Chỉ khi có tọa độ đáng tin cậy mới đưa dữ liệu thật lên bản đồ.\n"
    "6. Dữ liệu nội bộ không đưa lên GitHub Public/website demo công khai."
)

st.success("Nhà nước quyết định dữ liệu nào là chính thức và ai chịu trách nhiệm cập nhật; phần mềm chỉ hỗ trợ chuẩn hóa, cảnh báo, truy vết và điều hành.")
