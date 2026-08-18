import streamlit as st

from core.config import APP_NAME, APP_TAGLINE, DISCLAIMER, VERSION

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

home = st.Page("pages/home.py", title="Bảng điều hành lãnh đạo", icon="🏠", url_path="dieu-hanh", default=True)
system_views = st.Page("pages/system_views.py", title="Cấu trúc hệ thống", icon="🧩", url_path="cau-truc-he-thong")
asset_360 = st.Page("pages/asset_360.py", title="Hồ sơ tài sản 360°", icon="🧭", url_path="ho-so-tai-san")

water_dashboard = st.Page("pages/water_dashboard.py", title="Bảng điều hành cấp nước", icon="📊", url_path="cap-nuoc")
water_inventory = st.Page("pages/water_inventory.py", title="Danh mục công trình cấp nước", icon="📋", url_path="danh-muc-cap-nuoc")
water_map = st.Page("pages/dakwater.py", title="Bản đồ cấp nước", icon="🗺️", url_path="ban-do-cap-nuoc")
water_model = st.Page("pages/water_data_model.py", title="Mô hình dữ liệu cấp nước", icon="🧱", url_path="mo-hinh-du-lieu-cap-nuoc")
water_export = st.Page("pages/water_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤", url_path="xuat-du-lieu-cap-nuoc")

drain_dashboard = st.Page("pages/drain_dashboard.py", title="Bảng điều hành thoát nước", icon="📊", url_path="thoat-nuoc")
drain_inventory = st.Page("pages/drain_inventory.py", title="Danh mục công trình thoát nước", icon="📋", url_path="danh-muc-thoat-nuoc")
drain_map = st.Page("pages/dakdrain.py", title="Bản đồ thoát nước", icon="🗺️", url_path="ban-do-thoat-nuoc")
drain_model = st.Page("pages/drain_data_model.py", title="Mô hình dữ liệu thoát nước", icon="🧱", url_path="mo-hinh-du-lieu-thoat-nuoc")
drain_export = st.Page("pages/drain_export_center.py", title="Trung tâm xuất dữ liệu", icon="📤", url_path="xuat-du-lieu-thoat-nuoc")

road = st.Page("pages/dakroad.py", title="Quản lý kết cấu hạ tầng đường bộ", icon="🛣️", url_path="duong-bo")
data_import = st.Page("pages/data_import.py", title="Nhập và chuẩn hóa dữ liệu", icon="📥", url_path="nhap-du-lieu")
data_quality = st.Page("pages/data_quality.py", title="Kiểm tra chất lượng dữ liệu", icon="🧪", url_path="chat-luong-du-lieu")
legal_data = st.Page("pages/legal_data.py", title="Kho dữ liệu và cơ sở pháp lý", icon="⚖️", url_path="co-so-phap-ly")
implementation = st.Page("pages/implementation.py", title="Lộ trình triển khai", icon="🧭", url_path="lo-trinh")
paused = st.Page("pages/paused_modules.py", title="Nghĩa trang – DakCemetery AI", icon="⏸️", url_path="phan-he-tam-dung")

all_pages = [
    home, system_views, asset_360,
    water_dashboard, water_inventory, water_map, water_model, water_export,
    drain_dashboard, drain_inventory, drain_map, drain_model, drain_export,
    road, data_import, data_quality, legal_data, implementation, paused,
]

pg = st.navigation(all_pages, position="hidden")

with st.sidebar:
    st.title("🏗️ DakTech Infra AI")
    st.caption(APP_TAGLINE)
    st.info(f"Phiên bản: {VERSION}")

    st.markdown("### Điều hành chung")
    st.page_link(home, label="Bảng điều hành lãnh đạo", icon="🏠", width="stretch")
    st.page_link(system_views, label="Cấu trúc hệ thống", icon="🧩", width="stretch")
    st.page_link(asset_360, label="Hồ sơ tài sản 360°", icon="🧭", width="stretch")

    st.markdown("### 💧 Cấp nước sạch")
    st.caption("DakWater AI")
    st.page_link(water_dashboard, label="Bảng điều hành cấp nước", icon="📊", width="stretch")
    st.page_link(water_inventory, label="Danh mục công trình", icon="📋", width="stretch")
    st.page_link(water_map, label="Bản đồ cấp nước", icon="🗺️", width="stretch")
    st.page_link(water_model, label="Mô hình dữ liệu", icon="🧱", width="stretch")
    st.page_link(water_export, label="Trung tâm xuất dữ liệu", icon="📤", width="stretch")

    st.markdown("### 🌧️ Thoát nước và nước thải")
    st.caption("DakDrain AI")
    st.page_link(drain_dashboard, label="Bảng điều hành thoát nước", icon="📊", width="stretch")
    st.page_link(drain_inventory, label="Danh mục công trình", icon="📋", width="stretch")
    st.page_link(drain_map, label="Bản đồ thoát nước", icon="🗺️", width="stretch")
    st.page_link(drain_model, label="Mô hình dữ liệu", icon="🧱", width="stretch")
    st.page_link(drain_export, label="Trung tâm xuất dữ liệu", icon="📤", width="stretch")

    with st.expander("🛣️ Đường bộ"):
        st.page_link(road, label="Quản lý kết cấu hạ tầng đường bộ", icon="🛣️", width="stretch")

    with st.expander("⚖️ Dữ liệu và cơ sở pháp lý"):
        st.page_link(data_import, label="Nhập và chuẩn hóa dữ liệu", icon="📥", width="stretch")
        st.page_link(data_quality, label="Kiểm tra chất lượng dữ liệu", icon="🧪", width="stretch")
        st.page_link(legal_data, label="Kho dữ liệu và cơ sở pháp lý", icon="⚖️", width="stretch")
        st.page_link(implementation, label="Lộ trình triển khai", icon="🧭", width="stretch")

    with st.expander("⏸️ Phân hệ tạm dừng"):
        st.page_link(paused, label="Nghĩa trang – DakCemetery AI", icon="⏸️", width="stretch")

    st.divider()
    st.warning(DISCLAIMER)

pg.run()
