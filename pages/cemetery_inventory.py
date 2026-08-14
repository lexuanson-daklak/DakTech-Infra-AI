import streamlit as st

from core.cemetery_v06_service import metric, load_v06_progress
from core.cemetery_service import load_cemetery_master
from core.ui import status_table

st.title("📋 Danh mục nghĩa trang")
st.caption("MVP v0.6 quản lý ba lớp: hồ sơ nguồn → danh mục ứng viên chưa xác minh → danh mục chính thức.")

st.warning(
    "Bản GitHub Public không chứa tên/địa bàn chi tiết của 303 bản ghi dẫn xuất. "
    "Dữ liệu chi tiết v0.6 nằm trong Local DataPack nội bộ và bảng rà soát dành cho cán bộ."
)

tab1, tab2, tab3 = st.tabs(["Danh mục chính thức", "Danh mục ứng viên v0.6", "Dữ liệu mẫu giao diện"])

with tab1:
    st.metric("Bản ghi đã xác minh chính thức", int(metric("Đã xác minh chính thức")))
    st.info(
        "Hiện chưa có bản ghi nào được hệ thống tự chuyển vào danh mục chính thức. "
        "Cần cán bộ đối chiếu nguồn, xác định đúng đối tượng, loại hình, trạng thái, diện tích, đơn vị quản lý và cấp mã chính thức."
    )
    st.markdown("**Trường tối thiểu:** mã chính thức – tên chuẩn – địa bàn – loại hình – trạng thái – đơn vị quản lý – nguồn căn cứ – người/ngày xác minh.")

with tab2:
    a,b,c,d = st.columns(4)
    a.metric("Bản ghi ứng viên", int(metric("Bản ghi ứng viên từ báo cáo")))
    b.metric("Nhóm kỹ thuật", int(metric("Nhóm kỹ thuật tên + địa bàn")))
    c.metric("Nhóm cùng tên nhiều dòng", int(metric("Nhóm cùng tên + cùng địa bàn có nhiều dòng")))
    d.metric("Dòng trong nhóm cùng tên", int(metric("Bản ghi trong nhóm cùng tên + cùng địa bàn")))
    st.caption(
        "Nhóm kỹ thuật chỉ dùng để tổ chức rà soát. Nhiều dòng cùng tên có thể là nhiều thửa/bộ phận của một khu, "
        "các đối tượng riêng, hoặc bản ghi trùng; v0.6 không tự gộp."
    )
    progress = load_v06_progress()
    if not progress.empty:
        st.dataframe(progress.rename(columns={"chi_tieu":"Chỉ tiêu","gia_tri":"Giá trị","ghi_chu":"Ghi chú"}), width="stretch", hide_index=True)

with tab3:
    demo = load_cemetery_master()
    st.info("Dữ liệu bên dưới là dữ liệu mô phỏng để kiểm chứng giao diện, không phải dữ liệu nghĩa trang thực tế.")
    status_table(demo, [
        "asset_code", "asset_name", "locality", "cemetery_type", "total_area_ha", "remaining_area_ha",
        "management_unit", "status", "source_id", "verified_status"
    ])
