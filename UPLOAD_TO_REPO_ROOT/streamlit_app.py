import streamlit as st

from core.config import APP_NAME, APP_TAGLINE, DISCLAIMER, VERSION

st.set_page_config(page_title=APP_NAME, page_icon="🏗️", layout="wide")

st.sidebar.title("🏗️ DakTech Infra AI")
st.sidebar.caption(APP_TAGLINE)
st.sidebar.info(VERSION)
st.sidebar.warning(DISCLAIMER)

pages = {
    "Điều hành": [
        st.Page("pages/home.py", title="Dashboard lãnh đạo", icon="🏠"),
        st.Page("pages/system_views.py", title="Cấu trúc hệ thống", icon="🧩"),
        st.Page("pages/asset_360.py", title="Hồ sơ tài sản 360°", icon="🧭"),
    ],
    "DakWater AI – Quản lý cấp nước sạch": [
        st.Page("pages/water_dashboard.py", title="Dashboard cấp nước", icon="📊"),
        st.Page("pages/water_inventory.py", title="Danh mục công trình cấp nước", icon="📋"),
        st.Page("pages/dakwater.py", title="Bản đồ cấp nước (mẫu)", icon="🗺️"),
        st.Page("pages/water_data_model.py", title="Mô hình dữ liệu cấp nước", icon="🧱"),
        st.Page("pages/water_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤"),
    ],
    "DakDrain AI – Quản lý thoát nước và nước thải": [
        st.Page("pages/drain_dashboard.py", title="Dashboard thoát nước", icon="📊"),
        st.Page("pages/drain_inventory.py", title="Danh mục thoát nước", icon="📋"),
        st.Page("pages/dakdrain.py", title="Bản đồ thoát nước (mẫu)", icon="🗺️"),
        st.Page("pages/drain_data_model.py", title="Mô hình dữ liệu thoát nước", icon="🧱"),
        st.Page("pages/drain_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤"),
    ],
    "DakCemetery AI – Nghĩa trang (tạm dừng)": [
        st.Page("pages/cemetery_dashboard.py", title="Dashboard nghĩa trang", icon="📊"),
        st.Page("pages/cemetery_inventory.py", title="Danh mục nghĩa trang", icon="📋"),
        st.Page("pages/cemetery_review_queue.py", title="Hàng đợi rà soát", icon="🧹"),
        st.Page("pages/cemetery_map.py", title="Bản đồ nghĩa trang", icon="🗺️"),
        st.Page("pages/dakcemetery.py", title="Hồ sơ nghĩa trang 360° (mẫu)", icon="⚱️"),
        st.Page("pages/cemetery_sources.py", title="Kho báo cáo nghĩa trang", icon="🗂️"),
        st.Page("pages/cemetery_import.py", title="Mô phỏng nạp báo cáo", icon="📥"),
    ],
    "Các phân hệ khác": [
        st.Page("pages/dakroad.py", title="DakRoad AI – Đường bộ", icon="🛣️"),
    ],
    "Quản trị dữ liệu": [
        st.Page("pages/data_import.py", title="Nhập & chuẩn hóa", icon="📥"),
        st.Page("pages/data_quality.py", title="Bộ kiểm tra quy tắc dữ liệu", icon="🧪"),
        st.Page("pages/legal_data.py", title="Kho dữ liệu & pháp lý", icon="⚖️"),
        st.Page("pages/implementation.py", title="Lộ trình triển khai", icon="🧭"),
    ],
}

pg = st.navigation(pages)
pg.run()
