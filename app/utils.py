python

"""

Utility functions for image processing and validation

"""

from PIL import Image

import io

import logging

logger = logging.getLogger(__name__)

def validate_image(image_bytes: bytes, max_size_mb: int = 10) -> bool:

"""

Validate image file

Args:

image_bytes: Image data as bytes

max_size_mb: Maximum file size in MB

Returns:

True if valid, False otherwise

"""

# Check file size

size_mb = len(image_bytes) / (1024 * 1024)

if size_mb > max_size_mb:

logger.warning(f"Image too large: {size_mb:.2f}MB > {max_size_mb}MB")

return False

# Check if valid image

try:

image = Image.open(io.BytesIO(image_bytes))

image.verify()

return True

except Exception as e:

logger.error(f"Invalid image: {e}")

return False

def strip_metadata(image_bytes: bytes) -> bytes:

"""

Strip EXIF metadata from image for privacy

Args:

image_bytes: Image data as bytes

Returns:

Clean image bytes without metadata

"""

try:

image = Image.open(io.BytesIO(image_bytes))

# Remove EXIF data

data = list(image.getdata())

image_without_exif = Image.new(image.mode, image.size)

image_without_exif.putdata(data)

# Convert back to bytes

output = io.BytesIO()

image_without_exif.save(output, format=image.format or 'JPEG')

return output.getvalue()

except Exception as e:

logger.warning(f"Failed to strip metadata: {e}")

return image_bytes # Return original if stripping fails

```
