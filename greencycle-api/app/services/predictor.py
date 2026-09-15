import time

import numpy as np
from fastapi import HTTPException, UploadFile

from ..config import settings
from ..schemas import PredictionResult, PredictionResponse
from . import model_service

_ALLOWED = settings.ALLOWED_EXTENSIONS


async def predict_image(file: UploadFile) -> PredictionResponse:
    """Validate an uploaded image and run it through the waste classifier."""
    # --- validate extension ---
    name = file.filename or "upload"
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in _ALLOWED:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(_ALLOWED))}",
        )

    # --- read + validate size ---
    contents = await file.read()
    limit = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(contents) > limit:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(contents) / 1024 / 1024:.1f} MB). "
                   f"Max is {settings.MAX_FILE_SIZE_MB} MB.",
        )
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    # --- decode & preprocess exactly as in training (choose via PREPROCESS env) ---
    from io import BytesIO
    from PIL import Image

    try:
        img = Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode image file.")

    size = (settings.IMG_SIZE, settings.IMG_SIZE)
    img = img.resize(size)
    batch = np.asarray(img, dtype=np.float32)[np.newaxis, ...]

    if settings.PREPROCESS == "mobilenet":
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        batch = preprocess_input(batch)
    else:  # "rescale"
        batch = batch / 255.0

    # --- inference ---
    model = model_service.get_model()
    classes = model_service.get_class_names()

    start = time.perf_counter()
    probs = model.predict(batch, verbose=0)[0]
    elapsed_ms = (time.perf_counter() - start) * 1000

    order = np.argsort(probs)[::-1]
    all_preds = [
        PredictionResult(class_name=classes[i], confidence=float(probs[i]))
        for i in order
    ]

    return PredictionResponse(
        filename=name,
        top_prediction=all_preds[0],
        all_predictions=all_preds,
        model_version=settings.APP_VERSION,
        inference_time_ms=round(elapsed_ms, 2),
    )
