import csv
import json
import os
import sys
from datetime import datetime

# Add project root to sys.path so client imports succeed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from client.api import get_resolved_markets, get_trending_markets

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "ml", "data.csv")


def extract_price(market):
    """Safely extract the Yes/Outcome-0 contract price."""
    try:
        prices = json.loads(market.get("outcomePrices", "[]"))
        if prices and len(prices) > 0:
            return float(prices[0])
    except Exception:
        pass
    
    last_price = market.get("lastTradePrice")
    if last_price is not None:
        return float(last_price)
    
    best_bid = market.get("bestBid")
    if best_bid is not None:
        return float(best_bid)

    return 0.5


def collect_resolved_dataset(limit=250):
    """
    Fetch resolved markets from Polymarket and build a labeled dataset for ML training.
    Outcomes: 1 = primary outcome occurred (['1', '0']), 0 = opponent outcome (['0', '1']).
    """
    print(f"Fetching up to {limit} resolved markets from Polymarket...")
    markets = get_resolved_markets(limit=limit)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    rows = []
    for m in markets:
        outcome_prices_raw = m.get("outcomePrices", "")
        if outcome_prices_raw == '["1", "0"]':
            outcome = 1
        elif outcome_prices_raw == '["0", "1"]':
            outcome = 0
        else:
            continue

        try:
            price = extract_price(m)
            volume = float(m.get("volume", 0) or 0)
            volume24hr = float(m.get("volume24hr", 0) or 0)
            liquidity = float(m.get("liquidity", 0) or 0)
            # Use liquidity-adjusted volume as trade activity proxy
            num_trades = int(volume / max(liquidity, 1.0)) if liquidity > 0 else 10

            rows.append({
                "timestamp": datetime.now().isoformat(),
                "price": price,
                "volume": volume,
                "volume24hr": volume24hr,
                "num_trades": num_trades,
                "outcome": outcome,
                "question": m.get("question", "")[:80]
            })
        except Exception:
            continue

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["timestamp", "price", "volume", "volume24hr", "num_trades", "outcome", "question"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} labeled resolved market records to {DATA_FILE}")
    return len(rows)


def save_market_data(market):
    """Append a live market snapshot to ml/data.csv."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    file_exists = os.path.isfile(DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["timestamp", "price", "volume", "volume24hr", "num_trades", "outcome", "question"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "price": market.get("price", 0.5),
            "volume": market.get("volume", 0),
            "volume24hr": market.get("volume24hr", 0),
            "num_trades": market.get("trades", 0),
            "outcome": market.get("outcome", ""),
            "question": market.get("question", "")[:80]
        })


if __name__ == "__main__":
    collect_resolved_dataset(200)