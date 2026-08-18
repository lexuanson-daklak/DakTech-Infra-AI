import streamlit as st
from core.data import load_assets

st.title("📋 DakWater AI – Danh mục công trình cấp nước")
st.caption("Danh mục đang hiển thị dữ liệu mẫu để kiểm chứng cấu trúc. Chưa phải danh mục chính thức.")

df = load_assets("water").copy()

c1, c2, c3 = st.columns(3)
with c1:
    localities = ["Tất cả"] + sorted([str(x) for x in df["locality"].dropna().unique()])
    locality = st.selectbox("Địa bàn", localities)
with c2:
    sources = ["Tất cả"] + sorted([str(x) for x in df["source_type"].dropna().unique()])
    source = st.selectbox("Loại nguồn", sources)
with c3:
    statuses = ["Tất cả"] + sorted([str(x) for x in df["status"].dropna().unique()])
    status = st.selectbox("Trạng thái", statuses)

f = df.copy()
if locality != "Tất cả":
    f = f[f["locality"].astype(str) == locality]
if source != "Tất cả":
    f = f[f["source_type"].astype(str) == source]
if status != "Tất cả":
    f = f[f["status"].astype(str) == status]

show = f[[
    "asset_code","asset_name","locality","source_type","design_capacity_m3d",
    "current_capacity_m3d","served_population","management_unit","status","investment_need"
]].copy()
show = show.rename(columns={
    "asset_code":"Mã tài sản","asset_name":"Tên công trình","locality":"Địa bàn",
    "source_type":"Loại nguồn","design_capacity_m3d":"Công suất thiết kế (m³/ngđ)",
    "current_capacity_m3d":"Công suất khai thác (m³/ngđ)","served_population":"Dân số phục vụ",
    "management_unit":"Đơn vị quản lý","status":"Trạng thái","investment_need":"Nhu cầu đầu tư/kiến nghị"
})
show["Trạng thái"] = show["Trạng thái"].replace({
    "ACTIVE":"Đang hoạt động","REVIEW":"Cần rà soát","RESTRICTED":"Hạn chế",
    "LIMITED":"Giới hạn","CLOSED":"Đã đóng","PLANNED":"Quy hoạch/dự kiến","INACTIVE":"Không hoạt động"
})

st.metric("Số bản ghi đang hiển thị", len(show))
st.dataframe(show, width="stretch", hide_index=True)
st.warning("Không dùng bảng demo này làm căn cứ báo cáo. Khi có hồ sơ thật sẽ nạp vào lớp dữ liệu nội bộ và xác minh theo nguồn.")
