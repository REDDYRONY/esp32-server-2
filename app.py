from celery import Celery
import subprocess
import os
import glob
import time
import requests

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# 🔑 TELEGRAM CONFIG
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(video_path):
    print("📩 Sending video to Telegram...")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    with open(video_path, "rb") as video:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"video": video})

    print("✅ Sent to Telegram")


def upload_to_cloud(video_path):
    print("☁️ Uploading to cloud (basic)...")

    # Example: save in cloud folder (simulate)
    os.makedirs("cloud", exist_ok=True)

    filename = os.path.basename(video_path)
    os.rename(video_path, f"cloud/{filename}")

    print("✅ Uploaded to cloud folder")


@celery.task
def create_video():
    print("🎬 Celery worker started...")

    timestamp = int(time.time())
    output_file = f"videos/video_{timestamp}.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-framerate", "5",
        "-i", "frames/frame_%d.jpg",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    subprocess.run(command)

    print(f"✅ Video created: {output_file}")

    # 📩 TELEGRAM SEND
    send_telegram(output_file)

    # ☁️ CLOUD UPLOAD
    upload_to_cloud(output_file)

    # 🧹 DELETE FRAMES
    files = glob.glob("frames/*.jpg")
    for f in files:
        os.remove(f)

    print("🧹 Frames deleted")
