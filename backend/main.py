from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import os

app = FastAPI(
title="Third Eye Assistive AI",
description="AI-powered assistive vision and communication system",
version="1.0.0"
)

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=True,
allow_methods=[""],
allow_headers=["*"]
)

@app.get("/")
def home():
return {
"message": "Third Eye Assistive AI Backend",
"status": "running"
}

@app.get("/health")
def health():
return {"status": "healthy"}

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):

if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
    return {"error": "Unsupported image format"}

image_data = await file.read()

if len(image_data) > 5 * 1024 * 1024:
    return {"error": "Image size exceeds 5 MB"}

try:
    image = Image.open(BytesIO(image_data))
    image.verify()

    return {
        "status": "success",
        "message": "Image received successfully",
        "filename": file.filename,
        "image_size": len(image_data),
        "ai_analysis": "AI image analysis integration is pending."
    }

except Exception:
    return {"error": "Invalid image file"}

@app.get("/features")
def features():
return {
"features": [
"Image Upload",
"AI Scene Understanding - Pending",
"Object Recognition - Pending",
"Voice Assistance",
"Navigation Assistance"
]
}