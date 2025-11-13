```dockerfile

FROM python:3.11-slim

Set working directory

WORKDIR /app

Install system dependencies

RUN apt-get update && apt-get install -y \

libgl1-mesa-glx \

libglib2.0-0 \

&& rm -rf /var/lib/apt/lists/*

Copy requirements from ml-service folder

COPY ml-service/requirements.txt .

Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt

Copy application code from ml-service folder

COPY ml-service/app/ ./app/

Create models directory (model will be downloaded at runtime if needed)

RUN mkdir -p ./models

Set environment variables

ENV PYTHONUNBUFFERED=1

ENV MODEL_PATH=./models/yolov8_bottles.pt

ENV PORT=8000

Expose port (Railway will override with $PORT)

EXPOSE 8000

Run application - use $PORT env var for Railway compatibility

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

```

---

Option 3: Add railway.toml Config

Create or update `ml-service/railway.toml`:

```toml

[build]

builder = "dockerfile"

dockerfilePath = "Dockerfile"

[deploy]

startCommand = "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"

```
