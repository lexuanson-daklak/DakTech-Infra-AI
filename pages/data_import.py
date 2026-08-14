from pathlib import Path

import streamlit as st

from core.config import REQUIRED_REGISTRY_COLUMNS, TEMPLATE_DIR
from core.import_service import dataframe_to_csv_bytes, dataframe_to_xlsx_bytes, validate_uploaded_table

st.title("📥 Nhập & chuẩn hóa dữ liệu")
st.caption("Nhận CSV/Excel từ xã, phường hoặc đơn vị quản lý; kiểm tra trước khi đưa vào Asset Registry.")

st.info(
    "MVP v0.2 chỉ kiểm tra, chuẩn hóa và cho tải kết quả về. Hệ thống KHÔNG tự ghi đè dữ liệu gốc và chưa nhập trực tiếp vào CSDL chính thức."
)

st.markdown("### 1. Tải biểu mẫu chuẩn")
template = TEMPLATE_DIR / "DakTech_Asset_Import_Template_v0.2.xlsx"
if template.exists():
    st.download_button(
        "⬇️ Tải biểu mẫu Excel",
        data=template.read_bytes(),
        file_name=template.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.warning("Chưa tìm thấy biểu mẫu Excel trong gói cài đặt.")

st.caption("Các cột bắt buộc: " + ", ".join(REQUIRED_REGISTRY_COLUMNS))

st.markdown("### 2. Nạp tệp để kiểm tra")
uploaded = st.file_uploader("Chọn tệp CSV hoặc XLSX", type=["csv", "xlsx"])
if uploaded is not None:
    try:
        normalized, errors, summary = validate_uploaded_table(uploaded)
        c1, c2, c3 = st.columns(3)
        c1.metric("Số dòng", summary["rows"])
        c2.metric("Dòng ước tính hợp lệ", summary["valid_rows_estimate"])
        c3.metric("Lỗi phát hiện", summary["errors"])

        st.markdown("#### Dữ liệu sau chuẩn hóa")
        st.dataframe(normalized, use_container_width=True, hide_index=True)

        st.markdown("#### Kết quả kiểm tra")
        if errors.empty:
            st.success("Không phát hiện lỗi cấu trúc theo bộ kiểm tra của MVP v0.2.")
        else:
            st.error("Tệp còn lỗi. Cần xử lý trước khi đưa vào kho dữ liệu chính thức.")
            st.dataframe(errors, use_container_width=True, hide_index=True)

        left, right = st.columns(2)
        with left:
            st.download_button(
                "⬇️ Tải CSV đã chuẩn hóa",
                data=dataframe_to_csv_bytes(normalized),
                file_name="daktech_assets_normalized.csv",
                mime="text/csv",
            )
        with right:
            st.download_button(
                "⬇️ Tải Excel đã chuẩn hóa",
                data=dataframe_to_xlsx_bytes(normalized),
                file_name="daktech_assets_normalized.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    except Exception as exc:
        st.exception(exc)

st.markdown("### 3. Nguyên tắc khi nhập dữ liệu thật")
st.markdown(
    "- Giữ nguyên tệp nguồn và mã nguồn dữ liệu.\n"
    "- Không ghi đè lịch sử.\n"
    "- Dữ liệu mâu thuẫn phải gắn cờ để cán bộ xử lý.\n"
    "- Chỉ dữ liệu đã xác định nguồn, đơn vị chịu trách nhiệm và thời điểm cập nhật mới được đưa vào kho chính thức."
)
