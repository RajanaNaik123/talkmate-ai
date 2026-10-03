
import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/practice")
def practice():
    return render_template("practice.html")


@app.route("/chat")
def chat():
    scenario = request.args.get(
        "scenario", "Everyday Conversation"
    )
    return render_template("chat.html", scenario=scenario)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if client is None:
        return jsonify({"error": "Gemini API key is not configured."}), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    scenario = data.get("scenario", "Everyday Conversation")

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    prompt = f"""
    You are TalkMate AI, a friendly communication coach.
    Practice scenario: {scenario}.
    Reply naturally, as a conversation partner.
    Be supportive and give brief, practical communication tips.
    Support the language used by the user when possible.
    User message: {message}
    """

    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return jsonify({"reply": response.text})
    
    except Exception as e:
        app.logger.exception("Gemini API request failed")

        if "503" in str(e) or "UNAVAILABLE" in str(e):
            return jsonify({
                "error": "I'm receiving lots of requests right now. Please try again in a moment."
            }), 503

        return jsonify({
            "error": "I couldn't connect to the AI coach. Please try again shortly."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)