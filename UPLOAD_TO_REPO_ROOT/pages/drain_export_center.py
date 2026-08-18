import pandas as pd
import streamlit as st

from core.data import load_assets
from core.export_center import render_export_center

df = load_assets("drain").copy()

type_vi = {
    "SEWER":"Tuyến cống",
    "FLOOD_POINT":"Điểm ngập",
    "PUMP_STATION":"Trạm bơm",
    "WWTP":"Nhà máy xử lý nước thải",
    "OUTFALL":"Điểm xả",
}
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
types = ["Tất cả"] + sorted(df["asset_type"].dropna().astype(str).unique().tolist())
basins = ["Tất cả"] + sorted(df["basin"].dropna().astype(str).unique().tolist())
statuses = ["Tất cả"] + sorted(df["status"].dropna().astype(str).unique().tolist())

atype = st.sidebar.selectbox("Loại đối tượng", types)
basin = st.sidebar.selectbox("Lưu vực", basins)
status = st.sidebar.selectbox("Trạng thái", statuses)

f = df.copy()
if atype != "Tất cả":
    f = f[f["asset_type"].astype(str) == atype]
if basin != "Tất cả":
    f = f[f["basin"].astype(str) == basin]
if status != "Tất cả":
    f = f[f["status"].astype(str) == status]

display = f.copy()
if "asset_type" in display.columns:
    display["asset_type_vi"] = display["asset_type"].map(type_vi).fillna(display["asset_type"])
if "status" in display.columns:
    display["status_vi"] = display["status"].map(status_vi).fillna(display["status"])

dictionary = pd.DataFrame([
    ["asset_code","Mã tài sản/đối tượng","Chuỗi","Định danh kỹ thuật"],
    ["asset_name","Tên đối tượng","Chuỗi","Tên theo dữ liệu đang quản lý"],
    ["asset_type","Loại đối tượng","Chuỗi","Tuyến cống/điểm ngập/trạm bơm/XLNT/điểm xả"],
    ["locality","Địa bàn","Chuỗi","Địa danh/hành chính theo nguồn"],
    ["basin","Lưu vực","Chuỗi","Lưu vực thoát nước"],
    ["capacity_note","Quy mô/công suất","Chuỗi","Thông tin mô tả"],
    ["management_unit","Đơn vị quản lý/vận hành","Chuỗi","Theo hồ sơ nguồn"],
    ["status","Mã trạng thái","Chuỗi","Mã kỹ thuật"],
    ["investment_need","Nhu cầu đầu tư/kiến nghị","Chuỗi","Thông tin quản trị"],
    ["latitude","Vĩ độ","Số","Phục vụ bản đồ"],
    ["longitude","Kinh độ","Số","Phục vụ bản đồ"],
], columns=["Trường dữ liệu","Nghĩa tiếng Việt","Kiểu","Ghi chú"])

metadata = {
    "Nền tảng": "DakTech Infra AI",
    "Phân hệ": "DakDrain AI – Quản lý thoát nước và xử lý nước thải",
    "Phiên bản quy chuẩn xuất": "EXPORT STANDARD v1.0",
    "Phạm vi hiện tại": "Dữ liệu mẫu/Public Demo",
    "Bộ lọc loại đối tượng": atype,
    "Bộ lọc lưu vực": basin,
    "Bộ lọc trạng thái": status,
    "Số dòng sau lọc": int(len(display)),
    "Nguyên tắc": "Không coi dữ liệu Public Demo là dữ liệu chính thức",
}

render_export_center(
    module_name="DakDrain AI – Quản lý thoát nước và xử lý nước thải",
    module_slug="dakdrain-ai",
    description="Tải dữ liệu trực tiếp từ Streamlit; không cần vào GitHub.",
    datasets={"thoat_nuoc_nuoc_thai": display},
    metadata=metadata,
    data_dictionary=dictionary,
    public_demo=True,
)
