import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Central configuration class for the project.
    Controls API keys, model parameters, and system settings.
    """

    # ========================
    # API KEYS (from .env)
    # ========================
    NEWSDATA_KEY = os.getenv("NEWSDATA_KEY")
    ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")

    # ========================
    # DATA SETTINGS
    # ========================
    NEWS_LIMIT = 50
    LOOKBACK_DAYS = 1

    # ========================
    # MODEL SETTINGS
    # ========================
    MODEL_NAME = "ProsusAI/finbert"

    # ========================
    # STRATEGY SETTINGS
    # ========================
    SENTIMENT_THRESHOLD = 0.7

    # ========================
    # FILE PATHS
    # ========================
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

    MODEL_DIR = os.path.join(BASE_DIR, "models")

    # ========================
    # LOGGING
    # ========================
    LOG_LEVEL = "INFO"

    # ========================
    # API SETTINGS (FastAPI)
    # ========================
    HOST = "0.0.0.0"
    PORT = 8000


# Singleton instance
config = Config()