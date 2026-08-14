import streamlit as st

from core.cemetery_v06_service import (
    load_v06_priority,
    load_v06_type_summary,
    load_v06_status_summary,
    load_v06_quality_summary,
    metric,
)
from core.ui import kpi_row

st.title("📊 Dashboard quản lý nghĩa trang")
st.caption(
    "MVP v0.6 bắt đầu xử lý 303 bản ghi dẫn xuất từ báo cáo thực tế. "
    "Các số dưới đây là dữ liệu làm việc CHƯA XÁC MINH, không phải tổng số nghĩa trang chính thức của tỉnh."
)

kpi_row([
    ("Bản ghi ứng viên", f"{int(metric('Bản ghi ứng viên từ báo cáo')):,}", "Dòng dữ liệu tách từ báo cáo; chưa phải số nghĩa trang chính thức"),
    ("Nhóm kỹ thuật tên + địa bàn", f"{int(metric('Nhóm kỹ thuật tên + địa bàn')):,}", "Nhóm rà soát; không tự động coi mỗi nhóm là một nghĩa trang"),
    ("Nhóm cùng tên cần đối chiếu", f"{int(metric('Nhóm cùng tên + cùng địa bàn có nhiều dòng')):,}", "Có nhiều dòng cùng tên + cùng địa bàn; không tự động gộp"),
    ("P1 – ưu tiên cao", f"{int(metric('Ưu tiên P1 - đối chiếu diện tích')):,}", "Có cờ diện tích cần đối chiếu với nguồn"),
    ("P3 – đủ trường để đối chiếu", f"{int(metric('P3 - đủ trường để cán bộ đối chiếu')):,}", "Đủ trường cơ bản để cán bộ kiểm tra; vẫn chưa xác minh"),
])

st.warning(
    "v0.6 thực hiện chuẩn hóa kỹ thuật và xếp hàng đợi kiểm tra. "
    "Hệ thống không tự sửa số liệu, không tự gộp các dòng cùng tên và không tự cấp mã nghĩa trang chính thức."
)

left, right = st.columns(2)
with left:
    st.markdown("### Mức ưu tiên rà soát")
    pri = load_v06_priority()
    if pri.empty:
        st.info("Chưa có dữ liệu tổng hợp.")
    else:
        view = pri.rename(columns={"muc_uu_tien":"Mức ưu tiên","so_ban_ghi":"Số bản ghi","dien_giai":"Diễn giải"})
        st.dataframe(view, width="stretch", hide_index=True)
        st.bar_chart(view.set_index("Mức ưu tiên")["Số bản ghi"])

with right:
    st.markdown("### Loại hình gợi ý từ đúng chữ trong tên nguồn")
    typ = load_v06_type_summary()
    if typ.empty:
        st.info("Chưa có dữ liệu tổng hợp.")
    else:
        view = typ.rename(columns={"loai_hinh_hien_thi_v06":"Loại hình gợi ý","do_tin_cay_loai_hinh_v06":"Độ tin cậy","so_ban_ghi":"Số bản ghi"})
        st.dataframe(view, width="stretch", hide_index=True)
        st.bar_chart(view.groupby("Loại hình gợi ý")["Số bản ghi"].sum())

st.markdown("### Chất lượng trường dữ liệu")
q = load_v06_quality_summary()
if not q.empty:
    st.dataframe(q.rename(columns={"chi_tieu":"Chỉ tiêu","so_ban_ghi":"Số bản ghi"}), width="stretch", hide_index=True)

st.markdown("### Trạng thái theo dữ liệu nguồn")
s = load_v06_status_summary()
if not s.empty:
    st.dataframe(s[["trang_thai_hien_thi","so_ban_ghi"]].rename(columns={"trang_thai_hien_thi":"Trạng thái theo nguồn","so_ban_ghi":"Số bản ghi"}), width="stretch", hide_index=True)

st.markdown("### Quy trình chuyển sang danh mục quản lý chính thức")
st.markdown(
    "**Báo cáo gốc → bản ghi ứng viên → chuẩn hóa tên/địa bàn → nhóm cùng tên + cùng địa bàn → "
    "xếp P1/P2/P3 → cán bộ đối chiếu nguồn → kết luận cùng/khác đối tượng → xác minh loại hình, diện tích, đơn vị quản lý → "
    "cấp mã chính thức → mới đưa lên bản đồ và dashboard chính thức.**"
)
