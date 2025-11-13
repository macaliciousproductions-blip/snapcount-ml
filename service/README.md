```markdown

SnapCount AI - ML Inference Service

This directory contains the Python FastAPI service for AI-powered bottle detection using YOLOv8.

Overview

The ML inference service processes shelf photos and detects bottles using a trained YOLOv8 model. It returns bounding boxes, SKU matches, and confidence scores for each detected bottle.

Architecture

```

ml-service/

├── app/

│ ├── __init__.py

│ ├── main.py # FastAPI application

│ ├── models.py # Pydantic models

│ ├── inference.py # YOLOv8 inference logic

│ └── utils.py # Helper functions

├── models/

│ └── yolov8_bottles.pt # Trained model weights

├── requirements.txt # Python dependencies

├── Dockerfile # Docker container

└── README.md # This file

```

Setup

1. Install Dependencies

```bash

pip install -r requirements.txt

```

2. Required Packages

•
`fastapi` - Web framework
•
`uvicorn` - ASGI server
•
`ultralytics` - YOLOv8 implementation
•
`opencv-python` - Image processing
•
`pillow` - Image handling
•
`python-multipart` - File upload support
3. Model Training

#### Dataset Collection

1.
Capture 50-100 photos of bar shelves in various lighting conditions
2.
Include different bottle types: liquor, beer, wine
3.
Vary angles, distances, and shelf configurations
4.
Ensure diverse brand representation
#### Labeling with Roboflow

1.
Create a Roboflow project: https://roboflow.com
2.
Upload your photos
3.
Draw bounding boxes around each bottle
4.
Label with SKU name or brand (e.g., "makers-mark-750ml")
5.
Add tags: category, size, brand
6.
Split dataset: 70% train, 20% validation, 10% test
7.
Apply augmentations:
•
Flip horizontal
•
Rotation: ±15 degrees
•
Brightness: ±20%
•
Blur: up to 1px
8.
Export in YOLOv8 format
#### Training Pipeline

```python

from ultralytics import YOLO

Initialize model

model = YOLO('yolov8n.pt') # Start with nano model

Train on your dataset

results = model.train(

data='path/to/data.yaml', # From Roboflow export

epochs=100,

imgsz=640,

batch=16,

name='snapcount_bottles',

patience=20, # Early stopping

save=True,

device=0 # GPU

)

Validate

metrics = model.val()

Export

model.export(format='pt') # Save trained weights

```

API Endpoints

POST /detect

Detects bottles in an uploaded image.

Request:

```bash

curl -X POST "http://localhost:8000/detect" \

-H "Content-Type: multipart/form-data" \

-F "image=@shelf_photo.jpg" \

-F "confidence_threshold=0.5"

```

Response:

```json

{

"success": true,

"image_width": 1920,

"image_height": 1080,

"detections": [

{

"sku_name": "makers-mark-750ml",

"brand": "Maker's Mark",

"confidence": 0.92,

"bbox": {

"x1": 145,

"y1": 220,

"x2": 198,

"y2": 380

}

},

{

"sku_name": "grey-goose-750ml",

"brand": "Grey Goose",

"confidence": 0.87,

"bbox": {

"x1": 210,

"y1": 215,

"x2": 245,

"y2": 375

}

}

],

"total_detections": 2,

"inference_time_ms": 145

}

```

GET /health

Health check endpoint.

Response:

```json

{

"status": "healthy",

"model_loaded": true,

"version": "1.0.0"

}

```

Deployment

Local Development

```bash

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

Docker

```bash

docker build -t snapcount-ml:latest .

docker run -p 8000:8000 snapcount-ml:latest

```

Cloud Deployment

Option 1: Modal.com (Recommended for ML)

•
GPU-accelerated inference
•
Auto-scaling
•
Pay per compute
•
Deploy: `modal deploy app/main.py`
Option 2: Render

•
Easy deployment from GitHub
•
Auto-scaling
•
Good for CPU inference
•
Set service type to "Web Service"
Option 3: Vercel (Functions)

•
Serverless deployment
•
Limited to 10s execution time
•
Best for pre-warmed models
Option 4: Railway

•
Simple deployment
•
GPU support available
•
Good developer experience
Environment Variables

```bash

MODEL_PATH=./models/yolov8_bottles.pt

CONFIDENCE_THRESHOLD=0.5

MAX_UPLOAD_SIZE=10485760 # 10MB

CORS_ORIGINS=* # Update in production

LOG_LEVEL=info

```

Integration with SnapCount AI

Backend (Hono)

```typescript

// Create a proxy route in backend/src/routes/detect.ts

app.post("/api/detect", async (c) => {

const formData = await c.req.formData();

const image = formData.get("image");

// Forward to ML service

const response = await fetch("https://ml-service.railway.app/detect", {

method: "POST",

body: formData,

});

return c.json(await response.json());

});

```

Frontend (React Native)

```typescript

import * as ImagePicker from 'expo-image-picker';

// Capture photo

const result = await ImagePicker.launchCameraAsync({

quality: 0.8,

base64: false,

});

// Send to detection

const formData = new FormData();

formData.append('image', {

uri: result.uri,

type: 'image/jpeg',

name: 'shelf_photo.jpg',

});

const detections = await api.post('/api/detect', formData);

```

Model Performance

Target Metrics:

•
mAP@0.5: > 0.85
•
mAP@0.5:0.95: > 0.70
•
Inference time: < 200ms on GPU, < 1s on CPU
•
Precision: > 0.90 (avoid false positives)
•
Recall: > 0.85 (catch most bottles)
Privacy & Security

•
No facial recognition: Model trained only on bottles
•
Anonymized metadata: Strip EXIF data before processing
•
Secure storage: Images deleted after processing (optional retention)
•
HTTPS only: All API calls encrypted
•
Rate limiting: 100 requests per minute per user
•
File validation: Check file type, size, and format
Troubleshooting

Low Detection Accuracy

•
Increase training epochs
•
Add more labeled data
•
Improve lighting in photos
•
Use higher resolution images
•
Fine-tune confidence threshold
Slow Inference

•
Use YOLOv8n (nano) instead of YOLOv8x
•
Reduce image size to 640x640
•
Enable GPU acceleration
•
Use model quantization
•
Deploy on faster hardware
Wrong SKU Matches

•
Improve labeling consistency
•
Add more examples of similar bottles
•
Use transfer learning from pre-trained model
•
Implement post-processing logic
•
Allow user corrections to retrain
Next Steps

1.
Collect and label initial dataset (50-100 images)
2.
Train first model iteration
3.
Deploy ML service to Modal/Render
4.
Integrate with React Native app
5.
Test with real bar photos
6.
Collect user feedback and corrections
7.
Retrain with augmented dataset
8.
Deploy improved model
Support

For ML service issues:

•
Email: ml@snapcountai.com
•
GitHub: github.com/snapcount/ml-service
•
Documentation: docs.snapcountai.com/ml
---

Version: 1.0.0

Last Updated: 2025-11-12

Model: YOLOv8n trained on 100 bar shelf images


