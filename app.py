from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import ssl


load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
print(f"🔧 Attempting to connect to MongoDB URI: {MONGO_URI}")

try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False, ssl_cert_reqs=ssl.CERT_REQUIRED)
    db = client.get_database()
    client.admin.command("ping")
    print("✅ MongoDB connected successfully.")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

@app.route("/ping", methods=["GET"])
def ping():
    print(f"📡 /ping hit from: {request.remote_addr}")
    try:
        db.command("ping")
        print("✅ /ping success — MongoDB still connected.")
        return jsonify({"status": "Connected"}), 200
    except Exception as e:
        print("❌ /ping failed —", str(e))
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
