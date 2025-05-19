const webcam = document.getElementById("webcam");
const canvas = document.getElementById("captureCanvas");
const context = canvas.getContext("2d");
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (webcam.srcObject = stream))
  .catch((err) => console.error("Webcam không hoạt động:", err));
let allDishes = [];

function generateOrderID() {
  const today = new Date();
  const dateStr = today.toISOString().slice(0, 10).replace(/-/g, "");
  let count =
    parseInt(localStorage.getItem("orderCount_" + dateStr) || "0") + 1;
  localStorage.setItem("orderCount_" + dateStr, count);
  return `HD${dateStr}-${String(count).padStart(4, "0")}`;
}
async function xuathoadon() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  const orderID = generateOrderID();
  const now = new Date();
  const timestamp = now.toLocaleString();

  // Title
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(18);
  doc.text("INVOICE", 85, 20);

  // Order ID and timestamp
  doc.setFontSize(10);
  doc.setFont("Helvetica", "normal");
  doc.text(`Order ID: ${orderID}`, 20, 28);
  doc.text(`Date: ${timestamp}`, 120, 28);

  // Dish list
  doc.setFontSize(12);
  let y = 38;
  allDishes.forEach((dish, i) => {
    const itemText = `${dish.name} x1`;
    const priceText = `${dish.price.toLocaleString()} VND`;
    doc.text(itemText, 20, y);
    doc.text(priceText, 160 - priceText.length * 2.5, y); // right aligned
    y += 8;
  });

  // Total
  y += 5;
  const total = allDishes.reduce((acc, d) => acc + d.price, 0);
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(14);
  doc.text(`TOTAL: ${total.toLocaleString()} VND`, 20, y);
  y += 10;

  // QR Code
  const qrImage = document.getElementById("qr-code-img");
  if (qrImage && qrImage.src) {
    const img = new Image();
    img.src = qrImage.src;
    await new Promise((resolve) => {
      img.onload = () => {
        doc.addImage(img, "PNG", 70, y, 60, 60);
        resolve();
      };
    });
  }
  y += 70;

  // Payment Instructions
  doc.setFont("Helvetica", "normal");
  doc.setFontSize(11);
  doc.text("PAYMENT INSTRUCTIONS", 65, y);
  y += 7;
  doc.text(`Amount: ${total.toLocaleString()} VND`, 70, y);
  y += 7;
  doc.text("1. Open your banking app", 50, y);
  y += 6;
  doc.text("2. Scan the QR code above", 50, y);
  y += 6;
  doc.text("3. Verify information and confirm payment", 50, y);
  y += 10;

  doc.setFont("Helvetica", "bold");
  doc.setFontSize(10);
  doc.setTextColor(0, 0, 0);
  doc.text("Thank you for using our service!", 40, y);

  // Save as PDF
  doc.save(`invoice_${orderID}.pdf`);
}

function captureAndDetect() {
  canvas.width = webcam.videoWidth;
  canvas.height = webcam.videoHeight;
  context.drawImage(webcam, 1, 0);
  const imageDataURL = canvas.toDataURL("image/jpeg");
  showPreviewImage(imageDataURL);
  sendImageToServer(imageDataURL);
}

function handleUpload(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function (e) {
    const base64Image = e.target.result;
    showPreviewImage(base64Image);
    sendImageToServer(base64Image);
  };
  reader.readAsDataURL(file);
}

function showPreviewImage(base64Image) {
  const imgEl = document.createElement("img");
  imgEl.src = base64Image;
  document.getElementById("captured-images").appendChild(imgEl);
}

function sendImageToServer(base64Image) {
  const loading = document.getElementById("loading-indicator");
  loading.style.display = "block";
  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: base64Image }),
  })
    .then((res) => res.json())
    .then((data) => {
      loading.style.display = "none";
      if (data.error) {
        alert("Lỗi xử lý ảnh: " + data.error);
        return;
      }
      if (data.dishes) {
        allDishes = allDishes.concat(data.dishes);
        renderDishList();
      } else {
        alert("Không phát hiện món ăn nào.");
      }
    })
    .catch((err) => {
      loading.style.display = "none";
      console.error("Lỗi gửi ảnh:", err);
      alert("Không kết nối được với server.");
    });
}

function renderDishList() {
  const container = document.getElementById("dish-items");
  const totalText = document.getElementById("total-price");
  const qrCodeImg = document.getElementById("qr-code-img");
  container.innerHTML = "";
  let total = 0;
  allDishes.forEach((dish) => {
    container.innerHTML += `<div class="dish-item"><span>${
      dish.name
    }</span><span>${dish.price.toLocaleString()}₫</span></div>`;
    total += dish.price;
  });
  totalText.innerText = `Tổng tiền: ${total.toLocaleString()}₫`;
  if (qrCodeImg) {
    const base = "https://img.vietqr.io/image/ACB-34639877-compact.png";
    const qrParams = `?amount=${total}&addInfo=THANH+TOAN+BUA+AN`;
    qrCodeImg.src = base + qrParams;
  }
}

function resetOrder() {
  allDishes = [];
  document.getElementById("dish-items").innerHTML = "";
  document.getElementById("total-price").innerText = "Tổng tiền: 0₫";
  document.getElementById("captured-images").innerHTML = "";
  document.getElementById("qr-code-img").src =
    "https://img.vietqr.io/image/ACB-34639877-compact.png?amount=0&addInfo=THANH+TOAN+BUA+AN";
}
function renderDishList() {
  const container = document.getElementById("dish-items");
  const totalText = document.getElementById("total-price");
  const qrCodeImg = document.getElementById("qr-code-img");
  const qrSection = document.getElementById("qr-section");

  container.innerHTML = "";
  let total = 0;

  allDishes.forEach((dish, index) => {
    const row = document.createElement("div");
    row.className = "dish-item";
    row.innerHTML = `
            <span>${dish.name}</span>
            <span>
            ${dish.price.toLocaleString()}₫ 
            <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeDish(${index})">
                <i class="fas fa-times"></i>
            </button>
            </span>
        `;
    container.appendChild(row);
    total += dish.price;
  });

  totalText.innerText = `Tổng tiền: ${total.toLocaleString()}₫`;

  if (qrCodeImg) {
    const base = "https://img.vietqr.io/image/ACB-34639877-compact.png";
    const qrParams = `?amount=${total}&addInfo=THANH+TOAN+BUA+AN`;
    qrCodeImg.src = base + qrParams;
  }

  qrSection.style.display = allDishes.length > 0 ? "block" : "none";
}
function removeDish(index) {
  const dish = allDishes[index];
  Swal.fire({
    title: "Bạn có chắc muốn xoá món này?",
    text: `"${dish.name}" sẽ bị xoá khỏi danh sách.`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Xoá",
    cancelButtonText: "Huỷ",
    confirmButtonColor: "#d33",
    cancelButtonColor: "#6c757d",
  }).then((result) => {
    if (result.isConfirmed) {
      allDishes.splice(index, 1);
      renderDishList();
      Swal.fire({
        title: "Đã xoá!",
        text: `"${dish.name}" đã được xoá khỏi danh sách.`,
        icon: "success",
        timer: 1500,
        showConfirmButton: false,
      });
    }
  });
}
console.log("Đã load file script.js thành công!");
const langPath = "/static/lang.json";
const translations = {
  vi: {
    "title-text": "NHẬN DIỆN MÓN - THANH TOÁN TỨC THÌ",
    "btn-history": "Xem lịch sử",
    "btn-prices": "Xem thực đơn",
    "btn-admin": "Quản trị viên",
    btn_capture: "Chụp & Nhận Diện",
    "upload-info": "Hoặc tải ảnh từ máy:",
    //
    dish_list: "Danh sách món ăn:",
    detecting: "Đang nhận diện món ăn...",
    "total-price": "Tổng tiền: 0₫",
    qr_title: "Quét mã để thanh toán",
    "label-language": "Ngôn ngữ:",
    btn_invoice: "Xuất hóa đơn PDF",
    btn_reset: "Reset hóa đơn",
    content_bank: "Chuyển khoản đúng số tiền và nội dung để xác nhận đơn hàng.",
  },
  en: {
    "title-text": "FOOD RECOGNITION - INSTANT PAYMENT",
    "btn-history": "View History",
    "btn-prices": "View Menu",
    "btn-admin": "Admin Panel",
    btn_capture: "Capture & Detect",
    "upload-info": "Or upload an image:",
    "multi-info":
      "You can capture or upload multiple images to analyze dishes.",
    dish_list: "Dish List:",
    detecting: "Detecting food items...",
    "total-price": "Total: 0₫",
    qr_title: "Scan QR to Pay",
    "label-language": "Language:",
    btn_invoice: "Export Invoice PDF",
    btn_reset: "Reset Order",
    content_bank:
      "Transfer the exact amount and reference to confirm your order.",
  },
};

function changeLanguage(lang) {
  for (const key in translations[lang]) {
    const el = document.getElementById(key);
    if (el) el.innerText = translations[lang][key];
  }
}
