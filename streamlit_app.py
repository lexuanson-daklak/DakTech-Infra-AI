import streamlit as st

from core.config import APP_NAME, APP_TAGLINE, DISCLAIMER, VERSION

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🏗️ DakTech Infra AI")
st.sidebar.caption(APP_TAGLINE)
st.sidebar.info(f"Phiên bản: {VERSION}")
st.sidebar.warning(DISCLAIMER)

pages = {
    "Điều hành chung": [
        st.Page("pages/home.py", title="Bảng điều hành lãnh đạo", icon="🏠"),
        st.Page("pages/system_views.py", title="Cấu trúc hệ thống", icon="🧩"),
        st.Page("pages/asset_360.py", title="Hồ sơ tài sản 360°", icon="🧭"),
    ],
    "Cấp nước sạch – DakWater AI": [
        st.Page("pages/water_dashboard.py", title="Bảng điều hành cấp nước", icon="📊"),
        st.Page("pages/water_inventory.py", title="Danh mục công trình cấp nước", icon="📋"),
        st.Page("pages/dakwater.py", title="Bản đồ cấp nước", icon="🗺️"),
        st.Page("pages/water_data_model.py", title="Mô hình dữ liệu cấp nước", icon="🧱"),
        st.Page("pages/water_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤"),
    ],
    "Thoát nước & nước thải – DakDrain AI": [
        st.Page("pages/drain_dashboard.py", title="Bảng điều hành thoát nước", icon="📊"),
        st.Page("pages/drain_inventory.py", title="Danh mục công trình thoát nước", icon="📋"),
        st.Page("pages/dakdrain.py", title="Bản đồ thoát nước", icon="🗺️"),
        st.Page("pages/drain_data_model.py", title="Mô hình dữ liệu thoát nước", icon="🧱"),
        st.Page("pages/drain_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤"),
    ],
    "Đường bộ – DakRoad AI": [
        st.Page("pages/dakroad.py", title="Quản lý kết cấu hạ tầng đường bộ", icon="🛣️"),
    ],
    "Dữ liệu và cơ sở pháp lý": [
        st.Page("pages/data_import.py", title="Nhập và chuẩn hóa dữ liệu", icon="📥"),
        st.Page("pages/data_quality.py", title="Kiểm tra chất lượng dữ liệu", icon="🧪"),
        st.Page("pages/legal_data.py", title="Kho dữ liệu và cơ sở pháp lý", icon="⚖️"),
        st.Page("pages/implementation.py", title="Lộ trình triển khai", icon="🧭"),
    ],
    "Phân hệ tạm dừng": [
        st.Page("pages/paused_modules.py", title="Nghĩa trang – DakCemetery AI", icon="⏸️"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
