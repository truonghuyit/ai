
# 🍱 NHẬN DIỆN MÓN - THANH TOÁN TỨC THÌ
**Phát hiện món ăn và tính giá tiền tự động bằng YOLOv11 + Flask**

---
![image](https://github.com/user-attachments/assets/b8291156-827a-4106-9b07-7381bab2d17e)


## 🧠 Giới thiệu  
Hệ thống sử dụng **YOLOv11** để phát hiện các món ăn từ ảnh chụp khay cơm và **CNN** để phân loại từng món. Kết quả sẽ được hiển thị trên giao diện **web Flask**, bao gồm:

- Tên từng món ăn  
- Giá tiền theo menu  
- Tổng hóa đơn  
✔️ Giao diện đơn giản, dễ sử dụng  
✔️ Hỗ trợ chỉnh sửa giá món ăn qua file `price_map.json`  
✔️ Có trang web để **chỉnh sửa giá tiền trực tiếp**

---

## 🔧 Yêu cầu hệ thống
- Python >= 3.10  
- pip (Python package installer)  
- Git (nếu cài đặt qua GitHub)

---

## ⚙️ Cài đặt

### 1. Clone hoặc tải dự án
```bash
git clone https://github.com/truonghuyit/ai.git
cd ai
```

### 2. Tạo môi trường ảo
```bash
python -m venv yolo
```

### 3. Kích hoạt môi trường ảo  
**Windows:**
```bash
yolo\Scripts\activate
```
**macOS/Linux:**
```bash
source yolo/bin/activate
```

### 4. Cài đặt thư viện cần thiết
```bash
pip install flask ultralytics tensorflow opencv-python pillow
```

---

## 🚀 Chạy ứng dụng Flask
```bash
python app.py
```
Ứng dụng sẽ chạy tại: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Cấu trúc thư mục mẫu
```
project/
│
├── app.py                   # Flask server
├── YOLOv11n.pt              # YOLOv11 model phát hiện món ăn
├── best_food_model.tflite   # TFLite model phân loại món ăn
├── price_map.json           # Tên món ăn và giá tiền
│
├── static/
│   └── cropped/             # Ảnh sau khi YOLO cắt
│
├── templates/
│   ├── index.html           # Giao diện chính
│   └── history.html      # Giao diện chỉnh sửa giá
```

---

## 🛠️ Tùy chỉnh & Mở rộng

### 📝 Thay đổi tên món và giá
- Mở file `price_map.json` và chỉnh sửa theo cấu trúc:
```json
{
  "Ga chien": 20000,
  "Com trang": 5000,
  "Thit kho": 18000
}
```
Hoặc mở [http://127.0.0.1:5000/edit](http://127.0.0.1:5000/edit) để chỉnh giá qua giao diện web.

### 📈 Mở rộng thêm món ăn
- Cập nhật `class_names` trong mã nguồn CNN (nếu dùng).
- Đảm bảo nhãn món ăn khớp với các tên trong `price_map.json`.

---

## 📸 Demo
> Tải ảnh khay cơm → Hệ thống tự phát hiện & phân loại từng món → In kết quả tên, giá & tổng tiền.
![image](https://github.com/user-attachments/assets/a831b0d4-3de6-4580-b728-ac93040d8ace)
![image](https://github.com/user-attachments/assets/06dc2c8b-7b14-4c7b-9af8-fd501f8d2368)

---
