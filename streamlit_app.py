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
        st.Page("pages/asset_360.py", title="Hồ sơ tài sản 360°", icon="🧭"),
    ],
    "Phân hệ chuyên ngành": [
        st.Page("pages/dakroad.py", title="DakRoad AI", icon="🛣️"),
        st.Page("pages/dakcemetery.py", title="DakCemetery AI", icon="⚱️"),
        st.Page("pages/cemetery_sources.py", title="Kho báo cáo nghĩa trang", icon="🗂️"),
        st.Page("pages/cemetery_import.py", title="Nạp báo cáo nghĩa trang", icon="📥"),
        st.Page("pages/dakwater.py", title="DakWater AI", icon="💧"),
        st.Page("pages/dakdrain.py", title="DakDrain AI", icon="🌧️"),
    ],
    "Quản trị dữ liệu": [
        st.Page("pages/data_import.py", title="Nhập & chuẩn hóa", icon="📥"),
        st.Page("pages/data_quality.py", title="Rule Engine dữ liệu", icon="🧪"),
        st.Page("pages/legal_data.py", title="Kho dữ liệu & pháp lý", icon="⚖️"),
        st.Page("pages/implementation.py", title="Lộ trình triển khai", icon="🧭"),
    ],
}

pg = st.navigation(pages)
pg.run()
