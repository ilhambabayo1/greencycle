import json
import os

from ..config import settings

_model = None
_class_names: list[str] = []


class ModelNotLoadedError(RuntimeError):
    """Raised when prediction is requested but the model failed to load."""


def get_model():
    """Return the loaded Keras model, loading it on first access (lazy singleton)."""
    global _model
    if _model is None:
        _load()
    return _model


def get_class_names() -> list[str]:
    if _model is None:
        _load()
    return _class_names


def is_model_loaded() -> bool:
    return _model is not None


def _load() -> None:
    global _model, _class_names

    if not os.path.exists(settings.MODEL_PATH):
        raise ModelNotLoadedError(
            f"Model file not found at '{settings.MODEL_PATH}'. "
            "Copy the model trained in Greencycle1.ipynb (my_model.keras) into ./models/ "
            "or set MODEL_PATH."
        )

    # Imported lazily so the API can start (and report health) even if TF is
    # slow to import, and so unit tests without TF can still import modules.
    from tensorflow import keras

    # compile=False: weights load fine; optimizer state from Colab's TF version
    # is irrelevant for inference and fails to load across versions.
    _model = keras.models.load_model(settings.MODEL_PATH, compile=False)

    # Prefer class order saved alongside the model; fall back to defaults.
    _class_names = _load_class_indices() or settings.DEFAULT_CLASSES


def _load_class_indices() -> dict | None:
    """Load {'battery': 0, ...} saved next to the model as class_indices.json."""
    path = os.path.join(os.path.dirname(settings.MODEL_PATH), "class_indices.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        indices = json.load(f)  # {"battery": 0, "biological": 1, ...}
    return sorted(indices, key=indices.get)
