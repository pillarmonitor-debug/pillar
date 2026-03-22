from flask import Flask, request, jsonify
from datetime import datetime
import os
import resend

app = Flask(__name__)

# CONFIG
API_TOKEN = "esp8266secret123"
RECIPIENT_EMAIL = "pillarmonitor@gmail.com"

# RESEND KEY
resend.api_key = "re_bqQTtWqA_PqZnXs7zUwEwYrSqLtPbFDEy"


# EMAIL FUNCTION (SIMPLE + WORKING)
def send_email():
    try:
        resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": ["pillarmonitor@gmail.com"],
                "subject": "TEST MAIL",
                "html": "<h2>🚀 EMAIL WORKING</h2>"
            }
        )
        return True
    except:
        return False


# TEST ROUTE
@app.route("/test")
def test():
    if send_email():
        return "✅ Email Sent"
    else:
        return "❌ Email Failed"


# ALERT ROUTE (ESP USES THIS)
@app.route("/alert", methods=["POST"])
def alert():
    token = request.headers.get("X-Token", "")
    if token != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    resend.Emails.send(
        {
            "from": "onboarding@resend.dev",
            "to": ["pillarmonitor@gmail.com"],
            "subject": "🚨 ALERT",
            "html": f"""
            <h2>🚨 ALERT RECEIVED</h2>
            <p>Crack: {data.get('crack_length')}</p>
            <p>Vibration: {data.get('vibration')}</p>
            <p>Stability: {data.get('stability')}</p>
            """
        }
    )

    return jsonify({"status": "sent"}), 200


# ROOT (fix 404)
@app.route("/")
def home():
    return "Pillar Monitor Running"


# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
