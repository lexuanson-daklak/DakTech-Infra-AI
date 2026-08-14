import pandas as pd
import streamlit as st

from core.config import DATA_DIR, MODULES

st.title("⚖️ Kho dữ liệu & Legal Version Control")
st.caption("Lớp pháp lý dùng chung cho DakTech Infra AI; v0.2 tiếp tục kế thừa kho DakRoad và tạo khung liên kết tới từng tài sản.")

st.markdown("### Nguyên tắc")
st.code("Văn bản gốc → Văn bản sửa đổi → Văn bản hợp nhất → Hiệu lực → Lĩnh vực → Quy tắc nghiệp vụ → Hồ sơ/tài sản liên quan")

sources = pd.read_csv(DATA_DIR / "dakroad_legal_sources.csv")
flags = pd.read_csv(DATA_DIR / "dakroad_legal_review_flags.csv")
links = pd.read_csv(DATA_DIR / "asset_legal_links.csv")
data_sources = pd.read_csv(DATA_DIR / "data_sources.csv")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Nguồn pháp lý DakRoad", len(sources))
c2.metric("Cờ rà soát pháp lý", len(flags))
c3.metric("Tài sản có khung liên kết", links.asset_code.nunique())
c4.metric("Nguồn dữ liệu tài sản", len(data_sources))

st.subheader("Nguồn pháp lý kế thừa từ DakRoad AI")
show_cols = [c for c in ["source_id", "document_no", "date", "issuer", "document_type", "territory", "status", "summary"] if c in sources.columns]
st.dataframe(sources[show_cols], use_container_width=True, hide_index=True)

st.subheader("Các điểm cần rà soát")
st.dataframe(flags, use_container_width=True, hide_index=True)

st.subheader("Tình trạng pháp lý theo phân hệ")
rows = []
for code, m in MODULES.items():
    module_links = links[links["module"] == code]
    rows.append({
        "module": m["name"],
        "domain": m["domain"],
        "assets_linked": module_links.asset_code.nunique(),
        "legal_state": "Kế thừa kho DakRoad; vẫn phải xác định phạm vi áp dụng" if code == "road" else "Chưa nạp bộ pháp lý chuyên ngành",
        "legal_rule_engine": "Chưa tự động quyết định",
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.subheader("Nguồn dữ liệu tài sản")
st.dataframe(data_sources, use_container_width=True, hide_index=True)

st.warning("Không tự động coi dự thảo, đề án địa phương hoặc tài liệu tham khảo là quy định có hiệu lực. Mỗi dữ liệu pháp lý phải có nguồn, trạng thái, thời gian và phạm vi áp dụng.")
