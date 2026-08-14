import streamlit as st
from core.cemetery_v06_service import load_v06_priority, load_v06_progress, metric
from core.ui import kpi_row

st.title("🧹 Hàng đợi rà soát dữ liệu nghĩa trang")
st.caption("Trang điều hành công việc làm sạch dữ liệu v0.6. Bản Public chỉ hiển thị số lượng tổng hợp, không hiển thị tên/địa bàn chi tiết.")

kpi_row([
    ("P1", int(metric("Ưu tiên P1 - đối chiếu diện tích")), "Đối chiếu cờ diện tích trước"),
    ("P2", int(metric("Ưu tiên P2 - cần làm sạch")), "Thiếu trường/chưa rõ loại hình/cùng tên nhiều dòng"),
    ("P3", int(metric("P3 - đủ trường để cán bộ đối chiếu")), "Đủ trường cơ bản để cán bộ kiểm tra nguồn"),
    ("Thiếu đơn vị quản lý", int(metric("Thiếu đơn vị quản lý")), "Cần bổ sung hoặc xác minh"),
    ("Chưa rõ loại hình", int(metric("Chưa rõ loại hình")), "Tên nguồn chưa nêu rõ loại hình"),
])

st.markdown("### Ý nghĩa P1 / P2 / P3")
st.markdown(
    "- **P1:** ưu tiên đối chiếu trước vì có cờ chất lượng diện tích từ lớp dữ liệu trước. Không tự sửa số liệu.\n"
    "- **P2:** cần làm sạch hoặc bổ sung trường trước khi chuyển sang bước xác minh.\n"
    "- **P3:** dữ liệu có đủ trường cơ bản để cán bộ mở báo cáo gốc và đối chiếu. **P3 không đồng nghĩa đã đúng hoặc đã được phê duyệt.**"
)

pri = load_v06_priority()
if not pri.empty:
    st.dataframe(pri.rename(columns={"muc_uu_tien":"Mức ưu tiên","so_ban_ghi":"Số bản ghi","dien_giai":"Diễn giải"}), width="stretch", hide_index=True)

st.markdown("### Quy tắc xử lý nhóm cùng tên + cùng địa bàn")
st.markdown(
    "1. Không tự gộp.\n"
    "2. Mở hồ sơ nguồn để xem các dòng có phải nhiều thửa/bộ phận của cùng một khu hay không.\n"
    "3. Nếu là các đối tượng riêng: giữ riêng và cấp mã riêng sau xác minh.\n"
    "4. Nếu là cùng một đối tượng gồm nhiều thành phần: ghi quan hệ thành phần–đối tượng, không xóa dữ liệu nguồn.\n"
    "5. Nếu đúng là bản ghi trùng: giữ lịch sử nguồn và đánh dấu bản ghi được hợp nhất bằng quyết định của người rà soát."
)

st.info("Danh sách chi tiết phục vụ rà soát nằm trong `DakCemetery-Local-DataPack-v0.6` và tệp Excel nội bộ; không đưa lên GitHub Public.")
