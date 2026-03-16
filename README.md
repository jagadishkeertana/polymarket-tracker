# 🔮 Polymarket Tracker

A live prediction market dashboard built with Python, Streamlit, and the Polymarket API.

## 📸 Features

- **Live data** from Polymarket's public API
- **Interactive web dashboard** with filters by category
- **Bar charts** showing top markets by 24hr trading volume
- **Export to CSV & JSON** for offline analysis
- Clean modular Python code structure

## 🛠️ Tech Stack

- Python 3.11
- [Streamlit](https://streamlit.io/) — web dashboard
- [Plotly](https://plotly.com/) — interactive charts
- [Rich](https://rich.readthedocs.io/) — terminal tables
- [Polymarket Gamma API](https://gamma-api.polymarket.com) — market data
- [Polymarket CLOB API](https://clob.polymarket.com) — order book data

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/jagadishkeertana/polymarket-tracker.git
cd polymarket-tracker
```

### 2. Create virtual environment
```bash
py -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
py -m pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
py -m streamlit run dashboard.py
```

Open `http://localhost:8501` in your browser.

### 5. Or run the terminal tracker
```bash
py main.py
```

## 📁 Project Structure
```
polymarket-tracker/
├── client/
│   ├── __init__.py
│   └── api.py          # All Polymarket API calls
├── display/
│   ├── __init__.py
│   └── tables.py       # Rich terminal tables
├── saver/
│   ├── __init__.py
│   └── export.py       # CSV & JSON export
├── exports/            # Saved market data
├── dashboard.py        # Streamlit web dashboard
├── main.py             # Terminal entry point
└── README.md
```

## 📊 Data Sources

This project uses Polymarket's free public API — no API key required.

- `https://gamma-api.polymarket.com` — markets, categories
- `https://clob.polymarket.com` — order books

## 👩‍💻 Author

Built by Keertana