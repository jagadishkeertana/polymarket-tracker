import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(to_email, subject, body, from_email, app_password):
    """Send an email alert using Gmail."""
    msg = MIMEMultipart()
    msg["From"]    = from_email
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
    print(f"✅ Alert sent to {to_email}")

def check_and_alert(markets, threshold=20, to_email=None,
                    from_email=None, app_password=None):
    """Check if any market has moved sharply and send alert."""
    alerts = []
    for m in markets:
        change = abs(float(m.get("oneDayPriceChange", 0))) * 100
        if change >= threshold:
            alerts.append({
                "question": m.get("question"),
                "change":   round(change, 1),
                "volume":   m.get("volume24hr", 0)
            })

    if alerts and to_email:
        rows = "".join([
            f"<tr><td>{a['question']}</td>"
            f"<td style='color:red'>{a['change']}% move</td>"
            f"<td>${float(a['volume']):,.0f}</td></tr>"
            for a in alerts
        ])
        body = f"""
        <h2>🔮 Polymarket Alert — Sharp Market Moves</h2>
        <table border='1' cellpadding='8'>
            <tr><th>Market</th><th>Price Change</th><th>24hr Volume</th></tr>
            {rows}
        </table>
        """
        send_alert(to_email, "🔮 Polymarket Sharp Move Alert", body,
                   from_email, app_password)
    return alerts