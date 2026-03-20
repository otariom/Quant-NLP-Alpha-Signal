from fastapi import FastAPI, Query
from src.pipeline import AlphaPipeline
from src.backtest import Backtester
from src.utils import setup_logger

logger = setup_logger(__name__)

# Initialize app
app = FastAPI(
    title="Quant NLP Alpha Signal API",
    description="Generates trading signals using FinBERT sentiment analysis",
    version="1.0"
)

# Initialize pipeline + backtester
pipeline = AlphaPipeline()
backtester = Backtester()


# ==============================
# ROOT ENDPOINT
# ==============================
@app.get("/")
def home():
    return {
        "message": "Quant NLP Alpha Signal API is running"
    }


# ==============================
# SIGNAL ENDPOINT
# ==============================
@app.get("/signal")
def get_signal(ticker: str = Query(..., description="Stock ticker symbol")):
    """
    Get real-time sentiment-based trading signal
    """

    logger.info(f"API call: /signal for {ticker}")

    result = pipeline.run(ticker)

    return result


# ==============================
# BACKTEST ENDPOINT
# ==============================
@app.get("/backtest")
def run_backtest(ticker: str = Query(..., description="Stock ticker symbol")):
    """
    Run backtest for a ticker
    """

    logger.info(f"API call: /backtest for {ticker}")

    result = backtester.run(ticker)

    return result