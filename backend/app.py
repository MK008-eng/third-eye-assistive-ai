from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Third Eye Assistive AI",
    description="AI-powered assistive technology",
    version="1.0.0"
)

LANGUAGES = ["English", "Tamil"]


class AssistantRequest(BaseModel):
    message: str
    language: str = "English"


@app.get("/")
def home():
    return {
        "application": "Third Eye Assistive AI",
        "status": "Running",
        "message": "Welcome to Third Eye"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/languages")
def languages():
    return {
        "supported_languages": LANGUAGES
    }


@app.post("/api/assistant")
def assistant(data: AssistantRequest):

    message = data.message.strip()
    language = data.language

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Please provide a message"
        )

    if language not in LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    text = message.lower()

    if language == "English":

        if "hello" in text or "hi" in text:
            response = "Hello! How can I assist you?"

        elif "help" in text:
            response = "I am here to help you understand your surroundings."

        elif "who are you" in text:
            response = "I am Third Eye, your assistive AI companion."

        elif "time" in text:
            response = datetime.now().strftime(
                "The current time is %I:%M %p"
            )

        elif "features" in text:
            response = (
                "I support voice assistance, "
                "object recognition and text recognition."
            )

        else:
            response = "I received your message. How can I help?"

    else:

        if "வணக்கம்" in message:
            response = "வணக்கம்! நான் உங்களுக்கு எப்படி உதவலாம்?"

        elif "உதவி" in message:
            response = "உங்களுக்கு உதவ நான் தயாராக இருக்கிறேன்."

        else:
            response = "உங்கள் கோரிக்கையை நான் பெற்றுள்ளேன்."

    return {
        "success": True,
        "message": message,
        "language": language,
        "response": response
    }


@app.get("/api/info")
def application_info():
    return {
        "name": "Third Eye Assistive AI",
        "version": "1.0.0",
        "supported_languages": LANGUAGES,
        "features": [
            "Voice Assistance",
            "Object Recognition",
            "Text Recognition"
        ]
    }
