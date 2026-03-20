from typing import List, Dict
from src.config import config
from src.utils import setup_logger

logger = setup_logger(__name__)


class SentimentStrategy:
    """
    Converts sentiment scores into trading signals.
    """

    def __init__(self):
        self.threshold = config.SENTIMENT_THRESHOLD

    # ==============================
    # AGGREGATE SENTIMENT
    # ==============================
    def aggregate_sentiment(self, articles: List[Dict]) -> Dict:
        """
        Compute average sentiment across all articles
        """

        if not articles:
            logger.warning("No articles provided for aggregation")
            return {
                "avg_positive": 0.0,
                "avg_negative": 0.0,
                "avg_neutral": 0.0,
            }

        total_pos = 0
        total_neg = 0
        total_neu = 0

        for article in articles:
            sentiment = article["sentiment"]

            total_pos += sentiment["positive"]
            total_neg += sentiment["negative"]
            total_neu += sentiment["neutral"]

        n = len(articles)

        aggregated = {
            "avg_positive": total_pos / n,
            "avg_negative": total_neg / n,
            "avg_neutral": total_neu / n,
        }

        logger.info(f"Aggregated sentiment: {aggregated}")

        return aggregated

    # ==============================
    # GENERATE SIGNAL
    # ==============================
    def generate_signal(self, aggregated_sentiment: Dict) -> Dict:
        """
        Convert aggregated sentiment into trading signal
        """

        pos = aggregated_sentiment["avg_positive"]
        neg = aggregated_sentiment["avg_negative"]

        # Signal logic
        if pos > self.threshold:
            signal = 1   # BUY
        elif neg > self.threshold:
            signal = -1  # SELL
        else:
            signal = 0   # HOLD

        result = {
            "signal": signal,
            "confidence": max(pos, neg),
            "details": aggregated_sentiment,
        }

        logger.info(f"Generated signal: {result}")

        return result

    # ==============================
    # FULL PIPELINE STEP
    # ==============================
    def run(self, articles: List[Dict]) -> Dict:
        """
        Full strategy pipeline:
        sentiment -> aggregation -> signal
        """

        aggregated = self.aggregate_sentiment(articles)
        signal = self.generate_signal(aggregated)

        return signal