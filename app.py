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
HISTORY_FILE = "detection_history.json"
os.makedirs(CROP_FOLDER, exist_ok=True)

with open(PRICE_FILE, "r", encoding="utf-8") as f:
    price_map = json.load(f)

class_names = list(price_map.keys())

def preprocess_img(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
    img = tf.keras.utils.img_to_array(img) / 255.0
    return np.expand_dims(img, axis=0)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({"error": "Missing image data"}), 400

    if "," not in data['image']:
        return jsonify({"error": "Invalid base64 image format"}), 400

    img_data = data['image'].split(",")[1]
    img_bytes = base64.b64decode(img_data)
    img_array = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Invalid image format"}), 400

    # YOLO detect
    results = yolo_model.predict(source=frame, conf=0.3, save=False)[0]
    dishes, total = [], 0

    for i, box in enumerate(results.boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        crop = frame[y1:y2, x1:x2]

        # crop
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        crop_path = os.path.join(CROP_FOLDER, f"crop_{timestamp}_{i}.jpg")
        saved = cv2.imwrite(crop_path, crop)

        if not saved:
            continue  # bỏ qua nếu không lưu được ảnh

        # CNN predict
        input_tensor = preprocess_img(crop_path)
        pred = cnn_model.predict(input_tensor, verbose=0)[0]
        class_id = np.argmax(pred)
        class_name = class_names[class_id]
        price = price_map.get(class_name, 0)

        dishes.append({"name": class_name, "price": price})
        total += price

    order_id = "UEH" + datetime.now().strftime("%Y%m%d-%H%M%S")
    order_data = {
        "orderID": order_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": dishes,
        "total": total
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

    history.append(order_data)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return jsonify({"dishes": dishes, "total": total})

def edit_prices():
    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        price_map = json.load(f)
    return render_template("edit_price.html", price_map=price_map)

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

        return render_template("edit_price.html", price_map=price_map)

    except Exception as e:
        return f"Lỗi khi cập nhật: {e}", 500
    
@app.route('/view_prices')
def view_prices():
    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        price_map = json.load(f)
    return render_template("price.html", price_map=price_map)

@app.route("/view_orders")  
def view_history():
    try:
        with open("detection_history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    return render_template("view_order.html", history=history)
@app.route('/edit_prices')
def edit_prices():
    return render_template("edit_price.html", price_map=price_map)

if __name__ == '__main__':
    app.run(debug=True)
