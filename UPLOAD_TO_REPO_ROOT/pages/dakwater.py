import streamlit as st
from core.data import load_assets
from core.ui import kpi_row, point_map, status_table

st.title("💧 DakWater AI")
st.caption("MVP quản trị cấp nước sạch: nhà máy, nguồn cấp, công suất, phạm vi phục vụ, tình trạng vận hành và nhu cầu đầu tư.")
df = load_assets("water")
util = (df.current_capacity_m3d.sum() / df.design_capacity_m3d.sum() * 100) if df.design_capacity_m3d.sum() else 0

kpi_row([
    ("Công trình mẫu", len(df), "Nhà máy/trạm cấp nước mẫu"),
    ("Công suất thiết kế", f"{df.design_capacity_m3d.sum():,.0f} m³/ngđ", "Tổng công suất thiết kế"),
    ("Đang khai thác", f"{df.current_capacity_m3d.sum():,.0f} m³/ngđ", "Tổng công suất hiện khai thác"),
    ("Tỷ lệ khai thác", f"{util:.1f}%", "Khai thác/thiết kế"),
])

point_map(df, ["asset_code", "asset_name", "design_capacity_m3d", "current_capacity_m3d", "status"], zoom=7.2)

st.subheader("Danh mục công trình cấp nước")
status_table(df, ["asset_code", "asset_name", "locality", "source_type", "design_capacity_m3d", "current_capacity_m3d", "served_population", "management_unit", "status", "investment_need"])

st.info("Bước sau của DakWater AI sẽ bổ sung tuyến ống, bể chứa và vùng cấp nước để hình thành chuỗi: nguồn nước → nhà máy → mạng lưới → vùng phục vụ.")
