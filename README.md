# 📈 Quant-NLP-Alpha-Signal
### *Production-Grade MLOps Pipeline for Sentiment-Driven Algorithmic Trading*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI Status](https://github.com/otariom/Quant-NLP-Alpha-Signal/actions/workflows/ci.yml/badge.svg)](https://github.com/otariom/Quant-NLP-Alpha-Signal/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview
**Quant-NLP-Alpha-Signal** is an end-to-end MLOps pipeline designed to extract tradable signals from unstructured financial news. By leveraging **Alternative Data** and specialized NLP models (**FinBERT**), this system automates the transition from raw text to quantitative Alpha signals.

Unlike basic sentiment scripts, this project is built with a modular architecture, featuring automated data ingestion, a robust backtesting engine with no lookahead bias, and a FastAPI/Streamlit deployment layer.

---

## 🚀 Key Features
* **Automated Ingestion:** Multi-source news fetching via NewsData.io and Alpha Vantage.
* **Financial NLP:** State-of-the-art sentiment extraction using `ProsusAI/finbert` (HuggingFace).
* **Signal Logic:** Aggregated sentiment scoring to generate discrete BUY (1), HOLD (0), or SELL (-1) signals.
* **Quant Backtesting:** Integration with `yfinance` to validate signal performance against historical returns and Sharpe Ratio.
* **Production Ready:** CI/CD via GitHub Actions and a modular `src/` directory for scalability.
* **Interactive UI:** A Streamlit dashboard for real-time ticker analysis and confidence scores.

---

## 🏗 Architecture & Workflow
The system follows a strict linear pipeline to ensure data integrity:
1.  **Ingestion:** Scrapes headlines and descriptions; stores snapshots in JSON for reproducibility.
2.  **Preprocessing:** Cleans text and tokenizes data for transformer compatibility.
3.  **Inference:** FinBERT processes text to output probabilities (Positive/Neutral/Negative).
4.  **Strategy:** Sentiment is weighted and compared against a configurable threshold (e.g., > 0.7 for BUY).
5.  **Validation:** The backtester shifts signals by $T+1$ to ensure realistic execution simulations.

---

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **ML/NLP:** HuggingFace Transformers, PyTorch, FinBERT
* **Data Science:** Pandas, NumPy, yfinance
* **Backend/Frontend:** FastAPI, Streamlit
* **DevOps:** GitHub Actions (CI/CD), Pytest, MLflow (Integration in progress)

---

## 📂 Project Structure
```text
Quant-NLP-Alpha-Signal/
├── .github/workflows/    # CI/CD pipelines
├── api/                  # FastAPI service layer
│   └── main.py
├── data/                 # Raw and processed JSON storage
├── frontend/             # Streamlit dashboard
│   └── app.py
├── models/               # Model configurations and weights
├── src/                  # Core logic (Modular)
│   ├── ingest.py         # API ingestion logic
│   ├── features.py       # Text cleaning
│   ├── model.py          # FinBERT inference
│   ├── strategy.py       # Signal generation logic
│   ├── pipeline.py       # Orchestrator
│   └── backtest.py       # Performance metrics
├── tests/                # Unit tests (Pytest)
├── requirements.txt      # Dependency manifest
└── .env                  # Environment variables (Internal use only)
```
## ⚙️ Setup & Installation
* **1. Clone the Repository** :- git clone [https://github.com/otariom/Quant-NLP-Alpha-Signal.git](https://github.com/otariom/Quant-NLP-Alpha-Signal.git) cd Quant-NLP-Alpha-Signal
* **2. Create Environment** :- python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
* **3. Configure API Keys** :- Create a .env file in the root directory:
  * 1) NEWSDATA_IO_KEY=your_newsdata_key
  * 2) ALPHA_VANTAGE_KEY=your_alphavantage_key

## 🖥 How to Run
* **Run the Dashboard (Visual Analysis)** :- The Streamlit app allows you to input a ticker and see the Alpha signal instantly.
  * streamlit run frontend/app.py
    
* **Run the API (Production Service)** :- To serve signals as a JSON endpoint for trading bots:
  * uvicorn api.main:app --reload
    Access documentation at: http://127.0.0.1:8000/docs

* **Run Tests**
  *pytest tests/

## 📊 Performance & Backtesting
The backtesting engine calculates the effectiveness of the sentiment signal by comparing the strategy returns against a Buy-and-Hold benchmark.
* Metrics: Cumulative Returns, Daily Volatility, and Sharpe Ratio
* Execution Logic: Signals generated at time $t$ are applied to the "Open" price at $t+1$ to prevent lookahead bias—a common pitfall in financial ML projects.

## 🛡 Security & CI/CD
* Secrets Management: All API keys are managed via .env and are never committed to the repository (enforced by .gitignore).
* Continuous Integration: GitHub Actions automatically runs pytest on every push to ensure the pipeline remains unbroken and imports are valid.
  

 

