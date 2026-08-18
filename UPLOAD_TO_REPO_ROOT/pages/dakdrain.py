import streamlit as st
from core.data import load_assets
from core.ui import kpi_row, point_map, status_table

st.title("🌧️ DakDrain AI")
st.caption("MVP quản trị thoát nước và xử lý nước thải: tuyến cống, điểm ngập, trạm bơm, nhà máy xử lý và tình trạng vận hành.")
df = load_assets("drain")

kpi_row([
    ("Tài sản/điểm mẫu", len(df), "Tổng bản ghi mẫu"),
    ("Điểm ngập", int((df.asset_type == "FLOOD_POINT").sum()), "Điểm ngập cần theo dõi"),
    ("Tuyến cống", int((df.asset_type == "SEWER").sum()), "Tuyến cống mẫu"),
    ("Cần chú ý", int((df.status != "ACTIVE").sum()), "Bản ghi không ở trạng thái ACTIVE"),
])

point_map(df, ["asset_code", "asset_name", "asset_type", "basin", "status"], zoom=7.2)

st.subheader("Danh mục thoát nước")
status_table(df, ["asset_code", "asset_name", "asset_type", "locality", "basin", "capacity_note", "management_unit", "status", "investment_need"])

st.info("Định hướng dữ liệu: lưu vực → tuyến cống → hố ga → trạm bơm → nhà máy xử lý nước thải → điểm xả; điểm ngập được liên kết ngược về lưu vực và công trình xử lý.")
