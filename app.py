from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOCO_SECRET_KEY = "sk_live_6118503aM1J7kzZ8bec485fb0427"

unlock_status = {"full_unlocked": False}

@app.route("/create-checkout", methods=["POST"])
def create_checkout():
    data = {
        "amount": 10000,
        "currency": "ZAR",
        "description": "Smart7 Full Mode Unlock"
    }
    headers = {"X-Auth-Secret-Key": YOCO_SECRET_KEY}
    response = requests.post("https://online.yoco.com/v1/charges/", headers=headers, json=data)
    return jsonify(response.json())

@app.route("/yoco-webhook", methods=["POST"])
def yoco_webhook():
    payload = request.json
    if payload.get("status") == "successful":
        unlock_status["full_unlocked"] = True
    return jsonify({"received": True})

@app.route("/unlock-status", methods=["GET"])
def unlock_status_endpoint():
    return jsonify(unlock_status)
