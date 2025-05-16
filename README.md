 Food Recognition & Pricing System with YOLO + Flask
Hệ thống này sử dụng mô hình YOLO để phát hiện món ăn từ ảnh chụp khay cơm và Flask để xây dựng giao diện web hiển thị kết quả, tên món, giá tiền và tổng hóa đơn.

🔧 Yêu cầu hệ thống
Python 3.10+

pip (Python package installer)

Git (nếu clone từ GitHub)

⚙️ Cài đặt
1. Tạo môi trường ảo (virtual environment)
bash
Sao chép
Chỉnh sửa
python -m venv yolo
2. Kích hoạt môi trường ảo
Windows:

bash
Sao chép
Chỉnh sửa
yolo\Scripts\activate
Mac/Linux:

bash
Sao chép
Chỉnh sửa
source yolo/bin/activate
3. Cài đặt các thư viện cần thiết
bash
Sao chép
Chỉnh sửa
pip install flask
pip install ultralytics
❗ Lưu ý: Bạn có thể thêm các thư viện khác như opencv-python, tensorflow, Pillow, v.v... tùy vào cấu trúc dự án.

🚀 Chạy ứng dụng Flask
bash
Sao chép
Chỉnh sửa
python app.py
Ứng dụng sẽ khởi động tại http://127.0.0.1:5000 hoặc địa chỉ bạn cấu hình trong app.py.

📂 Cấu trúc thư mục mẫu
php
Sao chép
Chỉnh sửa
project/
│
├── app.py                 # Flask server
├── yolov8_model.pt        # Trained YOLO model
├── best_food_model.tflite # (Tùy chọn) Model phân loại món ăn
├── static/
│   └── cropped/           # Ảnh sau khi crop từ YOLO
├── templates/
│   └── index.html         # Giao diện HTML Flask
├── menu.json              # Danh sách món và giá
└── README.md
