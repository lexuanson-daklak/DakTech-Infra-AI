import pandas as pd
import streamlit as st

from core.config import DATA_DIR, VERSION
from core.cemetery_inventory_service import load_collection_status
from core.ui import kpi_row

st.title("🗂️ Kho báo cáo nghĩa trang")
st.caption("Theo dõi mức độ thu thập, phạm vi nguồn, trạng thái xử lý và chất lượng dữ liệu báo cáo nghĩa trang.")

st.warning(
    f"Đây là lớp kiểm kê nguồn của {VERSION}. Số liệu 'đã tách sơ bộ' là dữ liệu dẫn xuất từ báo cáo, "
    "chưa phải cơ sở dữ liệu nghĩa trang chính thức của tỉnh và chưa dùng để thay thế hồ sơ nguồn."
)

overview_path = DATA_DIR / "cemetery_collection_overview_v0.4.csv"
overview = pd.read_csv(overview_path) if overview_path.exists() else pd.DataFrame()
status = load_collection_status()


def metric_value(label: str, default=0):
    if overview.empty:
        return default
    hit = overview[overview["chi_tieu"] == label]
    return hit.iloc[0]["gia_tri"] if not hit.empty else default

kpi_row([
    ("Gói hồ sơ đã tiếp nhận", f"{int(metric_value('Gói hồ sơ đã tiếp nhận')):,}", "03 tệp RAR do tác giả thu thập"),
    ("Báo cáo hiện trạng cấp xã/phường", f"{int(metric_value('Báo cáo hiện trạng cấp xã/phường')):,}", "Nhóm có nội dung rà soát/hiện trạng"),
    ("Bản ghi đã tách sơ bộ", f"{int(metric_value('Bản ghi chi tiết đã tách sơ bộ')):,}", "Dữ liệu dẫn xuất, chưa xác minh chính thức"),
    ("Nguồn đã tách được bản ghi", f"{int(metric_value('Nguồn có bản ghi chi tiết đã tách')):,}", "Một số nguồn chỉ có thông tin tổng hợp hoặc quyết định"),
    ("Bản ghi có cờ chất lượng", f"{int(metric_value('Bản ghi có cờ chất lượng dữ liệu')):,}", "Cờ chất lượng v0.4; v0.5 có thêm hàng đợi rà soát trùng/thiếu trường"),
])

st.markdown("### 1. Phạm vi hồ sơ đã thu thập")
if overview.empty:
    st.info("Chưa có tệp tổng hợp nguồn.")
else:
    st.dataframe(overview.rename(columns={"chi_tieu":"Chỉ tiêu", "gia_tri":"Giá trị", "ghi_chu":"Ghi chú"}), width="stretch", hide_index=True)

st.markdown("### 2. Tình trạng xử lý theo nguồn báo cáo")
if status.empty:
    st.info("Chưa có dữ liệu kiểm kê nguồn.")
else:
    labels = {
        "source_id":"Mã nguồn", "package_no":"Gói số", "reporting_entity":"Nguồn báo cáo",
        "source_type":"Loại nguồn", "data_use_status":"Trạng thái sử dụng dữ liệu",
        "structured_records":"Bản ghi đã tách", "reported_count":"Số lượng theo báo cáo",
        "reported_area_ha":"Diện tích báo cáo (ha)", "records_with_quality_flags":"Bản ghi có cờ chất lượng",
        "verification_status":"Trạng thái xác minh",
    }
    cols=[c for c in labels if c in status.columns]
    st.dataframe(status[cols].rename(columns=labels), width="stretch", hide_index=True)

st.markdown("### 3. Những nhóm nguồn phải xử lý riêng")
st.markdown(
    "- Nguồn đã xin lấy lại/hủy văn bản → **không dùng làm dữ liệu chính thức**.\n"
    "- Văn bản triển khai chưa có danh mục hiện trạng → chỉ quản lý như nguồn.\n"
    "- Hồ sơ quy hoạch/mở rộng → tách khỏi kiểm kê hiện trạng.\n"
    "- Quyết định đóng cửa/chuyển trạng thái → quản lý theo lịch sử.\n"
    "- Báo cáo đơn vị vận hành → tách với báo cáo cấp xã/phường.\n"
    "- Hồ sơ bối cảnh dự án/di dời → không coi là danh mục hiện trạng đầy đủ."
)

st.markdown("### 4. Nguyên tắc đưa dữ liệu vào hệ thống")
st.markdown(
    "1. Giữ nguyên tệp nguồn và mã nguồn.\n"
    "2. Dữ liệu tách từ báo cáo được đánh dấu **CHƯA XÁC MINH**.\n"
    "3. Không tự sửa số liệu bất thường; chỉ gắn cờ để đối chiếu.\n"
    "4. Không cộng thành 'tổng số nghĩa trang toàn tỉnh' khi phạm vi báo cáo chưa đầy đủ.\n"
    "5. Không tự động gộp các bản ghi có tên giống nhau.\n"
    "6. Chỉ dữ liệu đã được cán bộ xác minh mới chuyển sang danh mục chính thức."
)

st.markdown("### 5. Dữ liệu làm việc nội bộ")
st.info(
    "Bản GitHub Public không cho nạp tệp dữ liệu nội bộ. Bộ chi tiết được quản lý riêng trong **DakCemetery Local DataPack v0.5** "
    "và chỉ dùng ở môi trường nội bộ/phiên bản riêng tư phù hợp."
)
