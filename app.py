import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = "You are a friendly, helpful AI assistant. Keep answers clear and concise."

# In-memory chat sessions, keyed by a simple session id from the client.
# For production, swap this for a real store (Redis, DB, etc.)
sessions = {}


def get_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "Server is missing GEMINI_API_KEY."}), 500

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        if session_id not in sessions:
            sessions[session_id] = get_model().start_chat(history=[])

        chat_session = sessions[session_id]
        response = chat_session.send_message(message)
        return jsonify({"reply": response.text})

    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Gemini API error: {exc}"}), 500


@app.route("/api/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default")
    sessions.pop(session_id, None)
    return jsonify({"status": "reset"})


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
