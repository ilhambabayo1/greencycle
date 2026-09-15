import os

class Settings:
    """Application settings sourced from environment variables (.env / docker-compose)."""
    APP_NAME: str = "GreenCycle Waste Classifier API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Path to the trained Keras model produced by Greencycle1.ipynb (cell: model.save('my_model.keras'))
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/my_model.keras")

    # Must match the trained model input (current model: MobileNetV2, 224x224)
    IMG_SIZE: int = int(os.getenv("IMG_SIZE", "224"))

    # Preprocessing used in training:
    #   "rescale"   -> pixels / 255   (custom CNN notebook, Green_cycle.ipynb)
    #   "mobilenet" -> tf.keras.applications.mobilenet_v2.preprocess_input
    #                  (MobileNetV2 transfer-learning notebook, Greencycle1/Green_cycle2.ipynb)
    PREPROCESS: str = os.getenv("PREPROCESS", "mobilenet")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp"}

    # Fallback if the model archive lacks class_indices metadata.
    DEFAULT_CLASSES: list = [
        "battery", "biological", "cardboard", "clothes",
        "glass", "metal", "paper", "plastic", "shoes", "trash",
    ]


settings = Settings()
