import cv2
import numpy as np
import os

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

# Open the video stream from your mobile camera (update the URL if needed)
video_url = "http://10.16.1.1:8080/video"
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Cannot connect to camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Get frame dimensions
    (h, w) = frame.shape[:2]
    
    # Prepare the frame for detection by creating a blob
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    
    # Forward pass to obtain detections
    detections = net.forward()
    
    # Loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])
        
        # Use a lower confidence threshold for testing (e.g., 0.3)
        if confidence > 0.3:
            if idx < len(CLASSES) and CLASSES[idx] == "person":
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"Person: {confidence * 100:.1f}%"
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow("Human Detection Video", frame)
    
    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
