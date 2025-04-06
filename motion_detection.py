import cv2
import numpy as np
import os
import requests
import time
import logging
from dotenv import load_dotenv
from datetime import datetime
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("motion_detection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configuration
class Config:
    # Telegram bot configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    VIDEO_URL = os.getenv("VIDEO_URL")
    
    # File storage
    VIDEO_DIR = "videos/motion"
    
    # Motion detection parameters
    MIN_AREA = 500  # Minimum contour area to consider as motion
    MOTION_THRESHOLD = 15  # Percentage of frame with motion to trigger recording
    
    # Recording parameters
    MIN_RECORD_SECONDS = 30
    FPS = 20.0
    RETENTION_DAYS = 14
    
    # Background subtraction parameters
    HISTORY = 200
    VAR_THRESHOLD = 40

# Ensure videos directory exists
if not os.path.exists(Config.VIDEO_DIR):
    os.makedirs(Config.VIDEO_DIR)


def get_video_filename():
    """Generate a unique filename with timestamp."""
    return os.path.join(
        Config.VIDEO_DIR, f"motion_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
    )


def send_video_to_telegram(video_path):
    """Send recorded video to Telegram bot in a separate thread."""
    def send_async():
        try:
            url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendVideo"
            with open(video_path, "rb") as video:
                files = {"video": video}
                data = {"chat_id": Config.CHAT_ID, "caption": "Motion detected - video recorded."}
                response = requests.post(url, data=data, files=files, timeout=60)
                if response.status_code == 200:
                    logger.info(f"Video sent successfully: {video_path}")
                else:
                    logger.error(f"Failed to send video: {response.text}")
        except Exception as e:
            logger.error(f"Error sending video: {str(e)}")
    
    # Start sending in background thread so we don't block motion detection
    threading.Thread(target=send_async).start()


def cleanup_old_videos(days=Config.RETENTION_DAYS):
    """Delete videos older than specified days."""
    try:
        now = time.time()
        count = 0
        for filename in os.listdir(Config.VIDEO_DIR):
            file_path = os.path.join(Config.VIDEO_DIR, filename)
            if os.path.isfile(file_path) and filename.startswith("motion_"):
                file_time = os.path.getmtime(file_path)
                if now - file_time > days * 86400:  # days in seconds
                    os.remove(file_path)
                    count += 1
        logger.info(f"Deleted {count} old videos")
    except Exception as e:
        logger.error(f"Error cleaning up videos: {str(e)}")


class MotionDetector:
    def __init__(self):
        self.cap = None
        self.video_writer = None
        self.recording = False
        self.record_end_time = None
        self.video_filename = None
        self.height = 0
        self.width = 0
        self.backSub = None
        
    def initialize(self):
        # Check for valid video URL
        if not Config.VIDEO_URL:
            logger.error("VIDEO_URL not found in environment variables")
            return False

        self.cap = cv2.VideoCapture(Config.VIDEO_URL)
        if not self.cap.isOpened():
            logger.error("Cannot connect to camera")
            return False

        # Get initial frame dimensions
        ret, frame = self.cap.read()
        if not ret:
            logger.error("Failed to grab initial frame")
            return False
        
        self.height, self.width = frame.shape[:2]
        
        # Create background subtractor
        self.backSub = cv2.createBackgroundSubtractorMOG2(
            history=Config.HISTORY, 
            varThreshold=Config.VAR_THRESHOLD, 
            detectShadows=True
        )
        
        return True
        
    def process_frame(self, frame):
        """Process a single frame and return motion information."""
        # Create a copy for display
        display_frame = frame.copy()
        
        # Apply background subtraction
        fg_mask = self.backSub.apply(frame)
        
        # Remove shadows (gray pixels) and keep only white pixels (motion)
        _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours of moving objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        total_motion_area = 0
        
        # Process detected contours
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > Config.MIN_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                total_motion_area += area
        
        # Calculate percentage of frame with motion
        frame_area = self.height * self.width
        motion_percentage = (total_motion_area / frame_area) * 100
        
        # Add motion percentage text to the frame
        cv2.putText(
            display_frame,
            f"Motion: {motion_percentage:.2f}%",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )
        
        return display_frame, fg_mask, motion_percentage
    
    def start_recording(self):
        """Start recording a video."""
        self.recording = True
        self.record_end_time = time.time() + Config.MIN_RECORD_SECONDS
        self.video_filename = get_video_filename()
        self.video_writer = cv2.VideoWriter(
            self.video_filename, 
            cv2.VideoWriter_fourcc(*"XVID"), 
            Config.FPS, 
            (self.width, self.height)
        )
        logger.info(f"Recording started: {self.video_filename}")
        
    def extend_recording(self):
        """Extend the current recording session."""
        self.record_end_time = time.time() + Config.MIN_RECORD_SECONDS
        logger.debug("Motion detected again — extended recording.")
        
    def stop_recording(self):
        """Stop recording and send the video."""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            logger.info(f"Recording stopped: {self.video_filename}")
            send_video_to_telegram(self.video_filename)
            self.recording = False
    
    def run(self):
        """Run the motion detection loop."""
        if not self.initialize():
            return
            
        logger.info("Motion detection started...")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Failed to grab frame")
                    # Try to reconnect
                    time.sleep(5)
                    self.cap = cv2.VideoCapture(Config.VIDEO_URL)
                    continue
                    
                # Process the frame
                display_frame, fg_mask, motion_percentage = self.process_frame(frame)
                
                current_time = time.time()
                
                # Check if motion is significant
                motion_detected = motion_percentage > Config.MOTION_THRESHOLD
                            
                if motion_detected:
                    if not self.recording:
                        self.start_recording()
                    else:
                        self.extend_recording()

                if self.recording:
                    # Add recording indicator
                    cv2.putText(
                        display_frame,
                        "RECORDING",
                        (self.width - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )
                    self.video_writer.write(frame)  # Save original frame without annotations
                    
                    if current_time >= self.record_end_time:
                        self.stop_recording()

                # Show the resulting frame with motion indicators
                cv2.imshow("Motion Detection", display_frame)
                
                # Show the mask (helpful for debugging)
                cv2.imshow("Motion Mask", fg_mask)

                # Press 'q' to exit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                    
        except KeyboardInterrupt:
            logger.info("Motion detection stopped by user")
        except Exception as e:
            logger.error(f"Error in motion detection: {str(e)}")
        finally:
            # Clean up
            if self.cap:
                self.cap.release()
            if self.recording and self.video_writer:
                self.video_writer.release()
            cv2.destroyAllWindows()
            
            # Cleanup old videos
            cleanup_old_videos()
            logger.info("Motion detection stopped")


def main():
    detector = MotionDetector()
    detector.run()


if __name__ == "__main__":
    main()