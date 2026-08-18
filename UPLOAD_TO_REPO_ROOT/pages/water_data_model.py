import streamlit as st
import pandas as pd

st.title("🧱 DakWater AI – Mô hình dữ liệu cấp nước")
st.caption("Khung quản trị dữ liệu để chuẩn bị tiếp nhận dữ liệu thực tế.")

st.code("""Nguồn nước
   ↓
Nhà máy / trạm cấp nước
   ↓
Tuyến ống truyền tải
   ↓
Mạng phân phối
   ↓
Vùng phục vụ
   ↓
Hộ dân / dân số phục vụ
   ↓
Vận hành – chất lượng – thất thoát – sự cố – đầu tư
""", language="text")

tabs = st.tabs(["Nguồn nước","Công trình","Mạng lưới","Vùng phục vụ","Rà soát dữ liệu"])
with tabs[0]:
    st.dataframe(pd.DataFrame([
        ["Mã nguồn","Định danh nguồn nước"],
        ["Tên nguồn","Tên sông/hồ/giếng/nguồn theo hồ sơ"],
        ["Loại nguồn","Nước mặt / nước ngầm"],
        ["Công suất","Cấp phép / quan trắc / khai thác"],
        ["Chất lượng","Theo hồ sơ/quan trắc"],
        ["Rủi ro mùa khô","Cờ quản trị, không phải kết luận pháp lý"],
    ], columns=["Nhóm trường","Ý nghĩa"]), width="stretch", hide_index=True)
with tabs[1]:
    st.dataframe(pd.DataFrame([
        ["Nhà máy/trạm","Tên, mã, tọa độ, địa bàn"],
        ["Công suất","Thiết kế và khai thác"],
        ["Đơn vị quản lý","Chủ quản/vận hành theo nguồn"],
        ["Trạng thái","Hoạt động/cần rà soát/..."],
        ["Nguồn hồ sơ","source_id để truy vết"],
    ], columns=["Nhóm trường","Ý nghĩa"]), width="stretch", hide_index=True)
with tabs[2]:
    st.write("Tuyến ống cần quản lý tối thiểu: mã tuyến, loại tuyến, điểm đầu/cuối, chiều dài, đường kính, vật liệu, vùng áp lực, đơn vị quản lý, nguồn hồ sơ.")
with tabs[3]:
    st.write("Vùng phục vụ cần quản lý tối thiểu: địa bàn, công trình cấp, dân số/hộ phục vụ, tỷ lệ bao phủ, thời gian cấp nước, thất thoát và nguồn xác minh.")
with tabs[4]:
    st.info("Nguyên tắc: hồ sơ nguồn giữ nguyên → dữ liệu ứng viên → kiểm tra/chuẩn hóa → cán bộ xác minh → danh mục quản lý chính thức.")
