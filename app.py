from flask import Flask, request, jsonify
import resend
from datetime import datetime

app = Flask(__name__)

API_TOKEN = "esp8266secret123"
resend.api_key = "YOUR_NEW_API_KEY"   # 🔥 change this

@app.route("/alert", methods=["POST"])
def alert():
    token = request.headers.get("X-Token", "")
    if token != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    alert_type = data.get("alert_type")
    crack = data.get("crack_length")
    stress = data.get("stress")
    stability = data.get("stability")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": ["pillarmonitor@gmail.com"],
        "subject": f"🚨 {alert_type}",
        "html": f"""
        <h2>🚨 STRUCTURE ALERT</h2>
        <p><b>Time:</b> {now}</p>
        <hr>
        <p><b>Crack:</b> {crack}</p>
        <p><b>Stress:</b> {stress}</p>
        <p><b>Status:</b> {"STABLE" if stability else "UNSTABLE"}</p>
        """
    })

    return jsonify({"status": "sent"}), 200


@app.route("/")
def home():
    return "SERVER RUNNING"
