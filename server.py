import os
import secrets
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder="web/static", template_folder="web")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna").strip()
ALBUS_TOKEN = os.getenv("ALBUS_TOKEN", "").strip()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYSTEM_PROMPT = """
You are ALBUS 2.0 — Augmented Learning Based Universal System, a personal AI assistant
designed primarily for an iPhone.

Personality:
- Calm, capable, concise, and helpful.
- You may have a subtle JARVIS-like technical tone, but do not imitate copyrighted dialogue.
- Address the user naturally.
- Do not claim to have performed an action unless you actually performed it.
- When current information is needed, use web search.
- When the user asks for a recommendation or explanation, give a practical answer.
- If you need clarification, ask only what is necessary.

Capabilities:
- General conversation, tutoring, writing, planning, coding, calculations.
- Current web research through the built-in web search tool.
- The phone UI handles local timers, reminders, speech output, and local conversation storage.
"""

def authorized():
    if not ALBUS_TOKEN:
        return False
    header = request.headers.get("Authorization", "")
    token = header.removeprefix("Bearer ").strip()
    return secrets.compare_digest(token, ALBUS_TOKEN)

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "microphone=(self), geolocation=(self)"
    return response

@app.get("/")
def home():
    return send_from_directory("web", "index.html")

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "service": "ALBUS 3.0 Core",
        "model": MODEL,
        "time": datetime.now(timezone.utc).isoformat()
    })

@app.post("/api/chat")
def chat():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401
    if not client:
        return jsonify({"error": "OPENAI_API_KEY is not configured on the ALBUS server."}), 500

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Message is required."}), 400

    safe_history = []
    if isinstance(history, list):
        for item in history[-16:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = str(item.get("content", ""))[:12000]
            if role in ("user", "assistant") and content:
                safe_history.append({"role": role, "content": content})

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=[{"type": "web_search"}],
            input=safe_history + [{"role": "user", "content": message}],
        )
        reply = response.output_text or "I wasn't able to produce a response."
        return jsonify({"reply": reply})
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 502

@app.get("/api/config")
def config():
    return jsonify({
        "name": "ALBUS 2.0",
        "version": "2.0",
        "voice": True,
        "web_search": bool(client),
    })

@app.route("/<path:path>")
def static_files(path):
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404
    return send_from_directory("web", path)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
