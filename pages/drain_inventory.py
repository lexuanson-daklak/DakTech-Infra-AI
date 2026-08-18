import streamlit as st
from core.data import load_assets

st.title("📋 DakDrain AI – Danh mục thoát nước và nước thải")
st.caption("Danh mục đang hiển thị dữ liệu mẫu để kiểm chứng cấu trúc. Chưa phải danh mục chính thức.")

df = load_assets("drain").copy()

c1, c2, c3 = st.columns(3)
with c1:
    types = ["Tất cả"] + sorted([str(x) for x in df["asset_type"].dropna().unique()])
    atype = st.selectbox("Loại đối tượng", types)
with c2:
    basins = ["Tất cả"] + sorted([str(x) for x in df["basin"].dropna().unique()])
    basin = st.selectbox("Lưu vực", basins)
with c3:
    statuses = ["Tất cả"] + sorted([str(x) for x in df["status"].dropna().unique()])
    status = st.selectbox("Trạng thái", statuses)

f = df.copy()
if atype != "Tất cả":
    f = f[f["asset_type"].astype(str) == atype]
if basin != "Tất cả":
    f = f[f["basin"].astype(str) == basin]
if status != "Tất cả":
    f = f[f["status"].astype(str) == status]

show = f[[
    "asset_code","asset_name","asset_type","locality","basin","capacity_note",
    "management_unit","status","investment_need"
]].copy()
show = show.rename(columns={
    "asset_code":"Mã tài sản","asset_name":"Tên đối tượng","asset_type":"Loại đối tượng",
    "locality":"Địa bàn","basin":"Lưu vực","capacity_note":"Quy mô/công suất ghi chú",
    "management_unit":"Đơn vị quản lý","status":"Trạng thái","investment_need":"Nhu cầu đầu tư/kiến nghị"
})
show["Loại đối tượng"] = show["Loại đối tượng"].replace({
    "SEWER":"Tuyến cống","FLOOD_POINT":"Điểm ngập","PUMP_STATION":"Trạm bơm",
    "WWTP":"Nhà máy xử lý nước thải","OUTFALL":"Điểm xả"
})
show["Trạng thái"] = show["Trạng thái"].replace({
    "ACTIVE":"Đang hoạt động","REVIEW":"Cần rà soát","RESTRICTED":"Hạn chế",
    "LIMITED":"Giới hạn","CLOSED":"Đã đóng","PLANNED":"Quy hoạch/dự kiến","INACTIVE":"Không hoạt động"
})

st.metric("Số bản ghi đang hiển thị", len(show))
st.dataframe(show, width="stretch", hide_index=True)
st.warning("Không dùng bảng demo này làm căn cứ báo cáo. Dữ liệu thật phải truy vết về hồ sơ nguồn và qua xác minh.")
