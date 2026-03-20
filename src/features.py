import re
from typing import List, Dict
from src.utils import setup_logger

logger = setup_logger(__name__)


class TextPreprocessor:
    """
    Handles text cleaning and preparation for NLP models.
    """

    def __init__(self):
        pass

    # ==============================
    # CLEAN TEXT
    # ==============================
    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning:
        - remove URLs
        - remove special characters
        - normalize whitespace
        """

        if not text:
            return ""

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove special characters (keep basic punctuation)
        text = re.sub(r"[^a-zA-Z0-9\s.,]", "", text)

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # ==============================
    # COMBINE TITLE + DESCRIPTION
    # ==============================
    def combine_text(self, article: Dict) -> str:
        """
        Combine title and description into one string
        """

        title = article.get("title", "") or ""
        description = article.get("description", "") or ""

        combined = f"{title}. {description}"

        return self.clean_text(combined)

    # ==============================
    # PROCESS ARTICLES
    # ==============================
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Convert raw articles into cleaned text format
        """

        processed = []

        for article in articles:
            cleaned_text = self.combine_text(article)

            if cleaned_text:  # skip empty
                processed.append(
                    {
                        "text": cleaned_text,
                        "published_at": article.get("published_at"),
                        "source": article.get("source"),
                    }
                )

        logger.info(f"Processed {len(processed)} articles")

        return processed