# GreenCycle ♻️

Waste classification project: a MobileNetV2 transfer-learning model (Keras, 224x224 input)
that classifies images of household waste into recyclable categories, served via a FastAPI
REST API packaged with Docker.

## Repository structure

```
+-- Green_cycle2.ipynb            # Main training notebook (data prep, training, evaluation)
+-- Green_cycle_backup.ipynb      # Backup copy of the notebook
+-- green_cycle_backup.py         # Exported Python version of the notebook
+-- my_model.keras                # Trained Keras model
+-- Dockerfile                    # Docker image for the training/model environment
+-- test_images/                  # Sample images for testing predictions
+-- greencycle-api/               # FastAPI serving service (see greencycle-api/README.md)
    +-- app/                      # FastAPI app, routes, services
    +-- models/                   # Mount point for my_model.keras (+ class_indices.json)
    +-- requirements.txt
    +-- Dockerfile / docker-compose.yml
```

## Model

- **Architecture:** MobileNetV2 (transfer learning) + custom classification head
- **Input:** 224x224 RGB images
- **Dataset:** [sumn2u/garbage-classification-v2](https://huggingface.co/datasets/sumn2u/garbage-classification-v2)
- **Classes:** battery, biological, cardboard, clothes, glass, metal, paper, plastic, shoes, trash

## API service

FastAPI service exposing:

| Method | Path              | Description                                |
|--------|-------------------|--------------------------------------------|
| GET    | /                 | Welcome message                            |
| GET    | /api/v1/health    | Service/model health                       |
| POST   | /api/v1/predict   | Upload an image (multipart) -> prediction  |

Run locally:

```bash
cd greencycle-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run with Docker:

```bash
cd greencycle-api
docker compose up --build
```

Then test:

```bash
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/predict -F "file=@test_images/apple.jpg"
```

Swagger UI is available at `http://localhost:8000/docs`.

## Getting started (training)

1. Open `Green_cycle2.ipynb` in Jupyter / VS Code / Colab.
2. Run the cells to download the dataset, train the model, and export `my_model.keras`.
3. Copy `my_model.keras` (optionally with `class_indices.json`) into `greencycle-api/models/`.
4. Serve it via the API as described above.
