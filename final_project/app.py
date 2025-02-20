from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["RESULT_FOLDER"] = "static/results"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def resize_image(image_path, max_size=600, interpolation=cv2.INTER_LINEAR):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=interpolation)

    cv2.imwrite(image_path, img)
    return img


def apply_bilinear_interpolation(img):
    height, width = img.shape[:2]
    result_img = np.zeros_like(img)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            f00 = img[i - 1, j - 1]
            f01 = img[i - 1, j]
            f10 = img[i, j - 1]
            f11 = img[i, j]

            x_weight = 0.5
            y_weight = 0.5

            interpolated_pixel = (
                f00 * (1 - x_weight) * (1 - y_weight)
                + f01 * (1 - x_weight) * y_weight
                + f10 * x_weight * (1 - y_weight)
                + f11 * x_weight * y_weight
            )
            result_img[i, j] = interpolated_pixel.astype(np.uint8)

    return result_img


def apply_filter(image_path, filter_name):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if filter_name == "grayscale":
        filtered = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
    elif filter_name == "sepia":
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        filtered = cv2.transform(img, kernel)
    elif filter_name == "invert":
        filtered = cv2.bitwise_not(img)
    elif filter_name == "warm":
        filtered = cv2.applyColorMap(img, cv2.COLORMAP_COOL)
    elif filter_name == "cool":
        filtered = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
    elif filter_name == "twilight":
        filtered = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT)
    elif filter_name == "enhance":
        filtered = cv2.detailEnhance(img, sigma_s=50, sigma_r=0.15)
    elif filter_name == "pencil_sketch":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        filtered = cv2.divide(gray, 255 - blurred, scale=256)
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
    elif filter_name == "bilinear_blur":
        filtered = apply_bilinear_interpolation(img)
    else:
        filtered = img

    return filtered


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file selected")

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No file selected")

        if file and allowed_file(file.filename):
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(upload_path)

            resize_image(upload_path)

            selected_filter = request.form.get("filter", "original")
            filtered_image = apply_filter(upload_path, selected_filter)
            result_path = os.path.join(app.config["RESULT_FOLDER"], filename)
            cv2.imwrite(result_path, cv2.cvtColor(filtered_image, cv2.COLOR_RGB2BGR))

            return render_template(
                "index.html",
                original=filename,
                result=filename,
                filter_used=selected_filter,
            )

    return render_template("index.html")


@app.route("/uploads/<filename>")
def send_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/results/<filename>")
def send_result_file(filename):
    return send_from_directory(app.config["RESULT_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
