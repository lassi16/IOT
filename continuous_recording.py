import signal
import threading
import cv2
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Ensure videos directory exists
VIDEO_DIR = "videos/continuous"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# Video recording settings
FPS = 20.0
SEGMENT_DURATION = 3600  # 1 hour (in seconds)
RETENTION_DAYS = 14  # Delete videos older than 14 days
RECONNECT_DELAY = 5  # Seconds to wait before reconnecting
MAX_RETRIES = 3  # Maximum number of retries for connection
video_url = os.getenv("VIDEO_URL")
print(video_url)


def get_video_filename():
    """Generate a filename based on the current timestamp."""
    return os.path.join(
        VIDEO_DIR, f"continuous_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
    )


def cleanup_old_videos():
    """Delete videos older than `RETENTION_DAYS`."""
    now = time.time()
    for filename in os.listdir(VIDEO_DIR):
        file_path = os.path.join(VIDEO_DIR, filename)
        if os.path.isfile(file_path) and filename.startswith("continuous_"):
            file_time = os.path.getmtime(file_path)
            if now - file_time > RETENTION_DAYS * 86400:  # Convert days to seconds
                os.remove(file_path)
                print(f"Deleted old video: {filename}")


def graceful_exit(sig, frame):
    """Handle script exit to release resources properly."""
    print("\nExiting... Cleaning up resources.")
    cv2.destroyAllWindows()
    exit(0)


# Register signal handler for graceful exit
signal.signal(signal.SIGINT, graceful_exit)


def continuous_recording(video_url):
    """Continuously record video in defined segments."""
    while True:
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            print(
                f"[{datetime.now()}] Error: Cannot connect to camera. Retrying in {RECONNECT_DELAY} seconds..."
            )
            time.sleep(RECONNECT_DELAY)
            continue  # Retry connection

        # Detect frame size dynamically
        FRAME_SIZE = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        print(f"[{datetime.now()}] Connected to camera. Frame size: {FRAME_SIZE}")

        video_writer = cv2.VideoWriter(
            get_video_filename(), cv2.VideoWriter_fourcc(*"XVID"), FPS, FRAME_SIZE
        )
        start_time = time.time()

        while time.time() - start_time < SEGMENT_DURATION:
            ret, frame = cap.read()

            if not ret:
                print(
                    f"[{datetime.now()}] Error: Lost connection. Attempting to reconnect..."
                )
                retry_count = 0
                while retry_count < MAX_RETRIES:
                    time.sleep(RECONNECT_DELAY)
                    ret, frame = cap.read()
                    if ret:
                        print(f"[{datetime.now()}] Reconnected successfully.")
                        break
                    retry_count += 1
                    print(
                        f"[{datetime.now()}] Reconnection attempt {retry_count}/{MAX_RETRIES}"
                    )

                if retry_count == MAX_RETRIES:
                    print(
                        f"[{datetime.now()}] Failed to reconnect. Restarting recording..."
                    )
                    break  # Exit loop to retry connection

            video_writer.write(frame)
            cv2.imshow("Continuous Recording", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                video_writer.release()
                cv2.destroyAllWindows()
                return  # Exit function

        # Release current segment and start a new one
        video_writer.release()
        cap.release()  # Ensure resource cleanup before reconnecting

        # Run cleanup in a separate thread
        threading.Thread(target=cleanup_old_videos, daemon=True).start()


if __name__ == "__main__":
    continuous_recording(video_url)
