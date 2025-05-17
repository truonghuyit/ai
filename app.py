from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import base64, os, cv2, json
from datetime import datetime

app = Flask(__name__)

# === Load models ===
yolo_model = YOLO("yolo11n.pt")
cnn_model = load_model("cnn-cls.h5")

# === Setup paths and load prices ===
PRICE_FILE = "price_map.json"
CROP_FOLDER = "static/cropped"
os.makedirs(CROP_FOLDER, exist_ok=True)

with open(PRICE_FILE, "r", encoding="utf-8") as f:
    price_map = json.load(f)

class_names = list(price_map.keys())

# === Image preprocessing for CNN ===
def preprocess_img(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
    img = tf.keras.utils.img_to_array(img) / 255.0
    return np.expand_dims(img, axis=0)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "Missing image data"}), 400

        # Decode base64 image
        img_data = data['image'].split(",")[1]
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid image format"}), 400

        # YOLO detection
        results = yolo_model.predict(source=frame, conf=0.3, save=False)[0]
        dishes, total = [], 0

        for i, box in enumerate(results.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box)
            crop = frame[y1:y2, x1:x2]

            # Save cropped image
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            crop_path = os.path.join(CROP_FOLDER, f"crop_{timestamp}_{i}.jpg")
            cv2.imwrite(crop_path, crop)

            # CNN prediction
            input_tensor = preprocess_img(crop_path)
            pred = cnn_model.predict(input_tensor, verbose=0)[0]
            class_id = np.argmax(pred)
            class_name = class_names[class_id]
            price = price_map.get(class_name, 0)

            dishes.append({"name": class_name, "price": price})
            total += price

        return jsonify({"dishes": dishes, "total": total})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/edit_prices')
def edit_prices():
    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        price_map = json.load(f)
    return render_template("history.html", price_map=price_map)

@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        form_data = request.form.to_dict(flat=False)
        updated_prices = {}

        for key, val in form_data.items():
            if key.startswith("prices[") and key.endswith("]"):
                name = key[7:-1]
                try:
                    updated_prices[name] = int(val[0])
                except ValueError:
                    updated_prices[name] = 0

        with open(PRICE_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_prices, f, ensure_ascii=False, indent=2)

        global price_map, class_names
        price_map = updated_prices
        class_names = list(price_map.keys())

        return render_template("history.html", price_map=price_map)

    except Exception as e:
        return f"Lỗi khi cập nhật: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
