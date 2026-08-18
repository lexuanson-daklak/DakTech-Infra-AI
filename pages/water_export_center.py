import pandas as pd
import streamlit as st

from core.data import load_assets
from core.export_center import render_export_center

df = load_assets("water").copy()

status_vi = {
    "ACTIVE":"Đang hoạt động",
    "REVIEW":"Cần rà soát",
    "RESTRICTED":"Hạn chế",
    "LIMITED":"Giới hạn",
    "CLOSED":"Đã đóng",
    "PLANNED":"Quy hoạch/dự kiến",
    "INACTIVE":"Không hoạt động",
}

st.sidebar.subheader("Bộ lọc xuất dữ liệu")
localities = ["Tất cả"] + sorted(df["locality"].dropna().astype(str).unique().tolist())
sources = ["Tất cả"] + sorted(df["source_type"].dropna().astype(str).unique().tolist())
statuses = ["Tất cả"] + sorted(df["status"].dropna().astype(str).unique().tolist())

locality = st.sidebar.selectbox("Địa bàn", localities)
source = st.sidebar.selectbox("Loại nguồn", sources)
status = st.sidebar.selectbox("Trạng thái", statuses)

f = df.copy()
if locality != "Tất cả":
    f = f[f["locality"].astype(str) == locality]
if source != "Tất cả":
    f = f[f["source_type"].astype(str) == source]
if status != "Tất cả":
    f = f[f["status"].astype(str) == status]

display = f.copy()
if "status" in display.columns:
    display["status_vi"] = display["status"].map(status_vi).fillna(display["status"])

dictionary = pd.DataFrame([
    ["asset_code","Mã tài sản/công trình","Chuỗi","Định danh kỹ thuật"],
    ["asset_name","Tên công trình","Chuỗi","Tên theo dữ liệu đang quản lý"],
    ["locality","Địa bàn","Chuỗi","Địa danh/hành chính theo nguồn"],
    ["source_type","Loại nguồn nước","Chuỗi","Ví dụ: nước mặt, nước ngầm"],
    ["design_capacity_m3d","Công suất thiết kế","Số","m³/ngày đêm"],
    ["current_capacity_m3d","Công suất đang khai thác","Số","m³/ngày đêm"],
    ["served_population","Dân số phục vụ","Số","Người"],
    ["management_unit","Đơn vị quản lý/vận hành","Chuỗi","Theo hồ sơ nguồn"],
    ["status","Mã trạng thái","Chuỗi","Mã kỹ thuật"],
    ["investment_need","Nhu cầu đầu tư/kiến nghị","Chuỗi","Thông tin quản trị"],
    ["latitude","Vĩ độ","Số","Phục vụ bản đồ"],
    ["longitude","Kinh độ","Số","Phục vụ bản đồ"],
], columns=["Trường dữ liệu","Nghĩa tiếng Việt","Kiểu","Ghi chú"])

metadata = {
    "Nền tảng": "DakTech Infra AI",
    "Phân hệ": "DakWater AI – Quản lý cấp nước sạch",
    "Phiên bản quy chuẩn xuất": "EXPORT STANDARD v1.0",
    "Phạm vi hiện tại": "Dữ liệu mẫu/Public Demo",
    "Bộ lọc địa bàn": locality,
    "Bộ lọc loại nguồn": source,
    "Bộ lọc trạng thái": status,
    "Số dòng sau lọc": int(len(display)),
    "Nguyên tắc": "Không coi dữ liệu Public Demo là dữ liệu chính thức",
}

render_export_center(
    module_name="DakWater AI – Quản lý cấp nước sạch",
    module_slug="dakwater-ai",
    description="Tải dữ liệu trực tiếp từ Streamlit; không cần vào GitHub.",
    datasets={"cong_trinh_cap_nuoc": display},
    metadata=metadata,
    data_dictionary=dictionary,
    public_demo=True,
)
