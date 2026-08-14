import pandas as pd
import streamlit as st

from core.config import MODULES
from core.data import load_asset_layer, load_asset_registry
from core.ui import point_map, show_key_value

st.title("🧭 Hồ sơ tài sản 360°")
st.caption("Một mã tài sản – một hồ sơ xuyên suốt: vị trí → pháp lý → quy hoạch → đầu tư → vận hành → bảo trì → sự cố → lịch sử.")

registry = load_asset_registry()

c1, c2 = st.columns([1, 2])
with c1:
    module_filter = st.selectbox("Phân hệ", ["ALL"] + list(MODULES.keys()), format_func=lambda x: "Tất cả" if x == "ALL" else MODULES[x]["name"])
with c2:
    choices = registry if module_filter == "ALL" else registry[registry["module"] == module_filter]
    selected = st.selectbox(
        "Chọn tài sản",
        choices["asset_code"].tolist(),
        format_func=lambda code: f"{code} – {choices.loc[choices.asset_code == code, 'asset_name'].iloc[0]}",
    )

asset = registry[registry["asset_code"] == selected].iloc[0]
st.subheader(f"{asset.asset_code} – {asset.asset_name}")
st.caption(f"{asset.module_name} • {asset.locality} • Trạng thái: {asset.status}")

tabs = st.tabs(["Định danh & bản đồ", "Pháp lý", "Quy hoạch/đất đai", "Đầu tư", "Vận hành", "Bảo trì & sự cố", "Lịch sử"])

with tabs[0]:
    left, right = st.columns([1, 1])
    with left:
        show_key_value(asset, [
            ("asset_code", "Mã tài sản"),
            ("module_name", "Phân hệ"),
            ("domain", "Lĩnh vực"),
            ("asset_type", "Loại tài sản"),
            ("locality", "Địa bàn"),
            ("management_unit", "Đơn vị quản lý"),
            ("status", "Trạng thái"),
            ("source_id", "Nguồn dữ liệu"),
            ("updated_at", "Cập nhật"),
            ("record_hash", "Mã băm bản ghi"),
        ])
    with right:
        point_map(pd.DataFrame([asset]), ["asset_code", "asset_name", "management_unit", "status"], zoom=12)

with tabs[1]:
    df = load_asset_layer("legal", selected)
    st.dataframe(df, width="stretch", hide_index=True)
    st.warning("Khung 360° không tự suy diễn căn cứ pháp lý. Quy định chuyên ngành chỉ được kích hoạt sau khi có nguồn, hiệu lực, phạm vi áp dụng và rà soát nghiệp vụ.")

with tabs[2]:
    df = load_asset_layer("planning", selected)
    st.dataframe(df, width="stretch", hide_index=True)

with tabs[3]:
    df = load_asset_layer("investment", selected)
    st.dataframe(df, width="stretch", hide_index=True)

with tabs[4]:
    df = load_asset_layer("operations", selected)
    st.dataframe(df, width="stretch", hide_index=True)

with tabs[5]:
    m = load_asset_layer("maintenance", selected)
    i = load_asset_layer("incidents", selected)
    st.markdown("#### Bảo trì")
    if m.empty:
        st.info("Chưa có bản ghi bảo trì cho tài sản này.")
    else:
        st.dataframe(m, width="stretch", hide_index=True)
    st.markdown("#### Sự cố")
    if i.empty:
        st.info("Chưa có sự cố trong bộ dữ liệu MVP.")
    else:
        st.dataframe(i, width="stretch", hide_index=True)

with tabs[6]:
    h = load_asset_layer("history", selected)
    st.dataframe(h, width="stretch", hide_index=True)
    st.caption("MVP v0.2 bắt đầu lưu dấu vết thay đổi bằng record_hash. Giai đoạn thí điểm cần chuyển thành audit log trong CSDL tập trung.")
