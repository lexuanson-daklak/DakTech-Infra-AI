# QUY CHUẨN MENU STREAMLIT v1.0

Áp dụng bắt buộc cho toàn bộ hệ sinh thái GitHub + Streamlit.

1. Giao diện người dùng dùng tiếng Việt làm ngôn ngữ chính.
2. Không hiển thị tên file kỹ thuật trong menu.
3. Không dùng menu tự sinh từ thư mục `pages/`.
4. Dùng `st.navigation(..., position="hidden")` để đăng ký trang.
5. Dùng `st.page_link` để dựng menu nghiệp vụ riêng.
6. Đặt `client.showSidebarNavigation = false` trong `.streamlit/config.toml` làm lớp bảo vệ.
7. `Dashboard` trên giao diện gọi là **Bảng điều hành**.
8. DakWater AI và DakDrain AI là hai phân hệ trọng tâm hiện tại.
9. DakCemetery AI được gom vào nhóm **Phân hệ tạm dừng**.
10. Mỗi phân hệ quản trị dữ liệu bắt buộc có **Trung tâm xuất dữ liệu**.
11. Người dùng nghiệp vụ không cần vào GitHub để lấy dữ liệu.
