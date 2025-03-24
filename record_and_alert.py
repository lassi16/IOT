import cv2
import numpy as np
import os
import time
import asyncio
from telegram import Bot

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to the model files using absolute paths
prototxt = os.path.join(current_dir, "models", "MobileNetSSD_deploy.prototxt.txt")
model = os.path.join(current_dir, "models", "MobileNetSSD_deploy.caffemodel")

# Verify that the model files exist
if not os.path.exists(prototxt):
    print("Error: Prototxt file not found:", prototxt)
    exit()
if not os.path.exists(model):
    print("Error: Caffemodel file not found:", model)
    exit()

# Initialize the list of class labels MobileNet SSD was trained to detect
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse",
    "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

# Load the neural network model
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# Telegram Bot configuration - replace with your actual bot token and chat ID
TELEGRAM_TOKEN = "7568303321:AAH9oIPNonVBmWK7C-Z5cUZan3eVP6cQ9UY"
CHAT_ID = "7736576183"
bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_alert(filename):
    """Asynchronously send video alert through Telegram"""
    with open(filename, 'rb') as video_file:
        await bot.send_video(
            chat_id=CHAT_ID,
            video=video_file,
            caption="Alert: Human detected!"
        )

# Open the video stream from your mobile camera (update the URL if necessary)
video_url = "http://10.16.1.1:8080/video"
cap = cv2.VideoCapture(video_url)
if not cap.isOpened():
    print("Error: Cannot connect to camera")
    exit()

# Variables for recording
recording = False
recorded_frames = []
clip_duration = 3  # seconds for the video clip
start_time = None
human_detected_time = None  # Track when a person is first detected
threshold_duration = 2  # Seconds before recording starts

def save_clip(frames, output_filename, fps=20, frame_size=(640, 480)):
    """Saves a list of frames as an MP4 video."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)
    for frame in frames:
        out.write(frame)
    out.release()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    (h, w) = frame.shape[:2]
    # Prepare the frame for detection
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    human_detected = False

    # Loop over the detections and check for "person"
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])
        # Use a threshold (e.g., 0.7) for detection confidence
        if confidence > 0.5:
            if idx < len(CLASSES) and CLASSES[idx] == "person":
                human_detected = True
                # Draw the bounding box and label
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"Person: {confidence * 100:.1f}%"
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Implement the 2-second threshold for detection before recording
    if human_detected:
        if human_detected_time is None:
            human_detected_time = time.time()
        elif time.time() - human_detected_time >= threshold_duration and not recording:
            print("Human detected continuously for 2 seconds! Starting to record...")
            recording = True
            recorded_frames = []
            start_time = time.time()
    else:
        human_detected_time = None  # Reset if no human is detected

    # If currently recording, save the current frame
    if recording:
        recorded_frames.append(frame.copy())
        # Stop recording after clip_duration seconds
        if time.time() - start_time > clip_duration:
            recording = False
            filename = f"alert_{int(time.time())}.mp4"
            save_clip(recorded_frames, filename, fps=20, frame_size=(w, h))
            print(f"Video clip saved as {filename}")

            # Send the video clip via Telegram
            try:
                asyncio.run(send_telegram_alert(filename))
                print("Telegram alert sent!")
            except Exception as e:
                print("Error sending Telegram alert:", e)

    # Show the live detection frame
    cv2.imshow("Live Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()