from pathlib import Path
import streamlit as st

from core.config import TEMPLATE_DIR, VERSION

st.title("📥 Mô phỏng nạp báo cáo nghĩa trang")
st.caption("Bản Public chỉ hướng dẫn và kiểm chứng biểu mẫu; không tiếp nhận hồ sơ nội bộ thật.")

st.warning(
    "Không tải báo cáo nội bộ, dữ liệu cá nhân hoặc hồ sơ chưa được phép công khai lên website demo này. "
    "Chức năng nạp dữ liệu thật được để dành cho môi trường nội bộ/riêng tư."
)

st.markdown("### Quy trình nạp báo cáo trong bản nội bộ")
st.markdown(
    "1. Giữ nguyên tệp báo cáo gốc và cấp mã nguồn.\n"
    "2. Đọc bảng CSV/XLSX, chọn sheet.\n"
    "3. Ghép cột báo cáo vào bộ trường chuẩn.\n"
    "4. Tạo mã tạm cho bản ghi chưa có mã tài sản.\n"
    "5. Chạy Bộ kiểm tra quy tắc dữ liệu.\n"
    "6. Xuất bản chuẩn hóa chờ cán bộ xác minh.\n"
    "7. Chỉ sau xác minh mới cấp mã chính thức và đưa vào danh mục quản lý."
)

st.markdown("### Biểu mẫu tham khảo")
template = TEMPLATE_DIR / "DakCemetery_Bieu_mau_du_lieu_v0.4.xlsx"
if template.exists():
    st.download_button(
        "Tải biểu mẫu DakCemetery",
        data=template.read_bytes(),
        file_name=template.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("Chưa có biểu mẫu trong gói triển khai.")

st.info(f"{VERSION}: dữ liệu thật được tách khỏi GitHub Public theo nguyên tắc bảo vệ dữ liệu và quản trị nguồn.")
