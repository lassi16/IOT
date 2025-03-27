import cv2

# Replace with your mobile camera URL (e.g., for IP Webcam)
video_url = "http://192.168.17.126:8080/video"

# Open the video capture stream
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Cannot connect to camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Live Feed", frame)
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
