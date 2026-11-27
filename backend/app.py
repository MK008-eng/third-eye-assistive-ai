from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Application information
APP_NAME = "Third Eye Assistive AI"
VERSION = "1.0.0"

# Supported languages
LANGUAGES = ["English", "Tamil"]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": APP_NAME,
        "version": VERSION,
        "status": "Running",
        "message": "Welcome to Third Eye Assistive AI"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/languages", methods=["GET"])
def languages():
    return jsonify({
        "supported_languages": LANGUAGES
    })


@app.route("/api/assistant", methods=["POST"])
def assistant():

    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()
    language = data.get("language", "English")

    if not user_message:
        return jsonify({
            "error": "Please provide a message"
        }), 400

    if language not in LANGUAGES:
        return jsonify({
            "error": "Unsupported language"
        }), 400

    message = user_message.lower()

    # English responses
    if language == "English":

        if "hello" in message or "hi" in message:
            response = "Hello! How can I assist you?"

        elif "help" in message:
            response = "I am here to help you understand your surroundings."

        elif "who are you" in message:
            response = "I am Third Eye, your assistive AI companion."

        elif "time" in message:
            response = datetime.now().strftime(
                "The current time is %I:%M %p"
            )

        elif "features" in message:
            response = (
                "I support voice assistance, "
                "object recognition and text recognition."
            )

        else:
            response = (
                "I heard your request. "
                "Please try asking about my features or assistance."
            )

    # Tamil responses
    else:

        if "வணக்கம்" in user_message:
            response = "வணக்கம்! நான் உங்களுக்கு எப்படி உதவலாம்?"

        elif "உதவி" in user_message:
            response = "உங்களுக்கு உதவ நான் தயாராக இருக்கிறேன்."

        else:
            response = "உங்கள் கோரிக்கையை நான் பெற்றுள்ளேன்."

    return jsonify({
        "application": APP_NAME,
        "user_message": user_message,
        "language": language,
        "response": response,
        "success": True
    })


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Requested page not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
      )
