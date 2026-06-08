from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from model import ImageClassifier
import io
from PIL import Image
import numpy as np

app = FastAPI(title="Computer Vision", version="1.0.0")

classifier = ImageClassifier()

@app.get("/")
async def root():
    return {"message": "Computer Vision Model API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read() # read the image
        image = Image.open(io.BytesIO(contents))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = image.resize((224,224))