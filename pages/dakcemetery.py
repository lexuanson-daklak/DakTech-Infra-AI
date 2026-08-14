import pandas as pd
import streamlit as st

from core.cemetery_service import cemetery_kpis, load_cemetery_master
from core.config import VERSION
from core.ui import kpi_row, point_map, show_key_value, status_table

st.title("⚱️ Hồ sơ nghĩa trang 360° – dữ liệu mẫu")
st.caption("Phân hệ quản trị nghĩa trang và cơ sở hỏa táng – tập trung vào tài sản, quỹ đất, công suất, quy hoạch, hạ tầng, đầu tư và nguồn dữ liệu.")

st.info(
    f"{VERSION} không quản lý thông tin cá nhân người đã mất trong bản Public. Trọng tâm là dữ liệu quản lý nhà nước về tài sản/hạ tầng. "
    "Các tín hiệu 'quỹ đất thấp' chỉ phục vụ rà soát, không phải kết luận pháp lý hoặc quyết định đóng/mở rộng nghĩa trang."
)

df = load_cemetery_master()

st.caption("Trang này chỉ dùng 8 bản ghi mô phỏng để kiểm chứng Hồ sơ 360°. Dữ liệu báo cáo thực tế được quản lý ở lớp ứng viên và chỉ chuyển sang danh mục chính thức sau xác minh.")

c1, c2, c3 = st.columns(3)
with c1:
    locality_options = ["Tất cả"] + sorted([x for x in df["locality"].dropna().astype(str).unique() if x.strip()])
    locality = st.selectbox("Địa phương", locality_options)
with c2:
    status_options = ["Tất cả"] + sorted([x for x in df["status"].dropna().astype(str).unique() if x.strip()])
    status = st.selectbox("Trạng thái", status_options)
with c3:
    signal_options = ["Tất cả"] + sorted([x for x in df["capacity_signal"].dropna().astype(str).unique() if x.strip()])
    signal = st.selectbox("Tín hiệu quỹ đất", signal_options)

view = df.copy()
if locality != "Tất cả":
    view = view[view["locality"] == locality]
if status != "Tất cả":
    view = view[view["status"] == status]
if signal != "Tất cả":
    view = view[view["capacity_signal"] == signal]

k = cemetery_kpis(view)
kpi_row([
    ("Số nghĩa trang", k["assets"], "Số bản ghi trong phạm vi lọc"),
    ("Tổng diện tích", f"{k['total_area_ha']:,.1f} ha", "Tổng diện tích theo dữ liệu nguồn"),
    ("Quỹ đất còn lại", f"{k['remaining_area_ha']:,.1f} ha", "Không tự suy diễn khi nguồn chưa có số liệu"),
    ("Quỹ đất thấp", k["low_land"], "Tín hiệu dưới 25% diện tích còn lại"),
    ("Đã xác minh", k["verified"], "Bản ghi được đánh dấu VERIFIED"),
])

st.markdown("### Bản đồ")
point_map(view, ["asset_code", "asset_name", "locality", "total_area_ha", "remaining_area_ha", "capacity_signal", "status"], zoom=7.1)

st.markdown("### Danh mục quản lý")
status_table(view, [
    "asset_code", "asset_name", "locality", "cemetery_type", "total_area_ha", "used_area_ha",
    "remaining_area_ha", "area_usage_pct", "capacity_signal", "management_unit", "planning_status",
    "land_status", "status", "priority", "investment_need", "source_id", "verified_status"
])

st.markdown("### Hồ sơ nhanh một nghĩa trang")
if view.empty:
    st.info("Không có bản ghi trong phạm vi lọc.")
else:
    options = view["asset_code"].astype(str) + " – " + view["asset_name"].astype(str)
    selected = st.selectbox("Chọn nghĩa trang", options.tolist())
    code = selected.split(" – ", 1)[0]
    record = view[view["asset_code"].astype(str) == code].iloc[0]

    left, right = st.columns(2)
    with left:
        st.markdown("#### 1. Định danh – quản lý")
        show_key_value(record, [
            ("asset_code", "Mã nghĩa trang"),
            ("asset_name", "Tên nghĩa trang"),
            ("locality", "Xã/phường"),
            ("address", "Địa điểm"),
            ("cemetery_type", "Loại hình"),
            ("management_unit", "Đơn vị quản lý"),
            ("management_model", "Mô hình quản lý"),
            ("status", "Trạng thái hoạt động"),
        ])

        st.markdown("#### 2. Quỹ đất – công suất")
        show_key_value(record, [
            ("total_area_ha", "Tổng diện tích (ha)"),
            ("used_area_ha", "Diện tích đã sử dụng (ha)"),
            ("remaining_area_ha", "Diện tích còn lại (ha)"),
            ("area_usage_pct", "Tỷ lệ diện tích đã sử dụng (%)"),
            ("planned_expansion_area_ha", "Diện tích dự kiến mở rộng (ha)"),
            ("remaining_graves", "Khả năng tiếp nhận còn lại (nếu có)"),
            ("annual_burials", "Số trường hợp/năm (nếu có)"),
            ("estimated_full_year", "Năm ước tính đầy theo số liệu hiện có"),
            ("capacity_signal", "Tín hiệu quỹ đất"),
        ])

    with right:
        st.markdown("#### 3. Quy hoạch – đất đai – môi trường")
        show_key_value(record, [
            ("planning_status", "Tình trạng quy hoạch"),
            ("land_status", "Tình trạng đất đai"),
            ("environmental_status", "Tình trạng môi trường"),
            ("internal_road_status", "Đường nội bộ"),
            ("drainage_status", "Thoát nước"),
            ("water_supply_status", "Cấp nước"),
            ("power_status", "Cấp điện"),
            ("greenery_status", "Cây xanh"),
        ])

        st.markdown("#### 4. Đầu tư – nguồn dữ liệu")
        show_key_value(record, [
            ("investment_need", "Nhu cầu/kiến nghị đầu tư"),
            ("priority", "Mức ưu tiên"),
            ("source_id", "Mã nguồn dữ liệu"),
            ("source_doc_no", "Số báo cáo/văn bản"),
            ("source_doc_date", "Ngày văn bản"),
            ("reporting_period", "Kỳ báo cáo"),
            ("verified_status", "Trạng thái xác minh"),
            ("updated_at", "Ngày cập nhật"),
        ])

st.markdown("### Cách dùng dữ liệu báo cáo thực tế")
st.markdown(
    "1. Nạp báo cáo gốc tại trang **Nạp báo cáo nghĩa trang**.\n"
    "2. Ghép các cột của báo cáo vào bộ trường chuẩn.\n"
    "3. Hệ thống chỉ chuẩn hóa và cảnh báo; không tự sửa nội dung báo cáo.\n"
    "4. Cán bộ xác minh nguồn và cấp mã tài sản chính thức trước khi nhập kho dữ liệu dùng chung."
)
