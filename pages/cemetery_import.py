from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from core.cemetery_service import (
    CEMETERY_CANONICAL_FIELDS,
    list_excel_sheets,
    normalize_cemetery_frame,
    read_report_table,
    suggest_column_mapping,
    validate_cemetery_frame,
)
from core.config import TEMPLATE_DIR

st.title("📥 Nạp báo cáo nghĩa trang")
st.caption("Dùng cho các báo cáo Excel/CSV đang có ở xã, phường, đơn vị quản lý hoặc hồ sơ tổng hợp của Phòng.")

st.warning(
    "MVP v0.3 KHÔNG tự ghi dữ liệu báo cáo vào kho chính thức. Tệp nguồn được giữ nguyên; bước này chỉ ghép cột, chuẩn hóa, kiểm tra và tạo bản dữ liệu chờ xác minh."
)

st.markdown("### 1. Biểu mẫu chuẩn chuyên ngành")
template = TEMPLATE_DIR / "DakCemetery_Bieu_mau_du_lieu_v0.3.xlsx"
if template.exists():
    st.download_button(
        "⬇️ Tải biểu mẫu dữ liệu nghĩa trang",
        data=template.read_bytes(),
        file_name=template.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.markdown("### 2. Nạp báo cáo đang có")
uploaded = st.file_uploader("Chọn báo cáo CSV hoặc Excel", type=["csv", "xlsx"])
if uploaded is not None:
    sheet = None
    if Path(uploaded.name).suffix.lower() == ".xlsx":
        try:
            sheets = list_excel_sheets(uploaded)
            sheet = st.selectbox("Chọn sheet cần đọc", sheets)
        except Exception as exc:
            st.error(f"Không đọc được danh sách sheet: {exc}")

    try:
        source_df = read_report_table(uploaded, sheet_name=sheet)
    except Exception as exc:
        st.exception(exc)
        st.stop()

    st.markdown("#### Xem dữ liệu nguồn")
    st.dataframe(source_df.head(100), use_container_width=True, hide_index=True)
    st.caption(f"Số dòng đọc được: {len(source_df):,} | Số cột: {len(source_df.columns):,}")

    suggestions = suggest_column_mapping([str(c) for c in source_df.columns])
    st.markdown("### 3. Ghép cột báo cáo vào bộ dữ liệu chuẩn")
    st.caption("Hệ thống gợi ý một số cột theo tên gọi thường gặp. Cán bộ là người xác nhận việc ghép cột.")

    mapping = {}
    fields_to_map = [
        "asset_code", "asset_name", "locality", "address", "management_unit", "status",
        "total_area_ha", "used_area_ha", "remaining_area_ha", "planned_expansion_area_ha",
        "planning_status", "land_status", "environmental_status", "investment_need",
        "source_id", "source_doc_no", "source_doc_date", "reporting_period", "updated_at", "notes",
    ]
    choices = ["— Không ghép —"] + [str(c) for c in source_df.columns]
    cols = st.columns(2)
    for i, field in enumerate(fields_to_map):
        suggested = suggestions.get(field)
        default_idx = choices.index(suggested) if suggested in choices else 0
        with cols[i % 2]:
            selected = st.selectbox(field, choices, index=default_idx, key=f"map_{field}")
        mapping[field] = None if selected == "— Không ghép —" else selected

    normalized = normalize_cemetery_frame(source_df, mapping)
    _, issues, summary = validate_cemetery_frame(normalized)

    st.markdown("### 4. Kết quả chuẩn hóa trước khi nhập kho")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Số dòng", summary["rows"])
    c2.metric("Lỗi", summary["errors"])
    c3.metric("Cảnh báo", summary["warnings"])
    c4.metric("Mã tạm", summary["temporary_codes"])

    st.dataframe(normalized, use_container_width=True, hide_index=True)

    st.markdown("#### Danh sách lỗi/cảnh báo")
    if issues.empty:
        st.success("Chưa phát hiện lỗi/cảnh báo theo bộ kiểm tra dữ liệu nghĩa trang v0.3.")
    else:
        st.dataframe(issues, use_container_width=True, hide_index=True)

    st.markdown("### 5. Xuất bản chờ xác minh")
    csv_bytes = normalized.to_csv(index=False).encode("utf-8-sig")
    xlsx_buffer = BytesIO()
    with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
        normalized.to_excel(writer, index=False, sheet_name="Du_lieu_chuan_hoa")
        issues.to_excel(writer, index=False, sheet_name="Loi_Canh_bao")

    left, right = st.columns(2)
    with left:
        st.download_button("⬇️ Tải CSV chuẩn hóa", csv_bytes, "dakcemetery_cho_xac_minh.csv", "text/csv")
    with right:
        st.download_button(
            "⬇️ Tải Excel chuẩn hóa + cảnh báo",
            xlsx_buffer.getvalue(),
            "dakcemetery_cho_xac_minh.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

st.markdown("### Nguyên tắc khi dùng báo cáo thực tế")
st.markdown(
    "- Không sửa số liệu nguồn trong bước nhập.\n"
    "- Nếu báo cáo không có mã nghĩa trang, hệ thống chỉ cấp **mã tạm**.\n"
    "- Số liệu tính toán như tỷ lệ sử dụng hay năm ước tính đầy được tách riêng, không ghi đè số liệu báo cáo.\n"
    "- Chỉ sau khi xác minh đơn vị báo cáo, thời điểm, nguồn, địa điểm và mã tài sản mới đưa vào kho chính thức."
)
