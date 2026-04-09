from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

# 🔥 Use /tmp (Render requirement)
UPLOAD_FOLDER = "/tmp/frames"
VIDEO_FOLDER = "/tmp/videos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

frame_count = 0
FRAME_THRESHOLD = 20  # 🔥 change if needed

# ===========================
# HOME
# ===========================
@app.route('/')
def home():
    return "ESP32 CCTV SERVER RUNNING ✅"

# ===========================
# UPLOAD
# ===========================
@app.route('/upload', methods=['POST'])
def upload():
    global frame_count

    filename = f"{UPLOAD_FOLDER}/frame_{int(time.time()*1000)}.jpg"

    with open(filename, "wb") as f:
        f.write(request.data)

    frame_count += 1
    print("Frame:", frame_count)

    # 🔥 AUTO VIDEO TRIGGER
    if frame_count >= FRAME_THRESHOLD:
        create_video()

    return "OK", 200

# ===========================
# VIDEO CREATION
# ===========================
def create_video():
    global frame_count

    print("🎬 Creating video...")

    output = f"{VIDEO_FOLDER}/output.mp4"

    os.system(f"ffmpeg -y -framerate 5 -pattern_type glob -i '{UPLOAD_FOLDER}/*.jpg' {output}")

    print("✅ Video created:", output)

    # 🔥 DELETE OLD FRAMES
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    frame_count = 0

# ===========================
# STATUS
# ===========================
@app.route('/status')
def status():
    return jsonify({
        "frames": frame_count,
        "threshold": FRAME_THRESHOLD
    })
