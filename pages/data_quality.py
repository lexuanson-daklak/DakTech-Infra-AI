import pandas as pd
import streamlit as st

from core.data import load_asset_registry
from core.rule_engine import evaluate_registry_rules, load_rule_catalog

st.title("🧪 Rule Engine & chất lượng dữ liệu")
st.caption("v0.2 chỉ kích hoạt các quy tắc an toàn về dữ liệu và tín hiệu quản trị; quy tắc pháp lý chuyên ngành đang khóa.")

registry = load_asset_registry()
results = evaluate_registry_rules(registry)
catalog = pd.DataFrame(load_rule_catalog())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Quy tắc đã khai báo", len(catalog))
c2.metric("Đang bật", int(catalog["enabled"].sum()))
c3.metric("Đang khóa", int((~catalog["enabled"]).sum()))
c4.metric("Tín hiệu/lỗi", len(results))

st.markdown("### Danh mục quy tắc")
st.dataframe(catalog, use_container_width=True, hide_index=True)

st.markdown("### Kết quả chạy Rule Engine")
if results.empty:
    st.success("Không phát hiện lỗi/tín hiệu theo bộ quy tắc hiện hành.")
else:
    severity = st.multiselect("Lọc mức độ", sorted(results["severity"].unique().tolist()), default=sorted(results["severity"].unique().tolist()))
    st.dataframe(results[results["severity"].isin(severity)], use_container_width=True, hide_index=True)

st.warning(
    "CEM-LEGAL-001, WTR-LEGAL-001 và DRN-LEGAL-001 chỉ là vị trí giữ chỗ trong kiến trúc và đang disabled. "
    "Không được bật cho đến khi bộ căn cứ pháp lý và quy trình nghiệp vụ được rà soát, phê duyệt để thí điểm."
)
