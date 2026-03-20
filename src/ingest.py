import requests
import json
from typing import List, Dict
from src.config import config
from src.utils import setup_logger, ensure_directories, get_timestamp

logger = setup_logger(__name__)


class NewsIngestor:
    """
    Handles ingestion of financial news from multiple sources.
    """

    def __init__(self):
        ensure_directories()

    # ==============================
    # NEWS DATA.IO (PRIMARY SOURCE)
    # ==============================
    def fetch_newsdata(self, ticker: str) -> List[Dict]:
        """
        Fetch news from NewsData.io API
        """

        url = "https://newsdata.io/api/1/news"

        params = {
            "apikey": config.NEWSDATA_KEY,
            "q": ticker,
            "language": "en",
            "category": "business",
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            articles = []

            if "results" in data:
                for item in data["results"][: config.NEWS_LIMIT]:
                    articles.append(
                        {
                            "source": "newsdata",
                            "title": item.get("title"),
                            "description": item.get("description"),
                            "published_at": item.get("pubDate"),
                        }
                    )

            logger.info(f"Fetched {len(articles)} articles from NewsData")

            return articles

        except Exception as e:
            logger.error(f"NewsData API failed: {e}")
            return []

    # ==============================
    # ALPHA VANTAGE (FALLBACK)
    # ==============================
    def fetch_alpha_vantage(self, ticker: str) -> List[Dict]:
        """
        Fetch news from Alpha Vantage API
        """

        url = "https://www.alphavantage.co/query"

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": config.ALPHAVANTAGE_KEY,
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            articles = []

            if "feed" in data:
                for item in data["feed"][: config.NEWS_LIMIT]:
                    articles.append(
                        {
                            "source": "alphavantage",
                            "title": item.get("title"),
                            "description": item.get("summary"),
                            "published_at": item.get("time_published"),
                        }
                    )

            logger.info(f"Fetched {len(articles)} articles from Alpha Vantage")

            return articles

        except Exception as e:
            logger.error(f"Alpha Vantage API failed: {e}")
            return []

    # ==============================
    # MASTER FUNCTION (WITH FALLBACK)
    # ==============================
    def get_news(self, ticker: str) -> List[Dict]:
        """
        Fetch news using primary + fallback logic
        """

        logger.info(f"Fetching news for {ticker}")

        articles = self.fetch_newsdata(ticker)

        if not articles:
            logger.warning("NewsData failed. Switching to Alpha Vantage...")
            articles = self.fetch_alpha_vantage(ticker)

        if not articles:
            logger.error("All news sources failed.")
            return []

        # Save raw data
        self.save_raw_data(ticker, articles)

        return articles

    # ==============================
    # SAVE RAW DATA
    # ==============================
    def save_raw_data(self, ticker: str, articles: List[Dict]):
        """
        Save raw news data to disk
        """

        timestamp = get_timestamp()
        file_path = f"{config.RAW_DATA_DIR}/{ticker}_{timestamp}.json"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=4)

            logger.info(f"Saved raw data to {file_path}")

        except Exception as e:
            logger.error(f"Failed to save raw data: {e}")