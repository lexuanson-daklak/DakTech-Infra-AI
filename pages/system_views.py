import streamlit as st
import pandas as pd

st.title("🧩 Cấu trúc hệ thống DakTech Infra AI")
st.caption("Cách nhìn trực quan để nắm hệ thống mà không cần đọc tên file kỹ thuật.")

view = st.radio(
    "Chọn chế độ xem",
    [
        "1. Tổng quan hệ sinh thái",
        "2. Cây sản phẩm",
        "3. Cây thư mục GitHub",
        "4. Liên hệ GitHub ↔ Streamlit",
        "5. Luồng dữ liệu nghiệp vụ",
        "6. Trạng thái các phân hệ",
    ],
    horizontal=True,
)

if view == "1. Tổng quan hệ sinh thái":
    st.subheader("Nền tảng mẹ và các phân hệ")
    c1, c2 = st.columns(2)
    with c1:
        st.success("💧 **DakWater AI**  \nQuản lý cấp nước sạch  \n**Đang phát triển trọng tâm**")
        st.info("🛣️ **DakRoad AI**  \nQuản lý kết cấu hạ tầng đường bộ  \nSản phẩm khởi nguồn")
    with c2:
        st.success("🌧️ **DakDrain AI**  \nQuản lý thoát nước và xử lý nước thải  \n**Đang phát triển trọng tâm**")
        st.warning("⚱️ **DakCemetery AI**  \nQuản lý nghĩa trang  \nTạm dừng tại phiên bản v0.6.x")

    st.subheader("Lõi dùng chung")
    st.markdown("""
- Quản lý người dùng và phân quyền.
- Kho dữ liệu và nguồn hồ sơ.
- Bản đồ.
- Kiểm tra chất lượng dữ liệu.
- Quản lý phiên bản cơ sở pháp lý.
- Luồng công việc và nhật ký xử lý.
- Bảng điều hành.
- **Trung tâm xuất dữ liệu**.
- Trợ lý AI hỗ trợ; không thay thế thẩm quyền của cơ quan nhà nước.
""")

elif view == "2. Cây sản phẩm":
    st.code("""DakTech Infra AI
│
├── DakWater AI
│   └── Quản lý cấp nước sạch              ← đang phát triển
│
├── DakDrain AI
│   └── Quản lý thoát nước và nước thải    ← đang phát triển
│
├── DakRoad AI
│   └── Quản lý kết cấu hạ tầng đường bộ   ← sản phẩm khởi nguồn
│
└── DakCemetery AI
    └── Quản lý nghĩa trang                ← tạm dừng
""", language="text")

elif view == "3. Cây thư mục GitHub":
    st.code("""DakTech-Infra-AI/
├── modules/
│   ├── dakwater-ai/        (Quản lý cấp nước sạch)
│   ├── dakdrain-ai/        (Quản lý thoát nước và xử lý nước thải)
│   ├── dakroad-ai/         (Quản lý kết cấu hạ tầng đường bộ)
│   └── dakcemetery-ai/     (Quản lý nghĩa trang)
├── pages/                  Các màn hình Streamlit
├── core/                   Lõi xử lý dùng chung
├── data/                   Dữ liệu mẫu/an toàn công khai
├── docs/                   Tài liệu và quy chuẩn
├── templates/              Biểu mẫu
├── tests/                  Kiểm thử
├── streamlit_app.py        Điểm khởi động Streamlit
└── README.md               Trang giới thiệu chính
""", language="text")
    st.info("Tên file kỹ thuật chỉ phục vụ GitHub. Người dùng Streamlit không phải nhìn các tên file này.")

elif view == "4. Liên hệ GitHub ↔ Streamlit":
    df = pd.DataFrame([
        ["pages/water_dashboard.py", "Bảng điều hành cấp nước"],
        ["pages/water_inventory.py", "Danh mục công trình cấp nước"],
        ["pages/water_export_center.py", "Trung tâm xuất dữ liệu cấp nước"],
        ["pages/drain_dashboard.py", "Bảng điều hành thoát nước"],
        ["pages/drain_inventory.py", "Danh mục công trình thoát nước"],
        ["pages/drain_export_center.py", "Trung tâm xuất dữ liệu thoát nước"],
        ["core/export_center.py", "Lõi xuất dữ liệu dùng chung"],
        ["data/", "Nguồn dữ liệu mẫu/an toàn công khai"],
        ["modules/", "Cấu trúc sản phẩm trên GitHub"],
    ], columns=["Vị trí kỹ thuật trên GitHub", "Tên chức năng người dùng nhìn thấy"])
    st.dataframe(df, width="stretch", hide_index=True)

elif view == "5. Luồng dữ liệu nghiệp vụ":
    st.code("""Hồ sơ nguồn
   ↓
Dữ liệu ứng viên
   ↓
Chuẩn hóa và kiểm tra
   ↓
Cán bộ rà soát / xác minh
   ↓
Danh mục quản lý
   ↓
Bản đồ + Hồ sơ 360° + Bảng điều hành
   ↓
Trung tâm xuất dữ liệu
""", language="text")
    st.info("Người dùng tải dữ liệu trực tiếp từ Streamlit; không cần vào GitHub.")

else:
    df = pd.DataFrame([
        ["DakWater AI", "Quản lý cấp nước sạch", "Đang phát triển trọng tâm", "v0.7.2"],
        ["DakDrain AI", "Quản lý thoát nước và xử lý nước thải", "Đang phát triển trọng tâm", "v0.7.2"],
        ["DakRoad AI", "Quản lý kết cấu hạ tầng đường bộ", "Kế thừa/sản phẩm khởi nguồn", "Đang tích hợp"],
        ["DakCemetery AI", "Quản lý nghĩa trang", "Tạm dừng", "v0.6.x"],
    ], columns=["Phân hệ", "Chức năng tiếng Việt", "Trạng thái", "Phiên bản/mức hiện tại"])
    st.dataframe(df, width="stretch", hide_index=True)

st.divider()
st.caption("MVP = phiên bản thử nghiệm nhỏ nhất nhưng có thể chạy và kiểm chứng được.")
