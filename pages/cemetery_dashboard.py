import pandas as pd
import streamlit as st

from core.cemetery_inventory_service import (
    load_candidate_status,
    load_candidate_summary,
    load_candidate_type,
    metric_from_summary,
)
from core.ui import kpi_row

st.title("📊 Dashboard quản lý nghĩa trang")
st.caption("Tổng hợp tiến độ hình thành danh mục nghĩa trang từ các báo cáo đã thu thập. Số liệu dưới đây là lớp ứng viên CHƯA XÁC MINH, không phải tổng số nghĩa trang chính thức của tỉnh.")

kpi_row([
    ("Bản ghi ứng viên", f"{int(metric_from_summary('Bản ghi ứng viên chưa xác minh')):,}", "Bản ghi dẫn xuất từ báo cáo, chưa xác minh"),
    ("Khóa ứng viên khác nhau", f"{int(metric_from_summary('Khóa định danh ứng viên khác nhau')):,}", "Khóa kỹ thuật tên + địa bàn; không đồng nghĩa số nghĩa trang chính thức"),
    ("Nhóm cần rà soát trùng", f"{int(metric_from_summary('Nhóm có khả năng trùng cần rà soát')):,}", "Chỉ là tín hiệu trùng khóa kỹ thuật; không tự động gộp"),
    ("Thiếu đơn vị quản lý", f"{int(metric_from_summary('Bản ghi thiếu đơn vị quản lý')):,}", "Cần bổ sung hoặc xác minh từ nguồn"),
    ("Đã xác minh", f"{int(metric_from_summary('Bản ghi đã xác minh')):,}", "Chỉ bản ghi xác minh mới được chuyển sang lớp chính thức"),
])

st.warning(
    "MVP v0.5 tách rõ ba lớp: (1) hồ sơ nguồn, (2) danh mục ứng viên chưa xác minh, (3) danh mục quản lý chính thức. "
    "Hiện lớp (3) chưa tự động nhận bất kỳ bản ghi nào từ báo cáo."
)

left, right = st.columns(2)
with left:
    st.markdown("### Trạng thái theo dữ liệu nguồn")
    status = load_candidate_status()
    if status.empty:
        st.info("Chưa có dữ liệu tổng hợp trạng thái.")
    else:
        view = status[["trang_thai_hien_thi", "so_ban_ghi"]].rename(columns={"trang_thai_hien_thi":"Trạng thái", "so_ban_ghi":"Số bản ghi"})
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.bar_chart(view.set_index("Trạng thái"))

with right:
    st.markdown("### Phân loại sơ bộ theo chữ trong tên nguồn")
    typ = load_candidate_type()
    if typ.empty:
        st.info("Chưa có dữ liệu phân loại.")
    else:
        view = typ[["loai_hien_thi", "so_ban_ghi"]].rename(columns={"loai_hien_thi":"Tín hiệu loại hình", "so_ban_ghi":"Số bản ghi"})
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.bar_chart(view.set_index("Tín hiệu loại hình"))

st.markdown("### Hàng đợi làm sạch dữ liệu")
summary = load_candidate_summary()
if summary.empty:
    st.info("Chưa có dữ liệu tổng hợp.")
else:
    focus = summary[summary["chi_tieu"].isin([
        "Bản ghi nằm trong nhóm có khả năng trùng",
        "Bản ghi thiếu đơn vị quản lý",
        "Bản ghi thiếu diện tích",
        "Bản ghi có cờ AREA_VALUE_SUSPECT",
    ])].copy()
    focus = focus.rename(columns={"chi_tieu":"Việc cần rà soát", "gia_tri":"Số bản ghi", "ghi_chu":"Nguyên tắc xử lý"})
    st.dataframe(focus, use_container_width=True, hide_index=True)

st.markdown("### Quy trình chuyển thành danh mục chính thức")
st.markdown(
    "**Báo cáo gốc → Bản ghi ứng viên → Phát hiện khả năng trùng → Đối chiếu nguồn → Xác định cùng/khác đối tượng → "
    "Chuẩn hóa tên/địa bàn/loại hình → Cấp mã nghĩa trang chính thức → Xác minh → Đưa lên bản đồ và dashboard điều hành.**"
)
