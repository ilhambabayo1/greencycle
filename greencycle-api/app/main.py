import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .api.routes import router
from .config import settings
from .services import model_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("greencycle")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Waste image classification API built from the GreenCycle notebook "
        "(MobileNetV2 transfer learning). Upload an image and get the predicted "
        "waste category with confidence scores."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_PREFIX)


@app.get("/", include_in_schema=False)
async def home():
    """Serve the GreenCycle web UI."""
    return FileResponse(
        str(__import__("pathlib").Path(__file__).parent / "static" / "index.html")
    )


@app.get("/api/health", tags=["health"], include_in_schema=False)
async def root():
    return {"message": "GreenCycle Waste Classifier API", "docs": "/docs"}


@app.on_event("startup")
async def startup_event():
    """Load the model at startup so the first request is fast.

    A missing model file is logged but not fatal: /health reports 'degraded'
    and /predict returns a 503 until the model is available.
    """
    try:
        model_service.get_model()
        logger.info("Model loaded from %s", settings.MODEL_PATH)
    except Exception as exc:
        logger.error("Model failed to load at startup: %s", exc)
