from pydantic import BaseModel, Field


class PredictionResult(BaseModel):
    """A single class prediction with its confidence."""
    class_name: str = Field(..., description="Waste category, e.g. 'battery'")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Softmax probability")


class PredictionResponse(BaseModel):
    """Response of the /predict endpoint."""
    filename: str
    top_prediction: PredictionResult
    all_predictions: list[PredictionResult] = Field(
        ..., description="All classes sorted by confidence (descending)"
    )
    model_version: str
    inference_time_ms: float = Field(..., description="Model inference wall time in ms")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_path: str
    app_version: str
