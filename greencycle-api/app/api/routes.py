from fastapi import APIRouter, UploadFile, File

from ..schemas import HealthResponse, PredictionResponse
from ..services import model_service, predictor
from ..config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok" if model_service.is_model_loaded() else "degraded",
        model_loaded=model_service.is_model_loaded(),
        model_path=settings.MODEL_PATH,
        app_version=settings.APP_VERSION,
    )


@router.post("/predict", response_model=PredictionResponse, tags=["classification"])
async def predict(file: UploadFile = File(..., description="Image to classify (jpg/png/webp)")):
    """Classify an uploaded waste image into GreenCycle categories."""
    return await predictor.predict_image(file)
