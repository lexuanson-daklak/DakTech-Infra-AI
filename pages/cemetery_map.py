import streamlit as st

from core.cemetery_inventory_service import metric_from_summary
from core.cemetery_service import load_cemetery_master
from core.ui import point_map

st.title("🗺️ Bản đồ nghĩa trang")
st.caption("Bản đồ chỉ đưa dữ liệu thật lên khi đã có tọa độ và được xác minh đủ điều kiện sử dụng.")

verified = int(metric_from_summary("Bản ghi đã xác minh"))
st.metric("Bản ghi thực tế đã xác minh sẵn sàng lên bản đồ", verified)
if verified == 0:
    st.info(
        "Hiện chưa có bản ghi dẫn xuất từ báo cáo được xác minh để đưa lên bản đồ công khai. "
        "Hệ thống không tự suy đoán tọa độ từ tên địa danh."
    )

st.markdown("### Bản đồ mẫu kiểm chứng giao diện")
demo = load_cemetery_master()
point_map(demo, ["asset_code", "asset_name", "locality", "status", "verified_status"], zoom=6.7)
st.caption("Các điểm trên là dữ liệu mô phỏng, không phải vị trí nghĩa trang thực tế.")
