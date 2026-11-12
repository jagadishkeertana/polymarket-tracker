import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM   = os.getenv("EMAIL_FROM")
EMAIL_TO     = os.getenv("EMAIL_TO")
APP_PASSWORD = os.getenv("APP_PASSWORD")

if not EMAIL_FROM or not APP_PASSWORD:
    print("❌ Error: Missing EMAIL_FROM or APP_PASSWORD in .env file.")
    exit(1)

msg = MIMEText("Test email from Polymarket Tracker!")
msg["Subject"] = "🔮 Test Alert"
msg["From"]    = EMAIL_FROM
msg["To"]      = EMAIL_TO

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, APP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
