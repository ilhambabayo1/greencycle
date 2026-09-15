FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    PORT=8000

WORKDIR /app

# Dependencies live in the greencycle-api subfolder
COPY greencycle-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI application
COPY greencycle-api/app ./app

# Trained model is committed at the repo root
RUN mkdir -p /app/models
COPY my_model.keras /app/models/my_model.keras

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
