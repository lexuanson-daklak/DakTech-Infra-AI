import streamlit as st
import pandas as pd

from core.data import load_assets
from core.ui import kpi_row, point_map

st.title("🌧️ DakDrain AI – Dashboard thoát nước và nước thải")
st.caption("MVP v0.7: chuẩn hóa khung quản trị thoát nước, ngập và xử lý nước thải trước khi nạp dữ liệu thực tế.")

df = load_assets("drain").copy()
atype = df["asset_type"] if "asset_type" in df.columns else pd.Series(dtype=str)

kpi_row([
    ("Tài sản/điểm mẫu", len(df), "Dữ liệu mẫu/demo hiện có"),
    ("Tuyến cống mẫu", int((atype == "SEWER").sum()), "Tuyến cống trong dữ liệu mẫu"),
    ("Điểm ngập mẫu", int((atype == "FLOOD_POINT").sum()), "Điểm ngập trong dữ liệu mẫu"),
    ("Trạm bơm + XLNT mẫu", int(atype.isin(["PUMP_STATION","WWTP"]).sum()), "Công trình trong dữ liệu mẫu"),
    ("Cần rà soát", int((df["status"] != "ACTIVE").sum()) if "status" in df.columns else 0, "Bản ghi mẫu không ACTIVE"),
])

st.warning("Các chỉ tiêu trên hiện là dữ liệu MẪU, chưa phải số liệu thoát nước/nước thải chính thức của tỉnh Đắk Lắk.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Theo loại đối tượng")
    if "asset_type" in df.columns and not df.empty:
        s = df.groupby("asset_type").size().rename("Số bản ghi").reset_index()
        s["asset_type"] = s["asset_type"].replace({
            "SEWER":"Tuyến cống","FLOOD_POINT":"Điểm ngập","PUMP_STATION":"Trạm bơm",
            "WWTP":"Nhà máy xử lý nước thải","OUTFALL":"Điểm xả"
        })
        s.columns = ["Loại đối tượng","Số bản ghi"]
        st.dataframe(s, width="stretch", hide_index=True)
with c2:
    st.subheader("Theo lưu vực")
    if "basin" in df.columns and not df.empty:
        s = df.groupby("basin", dropna=False).size().rename("Số bản ghi").reset_index()
        s.columns = ["Lưu vực","Số bản ghi"]
        st.dataframe(s, width="stretch", hide_index=True)

st.subheader("Bản đồ thoát nước – dữ liệu mẫu")
point_map(df, ["asset_code","asset_name","asset_type","basin","status"], zoom=7.2)

st.info("Chuỗi quản trị định hướng: lưu vực → tuyến cống/hố ga → trạm bơm → nhà máy xử lý nước thải → điểm xả; điểm ngập liên kết ngược với lưu vực và mạng thoát nước.")
