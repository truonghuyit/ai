# 🍱 NHẬN DIỆN MÓN ĂN & THANH TOÁN TỨC THÌ

**Tự động phát hiện món ăn, phân loại, tính tiền và xuất hóa đơn bằng YOLOv11 + CNN + Flask**
![image](https://github.com/user-attachments/assets/79fc5414-ab65-4152-a289-e49e1c6047fc)

---

## 🧠 Giới thiệu

Hệ thống sử dụng:
- 🔍 **YOLOv11** để phát hiện món ăn từ ảnh khay cơm
- 🧠 **CNN** để phân loại từng món
- 💰 Tự động tính tiền từ `price_map.json`
- 💳 Tạo **mã QR chuyển khoản VietQR**
- 🧾 **Xuất hóa đơn PDF**
- 🕘 **Lưu lịch sử giao dịch**
- 🖥️ Giao diện web bằng Flask, hỗ trợ chỉnh sửa giá động

---

## 🔧 Yêu cầu hệ thống

- Python >= 3.10  
- pip (Python package installer)  
- Git

---

## ⚙️ Cài đặt

```bash
git clone https://github.com/truonghuyit/ai.git
cd ai
python -m venv 3ITech
# Windows:
3ITech\Scripts\activate
# macOS/Linux:
source 3ITech/bin/activate
pip install flask ultralytics tensorflow opencv-python pillow
```

---

## 🚀 Chạy ứng dụng Flask

```bash
python app.py
```

Truy cập: http://127.0.0.1:5000

---

## 📂 Cấu trúc dự án

```
project/
├── app.py                   # Flask server chính
├── YOLOv11n.pt              # Mô hình YOLO phát hiện món
├── cnn.h5                   # Mô hình CNN phân loại món
├── price_map.json           # Bảng tên món ăn và giá
├── templates/
│   ├── index.html           # Giao diện nhận diện & tính tiền
│   └── edit_price.html      # Giao diện chỉnh sửa giá & xem lịch sử
├── static/
│   └── cropped/             # Ảnh món ăn sau khi YOLO cắt
```

---

## ✨ Tính năng chính

### 🔍 Phát hiện & phân loại

- YOLOv11 nhận diện vị trí món
- CNN phân loại từng món
- Tính tiền tự động dựa trên `price_map.json`

### 💳 QR chuyển khoản

- Tạo mã QR VietQR tự động theo tổng tiền
- Chuyển khoản chính xác, nội dung kèm xác minh
![image](https://github.com/user-attachments/assets/469ee8b2-f9bd-48f3-a4ae-6c98bc94c812)

### 🧾 Xuất hóa đơn PDF

- Tên món, giá, thời gian, tổng tiền
- Kèm ảnh mã QR trong file PDF

![image](https://github.com/user-attachments/assets/6594be01-bd99-44f1-b6b8-f85ed0a0877d)

## 🛠️ Quản lý giá món ăn
![image](https://github.com/user-attachments/assets/6e74ff41-db82-4498-8252-03abf28c79c3)


Chỉnh trong `price_map.json`:
```json
{
  "Ga chien": 20000,
  "Com trang": 5000,
  "Thit kho": 18000
}
```

Hoặc truy cập giao diện:
```
http://127.0.0.1:5000/edit_prices
```
![image](https://github.com/user-attachments/assets/72c4d749-38e6-4955-9662-1dc1a77ac6da)

---

## 📸 Demo hoạt động

> Chụp hoặc tải ảnh khay → nhận diện → phân loại → tính tiền → mã QR → hóa đơn PDF
![image](https://github.com/user-attachments/assets/793ccfae-c1f1-49c2-8822-cdaa6c84c551)

