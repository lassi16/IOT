import multiprocessing
import continuous_recording
import human_detection
import os
from dotenv import load_dotenv

load_dotenv()
video_url = os.getenv("VIDEO_URL")

if __name__ == "__main__":
    # Create processes for continuous recording and human detection
    process1 = multiprocessing.Process(
        target=continuous_recording.continuous_recording, args=(video_url,)
    )
    process2 = multiprocessing.Process(target=human_detection.run_human_detection)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
