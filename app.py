import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Health Check Route ---
@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Backend is running!"})

# --- Version Route ---
@app.route("/version")
def version():
    return jsonify({"app": "Smart7", "version": "1.0", "grade_levels": "7–12"})

# --- Unlock Status Route ---
@app.route("/unlock-status", methods=["GET"])
def unlock_status():
    # Example: check if user is unlocked (replace with your DB or logic)
    user_id = request.args.get("user_id", "demo_user")
    # For demo purposes, always return unlocked
    return jsonify({"user_id": user_id, "status": "unlocked"})

# --- Payment Confirmation Route ---
@app.route("/confirm-payment", methods=["POST"])
def confirm_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    # Example: store payment confirmation (replace with DB logic)
    return jsonify({
        "user_id": user_id,
        "amount": amount,
        "message": "Payment confirmed. Full Mode unlocked!"
    })

# --- Main Entry Point ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
