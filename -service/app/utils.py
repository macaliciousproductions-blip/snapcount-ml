#### `ml-service/app/utils.py`

```python

"""

Utility functions for image processing and validation

"""

import io

from PIL import Image, ExifTags

import logging

logger = logging.getLogger(__name__)

def validate_image(image_bytes: bytes, max_size_mb: int = 10) -> bool:

"""

Validate image file

Args:

image_bytes: Image as bytes

max_size_mb: Maximum file size in MB

Returns:

True if valid, False otherwise

"""

try:

# Check file size

size_mb = len(image_bytes) / (1024 * 1024)

if size_mb > max_size_mb:

logger.warning(f"Image too large: {size_mb:.2f}MB > {max_size_mb}MB")

return False

# Try to open as image

image = Image.open(io.BytesIO(image_bytes))

# Check format

if image.format not in ['JPEG', 'PNG', 'JPG']:

logger.warning(f"Invalid format: {image.format}")

return False

# Check dimensions

width, height = image.size

if width < 100 or height < 100:

logger.warning(f"Image too small: {width}x{height}")

return False

if width > 4096 or height > 4096:

logger.warning(f"Image too large: {width}x{height}")

return False

return True

except Exception as e:

logger.error(f"Image validation failed: {str(e)}")

return False

def strip_metadata(image_bytes: bytes) -> bytes:

"""

Strip EXIF metadata from image for privacy

Args:

image_bytes: Original image bytes

Returns:

Clean image bytes without metadata

"""

try:

image = Image.open(io.BytesIO(image_bytes))

# Create new image without EXIF

clean_image = Image.new(image.mode, image.size)

clean_image.putdata(list(image.getdata()))

# Save to bytes

output = io.BytesIO()

clean_image.save(output, format=image.format or 'JPEG', quality=95)

output.seek(0)

return output.read()

except Exception as e:

logger.warning(f"Failed to strip metadata: {str(e)}")

# Return original if stripping fails

return image_bytes

def resize_image(image_bytes: bytes, max_dimension: int = 1280) -> bytes:

"""

Resize image if too large

Args:

image_bytes: Original image bytes

max_dimension: Maximum width or height

Returns:

Resized image bytes

"""

try:

image = Image.open(io.BytesIO(image_bytes))

width, height = image.size

# Check if resize needed

if width <= max_dimension and height <= max_dimension:

return image_bytes

# Calculate new dimensions

if width > height:

new_width = max_dimension

new_height = int(height * (max_dimension / width))

else:

new_height = max_dimension

new_width = int(width * (max_dimension / height))

# Resize

resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Save to bytes

output = io.BytesIO()

resized.save(output, format=image.format or 'JPEG', quality=90)

output.seek(0)

return output.read()

except Exception as e:

logger.warning(f"Failed to resize image: {str(e)}")

return image_bytes

```
