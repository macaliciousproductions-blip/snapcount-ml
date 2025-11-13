python

"""

Pydantic models for API requests and responses

"""

from pydantic import BaseModel, Field

from typing import List, Optional

class BoundingBox(BaseModel):

"""Bounding box coordinates"""

x1: int = Field(..., description="Top-left X coordinate")

y1: int = Field(..., description="Top-left Y coordinate")

x2: int = Field(..., description="Bottom-right X coordinate")

y2: int = Field(..., description="Bottom-right Y coordinate")

class Detection(BaseModel):

"""Single bottle detection"""

sku_name: str = Field(..., description="Detected SKU name or class")

brand: Optional[str] = Field(None, description="Detected brand name")

confidence: float = Field(..., description="Detection confidence (0.0-1.0)")

bbox: BoundingBox = Field(..., description="Bounding box coordinates")

class DetectionResponse(BaseModel):

"""Response from detection endpoint"""

success: bool = Field(..., description="Whether detection was successful")

image_width: int = Field(..., description="Original image width in pixels")

image_height: int = Field(..., description="Original image height in pixels")

detections: List[Detection] = Field(..., description="List of detected bottles")

total_detections: int = Field(..., description="Total number of detections")

inference_time_ms: int = Field(..., description="Inference time in milliseconds")

class HealthResponse(BaseModel):

"""Health check response"""

status: str = Field(..., description="Service status")

model_loaded: bool = Field(..., description="Whether ML model is loaded")

version: str = Field(..., description="API version")

```

