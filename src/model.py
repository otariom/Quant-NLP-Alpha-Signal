from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

from src.config import config
from src.utils import setup_logger

logger = setup_logger(__name__)


class SentimentModel:
    """
    Handles FinBERT sentiment inference.
    """

    def __init__(self):
        logger.info("Loading FinBERT model...")

        self.tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.MODEL_NAME
        )

        self.model.eval()

        logger.info("FinBERT loaded successfully")

    # ==============================
    # PREDICT SINGLE TEXT
    # ==============================
    def predict(self, text: str) -> Dict:
        """
        Predict sentiment for a single text input
        """

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = F.softmax(logits, dim=1).detach().numpy()[0]

        # FinBERT label mapping
        labels = ["negative", "neutral", "positive"]

        result = {
            "negative": float(probs[0]),
            "neutral": float(probs[1]),
            "positive": float(probs[2]),
        }

        return result

    # ==============================
    # PREDICT BATCH
    # ==============================
    def predict_batch(self, articles: List[Dict]) -> List[Dict]:
        """
        Predict sentiment for multiple articles
        """

        results = []

        for article in articles:
            text = article["text"]

            sentiment = self.predict(text)

            results.append(
                {
                    "text": text,
                    "published_at": article["published_at"],
                    "source": article["source"],
                    "sentiment": sentiment,
                }
            )

        logger.info(f"Scored {len(results)} articles")

        return results