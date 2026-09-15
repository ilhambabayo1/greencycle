# GreenCycle Waste Classification API

FastAPI service that serves the waste classifier trained in Greencycle1.ipynb
(MobileNetV2 transfer learning, 224x224 input, Keras .keras format), packaged for Docker.

## Project structure

```
greencycle-api/
+-- app/
|   +-- __init__.py
|   +-- main.py                 # FastAPI app, CORS, startup model loading
|   +-- config.py               # Env-driven settings (model path, image size, limits)
|   +-- schemas.py              # Pydantic request/response models
|   +-- api/
|   |   +-- __init__.py
|   |   +-- routes.py           # /health and /predict endpoints
|   +-- services/
|       +-- __init__.py
|       +-- model_service.py    # Lazy model loading + class-name resolution
|       +-- predictor.py        # Image validation, preprocessing, inference
+-- models/                     # Put my_model.keras (+ class_indices.json) here
+-- requirements.txt
+-- Dockerfile
+-- docker-compose.yml
+-- .dockerignore
+-- .env.example
+-- README.md
```

## Endpoints

| Method | Path              | Description                                |
|--------|-------------------|--------------------------------------------|
| GET    | /                 | Welcome message                            |
| GET    | /api/v1/health    | Service/model health                       |
| POST   | /api/v1/predict   | Upload an image (multipart) -> prediction  |
| GET    | /docs             | Swagger UI                                 |

## Local run (without Docker)

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker deployment

1. Copy the trained model from the notebook (model.save('my_model.keras')) into ./models/my_model.keras
2. Build and run:

docker compose up --build

The models/ folder is mounted as a read-only volume, so you can swap models without rebuilding.

3. Test:

curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/predict -F "file=@plastic_bottle.jpg"

## Classes (dataset: sumn2u/garbage-classification-v2)

battery, biological, cardboard, clothes, glass, metal, paper, plastic, shoes, trash

Place class_indices.json (e.g. {"battery": 0, "biological": 1, ...}) next to the model
to guarantee class order matches training; otherwise the built-in default list is used.
