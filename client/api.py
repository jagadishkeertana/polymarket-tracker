import requests
import json

BASE_GAMMA = "https://gamma-api.polymarket.com"
BASE_CLOB  = "https://clob.polymarket.com"

def get_trending_markets(limit=10):
    """Fetch top markets by 24hr trading volume."""
    r = requests.get(f"{BASE_GAMMA}/markets", params={
        "active": "true",
        "closed": "false",
        "limit": limit,
        "order": "volume24hr",
        "ascending": "false"
    })
    r.raise_for_status()
    return r.json()

def get_resolved_markets(limit=10):
    """Fetch recently resolved/closed markets."""
    r = requests.get(f"{BASE_GAMMA}/markets", params={
        "closed": "true",
        "limit": limit,
        "order": "volume",
        "ascending": "false"
    })
    r.raise_for_status()
    return r.json()

def get_markets_by_category(category="politics", limit=10):
    """Fetch active markets filtered by category."""
    r = requests.get(f"{BASE_GAMMA}/markets", params={
        "active": "true",
        "closed": "false",
        "category": category,
        "limit": limit
    })
    r.raise_for_status()
    return r.json()

def get_order_book(token_id):
    """Fetch real-time order book for a specific market."""
    r = requests.get(f"{BASE_CLOB}/book", params={"token_id": token_id})
    r.raise_for_status()
    return r.json()