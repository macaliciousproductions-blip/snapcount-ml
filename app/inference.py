python

"""

YOLOv8 inference logic for bottle detection

"""

import cv2

import numpy as np

from ultralytics import YOLO

from typing import Dict, List

import logging

logger = logging.getLogger(__name__)

class BottleDetector:

"""YOLOv8-based bottle detector"""

def __init__(self, model_path: str = "yolov8n.pt"):

"""

Initialize detector with YOLOv8 model

Args:

model_path: Path to YOLOv8 weights file

"""

self.model_path = model_path

self.model_loaded = False

try:

logger.info(f"Loading YOLOv8 model from {model_path}...")

self.model = YOLO(model_path)

self.model_loaded = True

logger.info("✅ Model loaded successfully!")

except Exception as e:

logger.error(f"❌ Failed to load model: {e}")

self.model = None

def detect(self, image_bytes: bytes, confidence_threshold: float = 0.5) -> Dict:

"""

Detect bottles in image

Args:

image_bytes: Image data as bytes

confidence_threshold: Minimum confidence for detections

Returns:

Dict with detections and image metadata

"""

if not self.model_loaded:

raise RuntimeError("Model not loaded")

# Convert bytes to numpy array

nparr = np.frombuffer(image_bytes, np.uint8)

image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

if image is None:

raise ValueError("Failed to decode image")

# Get image dimensions

height, width = image.shape[:2]

# Run inference

results = self.model(image, conf=confidence_threshold, verbose=False)

# Parse detections

detections = []

for result in results:

boxes = result.boxes

for box in boxes:

# Get box coordinates

x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

# Get confidence and class

confidence = float(box.conf[0].cpu().numpy())

class_id = int(box.cls[0].cpu().numpy())

class_name = self.model.names[class_id]

# Create detection object

detection = {

"sku_name": class_name,

"brand": class_name.split()[0] if " " in class_name else class_name,

"confidence": confidence,

"bbox": {

"x1": int(x1),

"y1": int(y1),

"x2": int(x2),

"y2": int(y2)

}

}

detections.append(detection)

return {

"image_width": width,

"image_height": height,

"detections": detections

}
