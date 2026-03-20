import sys
import os

# 🔥 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.pipeline import AlphaPipeline

# Page config
st.set_page_config(
    page_title="Quant NLP Alpha Signal",
    page_icon="📈",
    layout="centered"
)

# Title
st.title("📈 Quant NLP Alpha Signal")
st.markdown("Generate trading signals using financial news sentiment (FinBERT)")

# Input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS)")

# Initialize pipeline
pipeline = AlphaPipeline()

# Button
if st.button("Generate Signal"):

    if not ticker:
        st.warning("Please enter a ticker")
    else:
        with st.spinner("Fetching data and analyzing sentiment..."):
            result = pipeline.run(ticker)

        if "error" in result:
            st.error(result["error"])
        else:
            signal = result["signal"]

            # Signal display
            if signal == 1:
                st.success("📈 BUY Signal")
            elif signal == -1:
                st.error("📉 SELL Signal")
            else:
                st.info("⏸ HOLD Signal")

            # Metrics
            st.subheader("Details")
            st.write(f"**Ticker:** {result['ticker']}")
            st.write(f"**Confidence:** {result['confidence']:.2f}")
            st.write(f"**Articles Analyzed:** {result['num_articles']}")

            # Sentiment breakdown
            st.subheader("Sentiment Breakdown")
            sentiment = result["sentiment_details"]

            st.write(f"Positive: {sentiment['avg_positive']:.2f}")
            st.write(f"Neutral: {sentiment['avg_neutral']:.2f}")
            st.write(f"Negative: {sentiment['avg_negative']:.2f}")