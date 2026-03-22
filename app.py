from flask import Flask, request, jsonify
import resend
from datetime import datetime
app = Flask(__name__)
# CONFIG
API_TOKEN = "esp8266secret123"
resend.api_key = "re_bqQTtWqA_PqZnXs7zUwEwYrSqLtPbFDEy"   # 🔥 replace
# ROOT (for keepAlive ping)
@app.route("/", methods=["GET"])
def home():
    return "Pillar Monitor Running", 200
# ALERT ENDPOINT (ESP CALLS THIS)
# ALERT ENDPOINT (ESP CALLS THIS)
@app.route("/alert", methods=["POST"])
def alert():
    try:
        # 🔐 TOKEN CHECK
        token = request.headers.get("X-Token", "")
        if token != API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        # 📦 GET DATA
        data = request.get_json()
        print("📥 DATA RECEIVED:", data)
        # 🧠 SAFE EXTRACTION
        alert_type = data.get("alert_type", "UNKNOWN")
        crack = float(data.get("crack_length", 0))
        stress = float(data.get("stress", 0))
        stability = bool(data.get("stability", True))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 📧 SEND EMAIL
        resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": ["pillarmonitor@gmail.com"],
                "subject": f"🚨 {alert_type}",
                "html": f"""
<pre>
====================================
  STRUCTURAL MONITORING ALERT
====================================

ALERT TYPE  : {alert_type}
TIMESTAMP   : {now}

------------------------------------
SENSOR READINGS AT TIME OF ALERT
------------------------------------
Crack Length : {crack:.4f} cm
Vibration    : {stress:.4f}
Stability    : {"STABLE" if stability else "UNSTABLE"}
------------------------------------

Please inspect the structure immediately.
The crack or instability may be developing further.

- ESP8266 Structure Monitor
====================================
</pre>
"""
            }
        )
        print("✅ EMAIL SENT")
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
# HEALTH CHECK
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
# RUN (Railway uses gunicorn, but this is fallback)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
