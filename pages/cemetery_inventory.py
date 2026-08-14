import streamlit as st
import pandas as pd

from core.cemetery_inventory_service import load_candidate_summary, metric_from_summary
from core.cemetery_service import load_cemetery_master
from core.ui import status_table

st.title("📋 Danh mục nghĩa trang")
st.caption("Trang lõi của DakCemetery AI: phân biệt dữ liệu chính thức, dữ liệu ứng viên chưa xác minh và dữ liệu mẫu giao diện.")

st.warning(
    "Không hiển thị tên/địa bàn của 303 bản ghi dẫn xuất trên bản GitHub Public. "
    "Danh mục chi tiết chỉ được quản lý trong bộ dữ liệu nội bộ cho đến khi được rà soát và cho phép sử dụng."
)

tab1, tab2, tab3 = st.tabs(["Danh mục chính thức", "Danh mục ứng viên", "Dữ liệu mẫu giao diện"])

with tab1:
    st.metric("Số bản ghi đã xác minh để đưa vào danh mục chính thức", int(metric_from_summary("Bản ghi đã xác minh")))
    st.info(
        "Hiện chưa có bản ghi nào từ các báo cáo được hệ thống tự động coi là danh mục nghĩa trang chính thức. "
        "Đây là chủ ý kiểm soát: phải có bước cán bộ đối chiếu nguồn, xác định đối tượng và cấp mã chính thức."
    )
    st.markdown("**Trường tối thiểu khi một nghĩa trang được xác minh:** Mã chính thức – tên – xã/phường – loại hình – trạng thái – đơn vị quản lý – nguồn căn cứ – ngày xác minh.")

with tab2:
    summary = load_candidate_summary()
    st.metric("Bản ghi ứng viên chưa xác minh", int(metric_from_summary("Bản ghi ứng viên chưa xác minh")))
    st.metric("Khóa kỹ thuật tên + địa bàn khác nhau", int(metric_from_summary("Khóa định danh ứng viên khác nhau")))
    st.caption("Khóa kỹ thuật chỉ hỗ trợ rà soát; không được dùng để tự động kết luận số nghĩa trang thực tế.")
    if not summary.empty:
        st.dataframe(summary.rename(columns={"chi_tieu":"Chỉ tiêu", "gia_tri":"Giá trị", "ghi_chu":"Ghi chú"}), use_container_width=True, hide_index=True)

with tab3:
    demo = load_cemetery_master()
    st.info("8 bản ghi dưới đây là dữ liệu mô phỏng để kiểm chứng giao diện Hồ sơ 360° và bản đồ; không phải dữ liệu quản lý thực tế.")
    status_table(demo, [
        "asset_code", "asset_name", "locality", "cemetery_type", "total_area_ha", "remaining_area_ha",
        "management_unit", "status", "source_id", "verified_status"
    ])
