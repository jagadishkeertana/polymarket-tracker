import csv
import json
import os
from datetime import datetime

EXPORT_DIR = "exports"

def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def save_to_json(markets, filename=None):
    ensure_export_dir()
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"markets_{timestamp}.json"
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(markets, f, indent=2, ensure_ascii=False)
    return filepath

def save_to_csv(markets, filename=None):
    ensure_export_dir()
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"markets_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)
    fields = ["id", "question", "category", "volume24hr",
              "volume", "endDate", "active", "closed"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for m in markets:
            writer.writerow({k: m.get(k, "") for k in fields})
    return filepath