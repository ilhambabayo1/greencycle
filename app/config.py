import os


class Settings:
    APP_NAME: str = "GreenCycle"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./greencycle.db")


settings = Settings()
