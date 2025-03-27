import requests
from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
UPLOAD_FOLDER = "server/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Server is running"


@app.route("/detect-human-video", methods=["POST"])
def detect_human():
    if "file" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    file = request.files["file"]
    user_id = request.form.get("user_id")
    timestamp = request.form.get("timestamp")

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    CHAT_ID = user_id

    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_path)

    with open(temp_path, "rb") as video_file:
        message = f"Here is the video."
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

        response = requests.post(
            telegram_url,
            data={"chat_id": CHAT_ID, "caption": message},
            files={"video": video_file},
        )

    os.remove(temp_path)

    if response.status_code == 200:
        return (
            jsonify({"status": "Video Sent", "telegram_response": response.json()}),
            200,
        )
    else:
        return (
            jsonify(
                {"status": "Failed to send video", "telegram_response": response.text}
            ),
            500,
        )


@app.route("/detect-human-image", methods=["POST"])
def detect_human_image():
    if "file" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    file = request.files["file"]
    user_id = request.form.get("user_id")
    timestamp = request.form.get("timestamp")

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    CHAT_ID = user_id

    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_path)

    with open(temp_path, "rb") as image_file:
        message = f"Alert! Human detected at {timestamp}."
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        response = requests.post(
            telegram_url,
            data={"chat_id": CHAT_ID, "caption": message},
            files={"photo": image_file},
        )

    os.remove(temp_path)
    if response.status_code == 200:
        return (
            jsonify({"status": "Image Sent", "telegram_response": response.json()}),
            200,
        )
    else:
        return (
            jsonify(
                {"status": "Failed to send image", "telegram_response": response.text}
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
