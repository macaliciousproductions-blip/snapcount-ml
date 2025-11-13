FROM python:3.11-slim

#Set working directory

WORKDIR /app

#Install system dependencies

RUN apt-get update && apt-get install -y \

libgl1-mesa-glx \

libglib2.0-0 \

&& rm -rf /var/lib/apt/lists/*

Copy requirements from ml-service

COPY ml-service/requirements.txt .

#Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt

#Copy application code from ml-service

COPY ml-service/app/ ./app/

#Create models directory

RUN mkdir -p ./models

#Set environment variables

ENV PYTHONUNBUFFERED=1

ENV MODEL_PATH=./models/yolov8_bottles.pt

ENV PORT=8000

#Expose port

EXPOSE 8000

#Run application - use $PORT env var for Railway

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
