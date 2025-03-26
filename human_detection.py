import cv2
import numpy as np
import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Replace with your own chat_id
VIDEO_URL = os.getenv("VIDEO_URL")

# Ensure videos directory exists
VIDEO_DIR = "videos/detection"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)


def get_video_filename():
    """Generate a unique filename with timestamp."""
    return os.path.join(
        VIDEO_DIR, f"motion_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
    )


def send_video_to_telegram(video_path):
    """Send recorded video to Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(video_path, "rb") as video:
        files = {"video": video}
        data = {"chat_id": CHAT_ID, "caption": "Motion detected - video recorded."}
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            print(f"Video sent successfully: {video_path}")
        else:
            print(f"Failed to send video: {response.text}")


def cleanup_old_videos(days=14):
    """Delete videos older than `days` days."""
    now = time.time()
    for filename in os.listdir(VIDEO_DIR):
        file_path = os.path.join(VIDEO_DIR, filename)
        if os.path.isfile(file_path) and filename.startswith("motion_"):
            file_time = os.path.getmtime(file_path)
            if now - file_time > days * 86400:  # 14 days in seconds
                os.remove(file_path)
                print(f"Deleted old video: {filename}")


def run_human_detection():
    # Load object detection model
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prototxt = os.path.join(current_dir, "models", "MobileNetSSD_deploy.prototxt.txt")
    model = os.path.join(current_dir, "models", "MobileNetSSD_deploy.caffemodel")

    if not os.path.exists(prototxt) or not os.path.exists(model):
        print("Model files missing")
        exit()

    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    CLASSES = [
        "background",
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "pottedplant",
        "sheep",
        "sofa",
        "train",
        "tvmonitor",
    ]

    # Check for valid video URL
    if not VIDEO_URL:
        print("Error: VIDEO_URL not found in environment variables")
        exit()

    cap = cv2.VideoCapture(VIDEO_URL)
    if not cap.isOpened():
        print("Error: Cannot connect to camera")
        exit()

    # Recording setup
    min_record_seconds = 30
    video_writer = None
    recording = False
    record_end_time = None  # Timestamp when recording should end

    print("Motion detection started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5
        )
        net.setInput(blob)
        detections = net.forward()

        person_detected = False

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])
            if confidence > 0.3 and idx < len(CLASSES) and CLASSES[idx] == "person":
                person_detected = True
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"Person: {confidence * 100:.1f}%"
                cv2.putText(
                    frame,
                    label,
                    (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

        current_time = time.time()

        if person_detected:
            if not recording:
                # Start recording
                recording = True
                record_end_time = current_time + min_record_seconds
                video_filename = get_video_filename()
                video_writer = cv2.VideoWriter(
                    video_filename, cv2.VideoWriter_fourcc(*"XVID"), 20.0, (w, h)
                )
                print(f"Recording started: {video_filename}")
            else:
                # Extend recording time
                record_end_time = current_time + min_record_seconds
                print("Person detected again — extended recording.")

        if recording:
            video_writer.write(frame)
            if current_time >= record_end_time:
                video_writer.release()
                print(f"Recording stopped. Sending video: {video_filename}")
                send_video_to_telegram(video_filename)
                recording = False

        cv2.imshow("Human Detection Video", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()

    # Cleanup old videos
    cleanup_old_videos()


if __name__ == "__main__":
    run_human_detection()
