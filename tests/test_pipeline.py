import sys
import os

# 🔥 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.pipeline import AlphaPipeline


@pytest.fixture
def pipeline():
    """
    Initialize pipeline once for tests
    """
    return AlphaPipeline()


# ==============================
# TEST: PIPELINE RUNS
# ==============================
def test_pipeline_runs(pipeline):
    result = pipeline.run("AAPL")

    assert isinstance(result, dict), "Output should be a dictionary"


# ==============================
# TEST: REQUIRED KEYS EXIST
# ==============================
def test_pipeline_output_keys(pipeline):
    result = pipeline.run("AAPL")

    expected_keys = {
        "ticker",
        "num_articles",
        "signal",
        "confidence",
        "sentiment_details",
    }

    assert expected_keys.issubset(result.keys()), "Missing expected keys"


# ==============================
# TEST: SIGNAL VALUES
# ==============================
def test_signal_values(pipeline):
    result = pipeline.run("AAPL")

    assert result["signal"] in [-1, 0, 1], "Signal must be -1, 0, or 1"


# ==============================
# TEST: CONFIDENCE RANGE
# ==============================
def test_confidence_range(pipeline):
    result = pipeline.run("AAPL")

    assert 0 <= result["confidence"] <= 1, "Confidence must be between 0 and 1"