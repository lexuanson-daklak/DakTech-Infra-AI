import streamlit as st
from core.data import load_assets
from core.ui import kpi_row, point_map, status_table

st.title("🛣️ DakRoad AI")
st.caption("Phân hệ khởi nguồn – quản trị tài sản kết cấu hạ tầng đường bộ. Dữ liệu mẫu được kế thừa từ DakRoad AI v0.6.3.")
df = load_assets("road")

kpi_row([
    ("Tài sản mẫu", len(df), "Số tài sản đường bộ mẫu"),
    ("ACTIVE", int((df.status == "ACTIVE").sum()), "Đang hoạt động"),
    ("Diện tích khả dụng", f"{df.usable_area_m2.sum():,.0f} m²", "Tổng diện tích khả dụng mô phỏng"),
    ("Đơn vị quản lý", df.management_unit.nunique(), "Số đơn vị quản lý trong dữ liệu mẫu"),
])

left, right = st.columns([2, 1])
with left:
    st.subheader("Bản đồ tài sản")
    point_map(df, ["asset_code", "asset_name", "road_name", "status"], zoom=11)
with right:
    st.subheader("Tra cứu nhanh")
    code = st.selectbox("Chọn tài sản", df.asset_code.tolist())
    r = df[df.asset_code == code].iloc[0]
    st.write(f"**{r.asset_name}**")
    st.write(f"Tuyến: {r.road_name}")
    st.write(f"Diện tích khả dụng: {r.usable_area_m2:,.0f} m²")
    st.write(f"Trạng thái: `{r.status}`")

st.subheader("Danh mục tài sản")
status_table(df, ["asset_code", "asset_name", "road_name", "usable_area_m2", "management_unit", "status"])

st.info("Bản DakRoad AI v0.6.3 gốc được giữ riêng trong thư mục legacy_dakroad để không làm mất sản phẩm dự thi ban đầu.")
