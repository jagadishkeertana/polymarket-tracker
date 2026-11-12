import os
from dotenv import load_dotenv

load_dotenv()

# config.py — alert settings loaded securely from .env
EMAIL_FROM      = os.getenv("EMAIL_FROM")
EMAIL_TO        = os.getenv("EMAIL_TO")
APP_PASSWORD    = os.getenv("APP_PASSWORD")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", 20))
