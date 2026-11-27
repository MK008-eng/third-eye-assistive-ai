from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import os

app = FastAPI(
    title="Third Eye Assistive AI",
    description="AI-powered visual assistance system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024

@app.get("/")
def home():
    return {
        "message": "Third Eye Assistive AI",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format"
        )

    image_data = await file.read(MAX_IMAGE_SIZE + 1)

    if len(image_data) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds 5 MB limit"
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured"
        )

    try:
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                "Describe this image clearly for a visually impaired "
                "person. Identify visible objects, surroundings, "
                "and relevant safety observations. "
                "Do not guess details that are unclear. "
                "Keep the description concise.",
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                )
            ]
        )

        description = response.text

        if not description:
            raise HTTPException(
                status_code=502,
                detail="AI returned an empty response"
            )

        return {
            "status": "success",
            "description": description
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Image analysis failed. Please try again."
        )

@app.get("/features")
def features():
    return {
        "features": [
            "AI Image Understanding",
            "Scene Description",
            "Object Identification",
            "Voice Assistance",
            "Navigation Assistance"
        ]
    }