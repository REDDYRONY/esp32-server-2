from flask import Flask, request, jsonify

app = Flask(__name__)

frame_count = 0

@app.route('/')
def home():
    return "ESP32 Server Running ✅"

# 🔥 THIS IS IMPORTANT (UPLOAD ROUTE)
@app.route('/upload', methods=['POST'])
def upload():
    global frame_count
    frame_count += 1
    print("Frame received:", frame_count)
    return "OK", 200

@app.route('/status')
def status():
    return jsonify({
        "frames": frame_count
    })
