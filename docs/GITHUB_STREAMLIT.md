# Đưa DakTech Infra AI lên GitHub và Streamlit

## GitHub
1. Tạo repository mới, ví dụ `daktech-infra-ai`.
2. Đưa toàn bộ nội dung thư mục này lên repository.
3. Không đưa `.streamlit/secrets.toml`, mật khẩu thật hoặc dữ liệu nội bộ lên repository công khai.

## Streamlit Community Cloud
1. Đăng nhập Streamlit Community Cloud bằng tài khoản phù hợp.
2. Tạo app mới từ repository GitHub.
3. Chọn entrypoint: `streamlit_app.py`.
4. Chọn Python version phù hợp trong Advanced settings trước khi deploy.
5. Deploy và kiểm tra đủ 4 phân hệ.

MVP dùng dữ liệu mô phỏng. Dữ liệu thật của cơ quan cần một kiến trúc triển khai riêng phù hợp yêu cầu bảo mật và quản trị dữ liệu.
