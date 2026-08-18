import streamlit as st
import pandas as pd

st.title("🧱 DakDrain AI – Mô hình dữ liệu thoát nước và xử lý nước thải")
st.caption("Khung quản trị dữ liệu để chuẩn bị tiếp nhận dữ liệu thực tế.")

st.code("""Lưu vực
   ↓
Tuyến cống / hố ga / cửa thu
   ↓
Trạm bơm
   ↓
Nhà máy xử lý nước thải
   ↓
Điểm xả / nguồn tiếp nhận

Điểm ngập
   ↘ liên kết với lưu vực + tuyến cống + công trình liên quan
""", language="text")

tabs = st.tabs(["Lưu vực","Mạng thoát nước","Điểm ngập","XLNT & điểm xả","Rà soát dữ liệu"])
with tabs[0]:
    st.write("Lưu vực là lớp tổ chức không gian để gom tuyến cống, điểm ngập, trạm bơm và công trình xử lý.")
with tabs[1]:
    st.dataframe(pd.DataFrame([
        ["Tuyến cống","Mã tuyến, điểm đầu/cuối, chiều dài, kích thước, vật liệu, độ dốc"],
        ["Hố ga/cửa thu","Mã, tọa độ, liên kết tuyến, tình trạng"],
        ["Trạm bơm","Công suất, số bơm, tình trạng vận hành"],
    ], columns=["Đối tượng","Trường quản lý tối thiểu"]), width="stretch", hide_index=True)
with tabs[2]:
    st.write("Điểm ngập cần tối thiểu: tọa độ, lưu vực, nguyên nhân/kích hoạt, độ sâu, thời gian ngập, tần suất, tuyến cống liên quan, mức ưu tiên.")
with tabs[3]:
    st.write("Nhà máy xử lý nước thải/điểm xả cần: công suất thiết kế/khai thác, nguồn tiếp nhận, giấy phép/trạng thái hồ sơ, đơn vị quản lý và nguồn dữ liệu.")
with tabs[4]:
    st.info("Nguyên tắc: dữ liệu ứng viên không tự động trở thành dữ liệu chính thức; AI chỉ hỗ trợ phát hiện thiếu, mâu thuẫn và ưu tiên rà soát.")
