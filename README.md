# 🔮 Polymarket Tracker & ML Predictor

A real-time prediction market intelligence platform and machine learning forecasting dashboard built with Python, Streamlit, scikit-learn, and Polymarket APIs.

## 📸 Features

- **Live Market Feeds:** Real-time ingestion from Polymarket's Gamma and CLOB public APIs.
- **Machine Learning Forecasting:** Trained `RandomForestClassifier` predicting contract resolution probability based on market price, 24hr volume, and trade liquidity depth.
- **Alpha & Inefficiency Detector:** Automatically flags markets where the AI model's forecast diverges significantly from the crowd-implied probability ($\text{Edge} = P_{\text{AI}} - P_{\text{Market}}$).
- **Interactive Web Dashboard:** Streamlit interface with Plotly volume charts, progress bars, and real-time category filtering.
- **Automated Volatility Alerts:** Background email notifications (SMTP/SSL) when markets experience sharp price swings ($\ge 20\%$).
- **Offline Data Exports:** Structured CSV and JSON datasets for offline financial backtesting.

## 🛠️ Tech Stack

- **Python 3.11**
- **Machine Learning:** scikit-learn (`RandomForestClassifier`), pandas, numpy
- **Web Interface:** [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/)
- **CLI & Output:** [Rich](https://rich.readthedocs.io/)
- **APIs:** Polymarket Gamma API (market data) & CLOB API (order books)
- **Security:** python-dotenv (zero hardcoded secrets)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/jagadishkeertana/polymarket-tracker.git
cd polymarket-tracker
```

### 2. Set up virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the sample environment file and configure your credentials:
```bash
cp .env.example .env
```
Edit `.env` with your email and alert preferences:
```env
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient_email@gmail.com
APP_PASSWORD=your_16_char_gmail_app_password
ALERT_THRESHOLD=20
```

### 5. Train the ML Model
```bash
python ml/train.py
```
*Evaluates historical resolved contracts, outputting classification accuracy, ROC-AUC score, and serializing `ml/model.pkl`.*

### 6. Run the Dashboard
```bash
streamlit run dashboard.py
```
Open `http://localhost:8501` in your browser.

### 7. Run the Terminal Tracker
```bash
python main.py
```

## 📁 Project Structure

```
polymarket-tracker/
├── alerts/
│   └── email_alert.py        # Volatility monitor and SMTP email dispatcher
├── client/
│   └── api.py                # Resilient Polymarket API client with IPv4 binding
├── display/
│   └── tables.py             # Rich colorized terminal tables
├── exports/                  # Saved market datasets (CSV / JSON)
├── ml/
│   ├── train.py              # ML training pipeline (RandomForestClassifier)
│   └── predict.py            # Real-time inference & edge calculator
├── saver/
│   ├── dataset_collector.py  # Ingestion pipeline for historical & live contracts
│   └── export.py             # CSV & JSON file export utilities
├── .env.example              # Template for environment configuration
├── .gitignore                # Excludes secrets, caches, and model artifacts
├── config.py                 # Centralized configuration
├── dashboard.py              # Interactive Streamlit analytics dashboard
├── main.py                   # Terminal entry point
├── requirements.txt          # Pinned dependency manifest
└── README.md
```

## 📊 Model Performance

| Metric | Score |
|---|---|
| **Test Accuracy** | **76.0%** |
| **ROC-AUC** | **0.863** |
| **Brier Score Loss** | **0.1582** |

## 👩‍💻 Author

Built by Keertana
