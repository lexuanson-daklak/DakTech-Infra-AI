import pandas as pd
import streamlit as st

from core.config import APP_NAME, APP_TAGLINE, MODULES, VERSION
from core.data import asset_summary, load_asset_registry
from core.registry import registry_completeness
from core.rule_engine import evaluate_registry_rules
from core.ui import kpi_row, point_map

st.title(f"🏗️ {APP_NAME}")
st.subheader(APP_TAGLINE)
st.caption(f"{VERSION} – dashboard điều hành dùng chung cho 4 phân hệ MVP.")

registry = load_asset_registry()
summary = asset_summary()
quality = evaluate_registry_rules(registry)
attention = registry[registry["status"] != "ACTIVE"]
completeness = registry_completeness(registry)

kpi_row([
    ("Phân hệ", f"{registry.module.nunique()}", "Đường bộ, nghĩa trang, cấp nước, thoát nước"),
    ("Tài sản mẫu", f"{len(registry):,}", "Tổng số tài sản trong Asset Registry dùng chung"),
    ("Cần chú ý", f"{len(attention):,}", "Tài sản có trạng thái khác ACTIVE"),
    ("Độ đầy đủ dữ liệu", f"{completeness:.1f}%", "Tỷ lệ có dữ liệu ở các trường bắt buộc của Asset Registry"),
    ("Lỗi dữ liệu", f"{int((quality.severity == 'ERROR').sum()) if not quality.empty else 0}", "Kết quả Rule Engine chất lượng dữ liệu"),
])

st.divider()
left, right = st.columns([3, 2])
with left:
    st.markdown("### Bản đồ tài sản dùng chung")
    point_map(registry, ["asset_code", "asset_name", "module_name", "locality", "status"], zoom=6.5)
with right:
    st.markdown("### Tín hiệu điều hành theo phân hệ")
    view = summary.copy()
    view["module_name"] = view["module"].map(lambda x: MODULES.get(x, {}).get("name", x))
    st.dataframe(view[["module_name", "assets", "active", "attention", "management_units", "localities"]], use_container_width=True, hide_index=True)
    st.bar_chart(view.set_index("module_name")[["active", "attention"]])

st.markdown("### Tài sản đang cần theo dõi")
if attention.empty:
    st.success("Không có tài sản nào mang trạng thái cần chú ý trong bộ dữ liệu hiện tại.")
else:
    st.dataframe(
        attention[["asset_code", "module_name", "asset_name", "locality", "management_unit", "status", "investment_need", "updated_at"]],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("### Từ v0.1 sang v0.2 đã thay đổi gì?")
st.info(
    "v0.2 đã có Asset Registry dùng chung, Hồ sơ tài sản 360°, nhập CSV/Excel có kiểm tra, "
    "Rule Engine chất lượng dữ liệu và dashboard lãnh đạo. Các quy tắc pháp lý chuyên ngành mới chỉ tạo khung, chưa tự động áp dụng."
)
