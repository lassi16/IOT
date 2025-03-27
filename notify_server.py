import requests
import cv2
import datetime
import os
import time
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
CHAT_ID = os.getenv("CHAT_ID")


def notify_server(image_path):
    global CHAT_ID
    global SERVER_URL

    with open(image_path, "rb") as img_file:
        files = {"file": (os.path.basename(image_path), img_file, "image/jpeg")}
        data = {"user_id": CHAT_ID, "timestamp": str(datetime.datetime.now())}

        try:
            response = requests.post(
                f"{SERVER_URL}/detect-human-image",
                files=files,
                data=data,
            )
            print(f"Server Response: {response.text}")
        except Exception as e:
            print(f"Failed to notify server : {e}")


def notify_server_video(video_path):
    global CHAT_ID
    global SERVER_URL

    with open(video_path, "rb") as video_file:
        files = {"file": (os.path.basename(video_path), video_file, "video/x-msvideo")}
        data = {"user_id": CHAT_ID, "timestamp": str(datetime.datetime.now())}
        try:
            response = requests.post(
                f"{SERVER_URL}/detect-human-video",
                files=files,
                data=data,
            )
            print(f"Server Response: {response.text}")
        except Exception as e:
            print(f"Failed to notify server : {e}")
