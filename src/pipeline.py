from src.ingest import NewsIngestor
from src.features import TextPreprocessor
from src.model import SentimentModel
from src.strategy import SentimentStrategy
from src.utils import setup_logger

logger = setup_logger(__name__)


class AlphaPipeline:
    """
    Main pipeline that connects all components:
    ingest -> preprocess -> model -> strategy
    """

    def __init__(self):
        logger.info("Initializing Alpha Pipeline...")

        self.ingestor = NewsIngestor()
        self.preprocessor = TextPreprocessor()
        self.model = SentimentModel()
        self.strategy = SentimentStrategy()

        logger.info("Pipeline initialized successfully")

    # ==============================
    # RUN FULL PIPELINE
    # ==============================
    def run(self, ticker: str) -> dict:
        """
        Run full pipeline for a given stock ticker
        """

        logger.info(f"Running pipeline for {ticker}")

        # Step 1: Ingest
        raw_articles = self.ingestor.get_news(ticker)

        if not raw_articles:
            logger.error("No articles fetched")
            return {"error": "No data available"}

        # Step 2: Preprocess
        processed_articles = self.preprocessor.process_articles(raw_articles)

        if not processed_articles:
            logger.error("No processed articles")
            return {"error": "Processing failed"}

        # Step 3: Model Inference
        sentiment_results = self.model.predict_batch(processed_articles)

        # Step 4: Strategy
        signal = self.strategy.run(sentiment_results)

        # Final Output
        output = {
            "ticker": ticker,
            "num_articles": len(sentiment_results),
            "signal": signal["signal"],
            "confidence": signal["confidence"],
            "sentiment_details": signal["details"],
        }

        logger.info(f"Pipeline output: {output}")

        return output