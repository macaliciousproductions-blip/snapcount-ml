#### `ml-service/app/main.py`

```python

"""

SnapCount AI - ML Inference Service

FastAPI application for bottle detection using YOLOv8

"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

import time

from typing import Optional

import logging

from .models import DetectionResponse, HealthResponse

from .inference import BottleDetector

from .utils import validate_image, strip_metadata

Configure logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

Initialize FastAPI app

app = FastAPI(

title="SnapCount AI - ML Service",

description="Bottle detection API using YOLOv8",

version="1.0.0"

)

Configure CORS

app.add_middleware(

CORSMiddleware,

allow_origins=["*"], # Update in production

allow_credentials=True,

allow_methods=["*"],

allow_headers=["*"],

)

Initialize detector (loads model on startup)

detector = BottleDetector()

@app.on_event("startup")

async def startup_event():

"""Load model on startup"""

logger.info("🚀 Starting SnapCount ML Service...")

logger.info(f"📦 Model loaded: {detector.model_loaded}")

logger.info("✅ Service ready!")

@app.get("/", response_model=dict)

async def root():

"""Root endpoint"""

return {

"service": "SnapCount AI - ML Inference",

"version": "1.0.0",

"status": "running",

"endpoints": {

"detect": "/detect",

"health": "/health"

}

}

@app.get("/health", response_model=HealthResponse)

async def health_check():

"""Health check endpoint"""

return HealthResponse(

status="healthy" if detector.model_loaded else "unhealthy",

model_loaded=detector.model_loaded,

version="1.0.0"

)

@app.post("/detect", response_model=DetectionResponse)

async def detect_bottles(

image: UploadFile = File(..., description="Shelf photo (JPEG/PNG, max 10MB)"),

confidence_threshold: Optional[float] = Form(0.5, description="Detection confidence threshold (0.0-1.0)")

):

"""

Detect bottles in shelf photo

Args:

image: Image file (JPEG/PNG)

confidence_threshold: Minimum confidence for detections (default: 0.5)

Returns:

DetectionResponse with bounding boxes and SKU predictions

"""

start_time = time.time()

try:

# Validate image

logger.info(f"📸 Received image: {image.filename}")

image_bytes = await image.read()

if not validate_image(image_bytes, max_size_mb=10):

raise HTTPException(

status_code=400,

detail="Invalid image. Must be JPEG/PNG and under 10MB"

)

# Strip metadata for privacy

clean_image_bytes = strip_metadata(image_bytes)

# Run inference

logger.info(f"🔍 Running inference with threshold: {confidence_threshold}")

detections = detector.detect(clean_image_bytes, confidence_threshold)

# Calculate inference time

inference_time = int((time.time() - start_time) * 1000)

logger.info(f"✅ Detected {len(detections['detections'])} bottles in {inference_time}ms")

# Build response

response = DetectionResponse(

success=True,

image_width=detections["image_width"],

image_height=detections["image_height"],

detections=detections["detections"],

total_detections=len(detections["detections"]),

inference_time_ms=inference_time

)

return response

except Exception as e:

logger.error(f"❌ Error during detection: {str(e)}")

raise HTTPException(

status_code=500,

detail=f"Detection failed: {str(e)}"

)

@app.exception_handler(Exception)

async def global_exception_handler(request, exc):

"""Global exception handler"""

logger.error(f"❌ Unhandled exception: {str(exc)}")

return JSONResponse(

status_code=500,

content={

"success": False,

"error": "Internal server error",

"detail": str(exc)

}

)

if __name__ == "__main__":

import uvicorn

uvicorn.run(

"app.main:app",

host="0.0.0.0",

port=8000,

reload=True,

log_level="info"

)

```
