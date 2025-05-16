from flask import Flask, request, jsonify
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64, os, cv2, json
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# === Load mô hình YOLO và CNN ===
yolo_model = YOLO("yolo11n.pt")
cnn_model = load_model("cnn-cls.h5")

# === Đường dẫn và file giá ===
PRICE_FILE = "price_map.json"
CROP_FOLDER = "static/cropped"
os.makedirs(CROP_FOLDER, exist_ok=True)

# === Load bảng giá ===
with open(PRICE_FILE, "r", encoding="utf-8") as f:
    price_map = json.load(f)

class_names = list(price_map.keys())

# === Tiền xử lý ảnh cho CNN ===
def preprocess_img(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
    img = tf.keras.utils.img_to_array(img)
    img = img / 255.0
    return np.expand_dims(img, axis=0)
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        # B1: Nhận và giải mã ảnh base64
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "Missing image data"}), 400

        img_data = data['image'].split(",")[1]
        img_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Invalid image"}), 400

        # B2: YOLO detect các bounding boxes
        results = yolo_model.predict(source=frame, save=False, conf=0.3)[0]
        dishes = []
        total = 0

        for i, box in enumerate(results.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box)
            crop_img = frame[y1:y2, x1:x2]

            # Lưu ảnh crop
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            crop_path = os.path.join(CROP_FOLDER, f"crop_{timestamp}_{i}.jpg")
            cv2.imwrite(crop_path, crop_img)

            # B3: Dự đoán class bằng CNN
            processed = preprocess_img(crop_path)
            pred = cnn_model.predict(processed, verbose=0)[0]
            class_id = np.argmax(pred)
            class_name = class_names[class_id]
            price = price_map.get(class_name, 0)

            dishes.append({
                "name": class_name,
                "price": price
            })
            total += price

        return jsonify({
            "dishes": dishes,
            "total": total
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        # Lấy dữ liệu từ form gửi về
        raw_prices = request.form.to_dict(flat=False)  # {'prices[canhchua]': ['20000'], ...}
        updated = {}

        for key, value in raw_prices.items():
            if key.startswith("prices[") and key.endswith("]"):
                dish_name = key[7:-1]  # Trích xuất tên món
                try:
                    updated[dish_name] = int(value[0])
                except:
                    updated[dish_name] = 0  # fallback nếu không hợp lệ

        # Ghi lại vào JSON
        with open(PRICE_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)

        # Cập nhật lại biến toàn cục
        global price_map, class_names
        price_map = updated
        class_names = list(price_map.keys())

        return render_template("history.html", price_map=price_map)

    except Exception as e:
        return f"Lỗi khi cập nhật: {e}", 500
@app.route('/edit_prices', methods=['GET'])
def edit_prices():
    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        price_map = json.load(f)
    return render_template("history.html", price_map=price_map)

if __name__ == '__main__':
    app.run(debug=True)
