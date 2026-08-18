import streamlit as st
import pandas as pd

st.title("🧩 Cấu trúc hệ thống DakTech Infra AI")
st.caption("Nhiều chế độ xem để hiểu nhanh GitHub, Streamlit, các phân hệ và luồng dữ liệu.")

view = st.radio(
    "Chọn chế độ xem",
    [
        "1. Tổng quan hệ sinh thái",
        "2. Cây sản phẩm",
        "3. Cây thư mục GitHub",
        "4. GitHub ↔ Streamlit",
        "5. Luồng dữ liệu nghiệp vụ",
        "6. Trạng thái các phân hệ",
    ],
    horizontal=True,
)

if view == "1. Tổng quan hệ sinh thái":
    st.subheader("Nền tảng mẹ và các phân hệ")
    c1, c2 = st.columns(2)
    with c1:
        st.info("⚱️ **DakCemetery AI**  \nQuản lý nghĩa trang và cơ sở hỏa táng  \n**Trọng tâm MVP v0.6.x**")
        st.info("🛣️ **DakRoad AI**  \nQuản lý kết cấu hạ tầng đường bộ  \n**Sản phẩm khởi nguồn**")
    with c2:
        st.info("💧 **DakWater AI**  \nQuản lý cấp nước sạch  \n**Khung phân hệ**")
        st.info("🌧️ **DakDrain AI**  \nQuản lý thoát nước và xử lý nước thải  \n**Khung phân hệ**")

    st.markdown("""
### Lõi dùng chung của DakTech Infra AI
- Đăng nhập và phân quyền.
- Kho dữ liệu và nguồn hồ sơ.
- Bản đồ.
- Bộ kiểm tra quy tắc dữ liệu.
- Quản lý phiên bản pháp lý.
- Luồng công việc và nhật ký xử lý.
- Dashboard điều hành.
- Trợ lý AI hỗ trợ, không thay thế thẩm quyền của cơ quan nhà nước.
""")

elif view == "2. Cây sản phẩm":
    st.subheader("Cây sản phẩm – nhìn theo chức năng quản lý")
    st.code("""DakTech Infra AI
│
├── DakCemetery AI (Quản lý nghĩa trang)
│   ├── Dashboard nghĩa trang
│   ├── Danh mục nghĩa trang
│   ├── Hàng đợi rà soát
│   ├── Bản đồ nghĩa trang
│   ├── Hồ sơ nghĩa trang 360°
│   ├── Kho báo cáo nghĩa trang
│   └── Mô phỏng nạp báo cáo
│
├── DakRoad AI (Quản lý kết cấu hạ tầng đường bộ)
│
├── DakWater AI (Quản lý cấp nước sạch)
│
└── DakDrain AI (Quản lý thoát nước và xử lý nước thải)
""", language="text")
    st.caption("Đây là cây nghiệp vụ/sản phẩm, không nhất thiết trùng 1:1 với cây thư mục kỹ thuật.")

elif view == "3. Cây thư mục GitHub":
    st.subheader("Cây thư mục GitHub – nhìn theo nơi lưu mã")
    st.code("""DakTech-Infra-AI/
│
├── modules/                    # Trang giới thiệu từng phân hệ
│   ├── dakcemetery-ai/         # Quản lý nghĩa trang
│   ├── dakroad-ai/             # Quản lý đường bộ
│   ├── dakwater-ai/            # Quản lý cấp nước
│   └── dakdrain-ai/            # Quản lý thoát nước
│
├── pages/                      # Các màn hình Streamlit
├── core/                       # Lõi dùng chung
├── data/                       # Dữ liệu demo/an toàn công khai
├── config/                     # Cấu hình
├── docs/                       # Tài liệu kiến trúc và hướng dẫn
├── templates/                  # Biểu mẫu
├── tests/                      # Kiểm thử
├── legacy_dakroad/             # Phần kế thừa DakRoad AI cũ
├── streamlit_app.py            # Điểm khởi động website
├── requirements.txt            # Thư viện Python cần dùng
└── README.md                   # Trang giới thiệu chính
""", language="text")
    st.warning(
        "GitHub mặc định hiển thị danh sách thư mục chứ không phải cây bung/mở như Windows Explorer. "
        "Trang này tạo 'chế độ xem cây' để cán bộ nhìn cấu trúc dễ hơn."
    )

elif view == "4. GitHub ↔ Streamlit":
    st.subheader("Bản đồ liên kết GitHub ↔ Streamlit")
    df = pd.DataFrame([
        ["streamlit_app.py", "Khởi động ứng dụng và tạo menu", "Thanh menu bên trái"],
        ["pages/home.py", "Dashboard điều hành chung", "Dashboard lãnh đạo"],
        ["pages/system_views.py", "Nhiều chế độ xem cấu trúc", "Cấu trúc hệ thống"],
        ["pages/cemetery_dashboard.py", "Dashboard phân hệ nghĩa trang", "Dashboard nghĩa trang"],
        ["pages/cemetery_inventory.py", "Danh mục ứng viên/chính thức", "Danh mục nghĩa trang"],
        ["pages/cemetery_review_queue.py", "Hàng đợi P1/P2/P3", "Hàng đợi rà soát"],
        ["pages/cemetery_map.py", "Bản đồ nghĩa trang", "Bản đồ nghĩa trang"],
        ["pages/cemetery_sources.py", "Kho nguồn báo cáo", "Kho báo cáo nghĩa trang"],
        ["core/", "Xử lý nghiệp vụ dùng chung", "Không hiện trực tiếp; phục vụ các trang"],
        ["data/", "Dữ liệu demo/an toàn công khai", "Nguồn cho bảng, biểu đồ, bản đồ"],
        ["modules/", "Giới thiệu cấu trúc sản phẩm", "Tham chiếu quản trị GitHub"],
        ["docs/", "Tài liệu hướng dẫn/kiến trúc", "Tham chiếu quản trị"],
    ], columns=["Vị trí trên GitHub", "Vai trò", "Nhìn thấy trên Streamlit"])
    st.dataframe(df, width="stretch", hide_index=True)

elif view == "5. Luồng dữ liệu nghiệp vụ":
    st.subheader("Luồng dữ liệu – từ hồ sơ nguồn đến dashboard")
    st.code("""Hồ sơ nguồn
   ↓
Nạp / ghi nhận nguồn
   ↓
Danh mục ứng viên
   ↓
Chuẩn hóa tên + địa bàn + loại hình
   ↓
Kiểm tra quy tắc / gắn cờ
   ↓
Hàng đợi P1 / P2 / P3
   ↓
Cán bộ đối chiếu và xác minh
   ↓
Danh mục chính thức
   ↓
Hồ sơ 360° + Bản đồ + Dashboard
""", language="text")
    st.info(
        "AI và bộ quy tắc chỉ hỗ trợ phát hiện, sắp xếp và gợi ý. "
        "Kết quả chính thức phải qua xác minh của cán bộ có trách nhiệm."
    )

elif view == "6. Trạng thái các phân hệ":
    st.subheader("Trạng thái phát triển")
    df = pd.DataFrame([
        ["DakCemetery AI", "Quản lý nghĩa trang", "Đang phát triển sâu", "MVP v0.6.x", "Dữ liệu thực tế + hàng đợi xác minh"],
        ["DakRoad AI", "Đường bộ", "Có sản phẩm khởi nguồn", "Kế thừa", "Chuẩn hóa để tích hợp sâu vào nền tảng mẹ"],
        ["DakWater AI", "Cấp nước sạch", "Khung phân hệ", "Khung", "Xây bộ dữ liệu và nghiệp vụ"],
        ["DakDrain AI", "Thoát nước, nước thải", "Khung phân hệ", "Khung", "Xây bộ dữ liệu và nghiệp vụ"],
    ], columns=["Phân hệ", "Nghĩa tiếng Việt", "Trạng thái", "Mức hiện tại", "Bước tiếp theo"])
    st.dataframe(df, width="stretch", hide_index=True)

st.divider()
st.caption(
    "MVP v0.6.1 – bổ sung nhiều chế độ xem để nắm cấu trúc, quản lý và khai thác GitHub/Streamlit thuận tiện hơn."
)
