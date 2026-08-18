import streamlit as st
import pandas as pd

from core.data import load_assets
from core.ui import kpi_row, point_map

st.title("💧 DakWater AI – Dashboard cấp nước")
st.caption("MVP v0.7: chuẩn hóa khung quản trị cấp nước sạch trước khi nạp dữ liệu thực tế.")

df = load_assets("water").copy()

design = pd.to_numeric(df.get("design_capacity_m3d"), errors="coerce").fillna(0).sum()
current = pd.to_numeric(df.get("current_capacity_m3d"), errors="coerce").fillna(0).sum()
util = (current / design * 100) if design else 0
attention = int((df.get("status") != "ACTIVE").sum()) if "status" in df.columns else 0

kpi_row([
    ("Công trình mẫu", len(df), "Dữ liệu hiện tại trong GitHub là dữ liệu mẫu/demo"),
    ("Công suất thiết kế mẫu", f"{design:,.0f} m³/ngđ", "Tổng từ dữ liệu mẫu hiện có"),
    ("Đang khai thác mẫu", f"{current:,.0f} m³/ngđ", "Tổng từ dữ liệu mẫu hiện có"),
    ("Tỷ lệ khai thác mẫu", f"{util:.1f}%", "Khai thác/thiết kế của dữ liệu mẫu"),
    ("Cần rà soát", attention, "Bản ghi mẫu không ở trạng thái ACTIVE"),
])

st.warning("Các chỉ tiêu trên hiện là dữ liệu MẪU, chưa phải số liệu cấp nước chính thức của tỉnh Đắk Lắk.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Theo loại nguồn")
    if "source_type" in df.columns and not df.empty:
        s = df.groupby("source_type", dropna=False).size().rename("Số công trình").reset_index()
        s.columns = ["Loại nguồn", "Số công trình"]
        st.dataframe(s, width="stretch", hide_index=True)
with c2:
    st.subheader("Theo trạng thái")
    if "status" in df.columns and not df.empty:
        s = df.groupby("status", dropna=False).size().rename("Số bản ghi").reset_index()
        s["status"] = s["status"].replace({
            "ACTIVE":"Đang hoạt động","REVIEW":"Cần rà soát","RESTRICTED":"Hạn chế",
            "LIMITED":"Giới hạn","CLOSED":"Đã đóng","PLANNED":"Quy hoạch/dự kiến","INACTIVE":"Không hoạt động"
        })
        s.columns = ["Trạng thái", "Số bản ghi"]
        st.dataframe(s, width="stretch", hide_index=True)

st.subheader("Bản đồ công trình cấp nước – dữ liệu mẫu")
point_map(df, ["asset_code","asset_name","source_type","design_capacity_m3d","current_capacity_m3d","status"], zoom=7.2)

st.info("Bước dữ liệu thực tế của DakWater AI sẽ theo chuỗi: nguồn nước → nhà máy/trạm → tuyến ống → vùng phục vụ → vận hành/chất lượng → đầu tư.")
