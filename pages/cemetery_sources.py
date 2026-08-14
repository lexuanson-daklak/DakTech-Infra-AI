from pathlib import Path

import pandas as pd
import streamlit as st

from core.config import DATA_DIR
from core.ui import kpi_row

st.title("🗂️ Kho báo cáo nghĩa trang")
st.caption("Theo dõi mức độ thu thập, phạm vi nguồn, trạng thái xử lý và chất lượng dữ liệu báo cáo nghĩa trang.")

st.warning(
    "Đây là lớp kiểm kê nguồn của MVP v0.4. Số liệu 'đã tách sơ bộ' là dữ liệu dẫn xuất từ báo cáo, "
    "chưa phải cơ sở dữ liệu nghĩa trang chính thức của tỉnh và chưa dùng để thay thế hồ sơ nguồn."
)

overview_path = DATA_DIR / "cemetery_collection_overview_v0.4.csv"
status_path = DATA_DIR / "cemetery_collection_status_v0.4.csv"

overview = pd.read_csv(overview_path) if overview_path.exists() else pd.DataFrame()
status = pd.read_csv(status_path) if status_path.exists() else pd.DataFrame()


def metric_value(label: str, default=0):
    if overview.empty:
        return default
    hit = overview[overview["chi_tieu"] == label]
    if hit.empty:
        return default
    return hit.iloc[0]["gia_tri"]

kpi_row([
    ("Gói hồ sơ đã tiếp nhận", f"{int(metric_value('Gói hồ sơ đã tiếp nhận')):,}", "03 tệp RAR do tác giả thu thập"),
    ("Báo cáo hiện trạng cấp xã/phường", f"{int(metric_value('Báo cáo hiện trạng cấp xã/phường')):,}", "Nhóm có nội dung rà soát/hiện trạng"),
    ("Bản ghi đã tách sơ bộ", f"{int(metric_value('Bản ghi chi tiết đã tách sơ bộ')):,}", "Dữ liệu dẫn xuất, chưa xác minh chính thức"),
    ("Nguồn đã tách được bản ghi", f"{int(metric_value('Nguồn có bản ghi chi tiết đã tách')):,}", "Một số nguồn chỉ có thông tin tổng hợp hoặc quyết định"),
    ("Bản ghi có cờ chất lượng", f"{int(metric_value('Bản ghi có cờ chất lượng dữ liệu')):,}", "Cần đối chiếu trước khi dùng điều hành"),
])

st.markdown("### 1. Phạm vi hồ sơ đã thu thập")
if overview.empty:
    st.info("Chưa có tệp tổng hợp nguồn.")
else:
    ov = overview.rename(columns={"chi_tieu": "Chỉ tiêu", "gia_tri": "Giá trị", "ghi_chu": "Ghi chú"})
    st.dataframe(ov, use_container_width=True, hide_index=True)

st.markdown("### 2. Tình trạng xử lý theo đơn vị báo cáo")
if status.empty:
    st.info("Chưa có dữ liệu kiểm kê nguồn.")
else:
    labels = {
        "source_id": "Mã nguồn",
        "package_no": "Gói số",
        "reporting_entity": "Đơn vị báo cáo",
        "source_type": "Loại nguồn",
        "data_use_status": "Trạng thái sử dụng dữ liệu",
        "structured_records": "Bản ghi đã tách",
        "reported_count": "Số lượng theo báo cáo",
        "reported_area_ha": "Diện tích báo cáo (ha)",
        "records_with_quality_flags": "Bản ghi có cờ chất lượng",
        "verification_status": "Trạng thái xác minh",
    }
    view = status.rename(columns=labels)
    st.dataframe(view, use_container_width=True, hide_index=True)

st.markdown("### 3. Những nhóm nguồn phải xử lý riêng")
st.markdown(
    "- Có nguồn đã xin lấy lại/hủy văn bản → **không dùng làm dữ liệu chính thức**.\n"
    "- Có nguồn mới là văn bản triển khai, chưa có danh mục hiện trạng để nhập.\n"
    "- Có nguồn chủ yếu là hồ sơ quy hoạch/mở rộng → cần tách khỏi kiểm kê hiện trạng.\n"
    "- Có nguồn có quyết định đóng cửa/chuyển trạng thái → cần quản lý theo lịch sử.\n"
    "- Có nguồn từ đơn vị vận hành → phải tách với báo cáo cấp xã/phường.\n"
    "- Có nguồn bối cảnh dự án/di dời → không coi là danh mục hiện trạng đầy đủ."
)

st.markdown("### 4. Nguyên tắc đưa dữ liệu vào hệ thống")
st.markdown(
    "1. Giữ nguyên tệp nguồn và mã nguồn.\n"
    "2. Dữ liệu tách từ báo cáo được đánh dấu **CHƯA XÁC MINH**.\n"
    "3. Không tự sửa các số liệu có dấu hiệu bất thường; chỉ gắn cờ để đối chiếu.\n"
    "4. Không cộng thành 'tổng số nghĩa trang toàn tỉnh' khi phạm vi báo cáo chưa đầy đủ.\n"
    "5. Chỉ dữ liệu đã được cán bộ xác minh mới được chuyển sang lớp điều hành/chính thức."
)

st.markdown("### 5. Mở dữ liệu làm việc nội bộ (không lưu lên GitHub)")
st.info(
    "Nếu có tệp CSV dữ liệu chi tiết đã được chuẩn hóa ở máy nội bộ, có thể nạp tạm vào phiên làm việc để kiểm tra. "
    "Tệp không được ghi vào repository bởi chức năng này. Với dữ liệu nhạy cảm/nội bộ, không nên nạp trên website demo công khai."
)
private_upload = st.file_uploader("Chọn CSV dữ liệu làm việc nội bộ (tùy chọn)", type=["csv"], key="cem_private_upload")
if private_upload is not None:
    try:
        private_df = pd.read_csv(private_upload)
        st.success(f"Đã đọc tạm {len(private_df):,} bản ghi trong phiên làm việc.")
        st.dataframe(private_df.head(200), use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Không đọc được tệp: {exc}")
