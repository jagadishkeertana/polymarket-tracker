import os
import socket
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.util import connection

# Force IPv4 socket resolution to prevent Cloudflare/AWS IPv6 handshake drops (WinError 10054)
connection.allowed_gai_family = lambda: socket.AF_INET

BASE_GAMMA = "https://gamma-api.polymarket.com"
BASE_CLOB  = "https://clob.polymarket.com"
CACHE_DIR  = os.path.join(os.path.dirname(__file__), "..", "exports")

# Setup resilient HTTP session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
})

retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)


def _load_fallback_markets(filename="trending_markets.json", limit=10):
    """Fallback to locally cached snapshot if external API encounters network drops."""
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data[:limit] if isinstance(data, list) else []
        except Exception:
            pass
    return []


def get_trending_markets(limit=10):
    """Fetch top markets by 24hr trading volume with local fallback."""
    try:
        r = session.get(f"{BASE_GAMMA}/markets", params={
            "active": "true",
            "closed": "false",
            "limit": limit,
            "order": "volume24hr",
            "ascending": "false"
        }, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data:
            return data
    except Exception as e:
        print(f"[WARN] Live API fetch error ({e}). Using cached market data.")

    return _load_fallback_markets("trending_markets.json", limit)


def get_resolved_markets(limit=100):
    """Fetch recently resolved/closed markets with ground-truth outcomes."""
    try:
        r = session.get(f"{BASE_GAMMA}/markets", params={
            "closed": "true",
            "limit": limit,
            "order": "volume",
            "ascending": "false"
        }, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[WARN] Live resolved markets fetch error ({e}).")
        return []


def get_markets_by_category(category="politics", limit=10):
    """Fetch active markets filtered by category."""
    try:
        r = session.get(f"{BASE_GAMMA}/markets", params={
            "active": "true",
            "closed": "false",
            "category": category,
            "limit": limit
        }, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data:
            return data
    except Exception as e:
        print(f"[WARN] Live category fetch error ({e}).")

    fallback = _load_fallback_markets("trending_markets.json", limit)
    # Filter fallback if category matches
    cat_filtered = [m for m in fallback if str(m.get("category", "")).lower() == category.lower()]
    return cat_filtered if cat_filtered else fallback[:limit]


def get_order_book(token_id):
    """Fetch real-time order book for a specific market."""
    try:
        r = session.get(f"{BASE_CLOB}/book", params={"token_id": token_id}, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[WARN] Order book fetch error: {e}")
        return {"bids": [], "asks": []}