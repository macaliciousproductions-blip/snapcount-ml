#### `ml-service/app/inference.py`

```python

"""

YOLOv8 inference logic for bottle detection

"""

import os

import io

import cv2

import numpy as np

from PIL import Image

from typing import Dict, List

import logging

logger = logging.getLogger(__name__)

class BottleDetector:

"""Bottle detection using YOLOv8"""

def __init__(self, model_path: str = "./models/yolov8_bottles.pt"):

"""

Initialize detector

Args:

model_path: Path to trained YOLOv8 weights

"""

self.model_path = model_path

self.model = None

self.model_loaded = False

# Try to load model

self._load_model()

def _load_model(self):

"""Load YOLOv8 model"""

try:

from ultralytics import YOLO

# Check if model exists

if os.path.exists(self.model_path):

logger.info(f"📦 Loading model from {self.model_path}")

self.model = YOLO(self.model_path)

self.model_loaded = True

logger.info("✅ Model loaded successfully")

else:

# Fallback to pretrained COCO model for demo

logger.warning(f"⚠️ Model not found at {self.model_path}")

logger.info("📦 Loading pretrained YOLOv8n for demo...")

self.model = YOLO('yolov8n.pt')

self.model_loaded = True

logger.info("✅ Pretrained model loaded (demo mode)")

except Exception as e:

logger.error(f"❌ Failed to load model: {str(e)}")

self.model_loaded = False

def detect(self, image_bytes: bytes, confidence_threshold: float = 0.5) -> Dict:

"""

Run detection on image

Args:

image_bytes: Image as bytes

confidence_threshold: Minimum confidence for detections

Returns:

Dictionary with detections and metadata

"""

if not self.model_loaded:

raise RuntimeError("Model not loaded")

# Convert bytes to image

image = Image.open(io.BytesIO(image_bytes))

image_array = np.array(image)

# Ensure RGB

if len(image_array.shape) == 2: # Grayscale

image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)

elif image_array.shape[2] == 4: # RGBA

image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)

# Get image dimensions

height, width = image_array.shape[:2]

# Run inference

results = self.model(image_array, conf=confidence_threshold, verbose=False)

# Parse results

detections = []

for result in results:

boxes = result.boxes

for i in range(len(boxes)):

# Get box coordinates

box = boxes.xyxy[i].cpu().numpy()

x1, y1, x2, y2 = map(int, box)

# Get confidence

confidence = float(boxes.conf[i].cpu().numpy())

# Get class name

class_id = int(boxes.cls[i].cpu().numpy())

class_name = result.names[class_id]

# Map class name to SKU (simplified for demo)

# In production, implement proper SKU matching logic

sku_name = self._map_class_to_sku(class_name)

brand = self._extract_brand(class_name)

detections.append({

"sku_name": sku_name,

"brand": brand,

"confidence": round(confidence, 2),

"bbox": {

"x1": x1,

"y1": y1,

"x2": x2,

"y2": y2

}

})

return {

"image_width": width,

"image_height": height,

"detections": detections

}

def _map_class_to_sku(self, class_name: str) -> str:

"""

Map detected class to SKU name

In production, this should:

1. Query database for SKU by visual features

2. Use OCR for label text matching

3. Match bottle shape and size

4. Consider location context

For demo, we'll use simple mapping

"""

# Demo mapping - replace with actual SKU database lookup

bottle_mappings = {

"bottle": "generic-bottle-750ml",

"wine": "red-wine-750ml",

"beer": "beer-bottle-355ml",

"cup": "cocktail-glass",

}

return bottle_mappings.get(class_name, f"{class_name}-unknown")

def _extract_brand(self, class_name: str) -> str:

"""Extract brand from class name"""

# Simplified - in production, use proper brand recognition

brand_map = {

"bottle": "Unknown",

"wine": "Unknown Wine",

"beer": "Unknown Beer",

}

return brand_map.get(class_name, "Unknown")

```
