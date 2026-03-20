import yfinance as yf
import pandas as pd
import numpy as np

from src.pipeline import AlphaPipeline
from src.utils import setup_logger

logger = setup_logger(__name__)


class Backtester:
    """
    Backtests the sentiment-based trading strategy.
    """

    def __init__(self):
        self.pipeline = AlphaPipeline()

    # ==============================
    # FETCH PRICE DATA
    # ==============================
    def get_price_data(self, ticker: str, period: str = "3mo") -> pd.DataFrame:
        """
        Fetch historical price data using yfinance
        """

        logger.info(f"Fetching price data for {ticker}")

        df = yf.download(ticker, period=period, interval="1d")

        if df.empty:
            logger.error("No price data found")
            return pd.DataFrame()

        df = df[["Close"]]
        df["returns"] = df["Close"].pct_change()

        return df

    # ==============================
    # RUN BACKTEST
    # ==============================
    def run(self, ticker: str) -> dict:
        """
        Run full backtest
        """

        # Step 1: Get price data
        df = self.get_price_data(ticker)

        if df.empty:
            return {"error": "No price data"}

        signals = []

        # Step 2: Generate signals for each day
        for date in df.index[:-1]:  # skip last day
            result = self.pipeline.run(ticker)

            if "error" in result:
                signals.append(0)
            else:
                signals.append(result["signal"])

        # Align signals with dataframe
        df = df.iloc[: len(signals)]
        df["signal"] = signals

        # Step 3: Strategy returns (next day return * signal)
        df["strategy_returns"] = df["signal"].shift(1) * df["returns"]

        df.dropna(inplace=True)

        # Step 4: Performance metrics
        total_return = (1 + df["strategy_returns"]).prod() - 1

        sharpe_ratio = (
            df["strategy_returns"].mean()
            / df["strategy_returns"].std()
        ) * np.sqrt(252)

        result = {
            "ticker": ticker,
            "total_return": float(total_return),
            "sharpe_ratio": float(sharpe_ratio),
            "num_trades": int((df["signal"] != 0).sum()),
        }

        logger.info(f"Backtest result: {result}")

        return result