from client.api import get_trending_markets, get_markets_by_category
from display.tables import show_markets_table
from saver.export import save_to_json, save_to_csv
from alerts.email_alert import check_and_alert, send_alert
from saver.dataset_collector import save_market_data
from rich.console import Console

console = Console()

import os
from dotenv import load_dotenv

load_dotenv()

# ── Email alert settings (loaded from .env) ───────────────────────
EMAIL_FROM      = os.getenv("EMAIL_FROM")
EMAIL_TO        = os.getenv("EMAIL_TO")
APP_PASSWORD    = os.getenv("APP_PASSWORD")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", 20))
# ─────────────────────────────────────────────────────────────────


def main():
    console.print("\n[bold cyan]🔮 Polymarket Tracker[/bold cyan]\n")

    # ── Trending markets ──────────────────────────────────────────
    console.print("[bold]📈 Fetching Trending Markets...[/bold]")
    trending = get_trending_markets(limit=10)

    # ✅ SAVE LIVE DATASET (AI/ML)
    for market in trending:
        try:
            save_market_data({
                "price": market.get("price", 0),
                "volume": market.get("volume", 0),
                "trades": market.get("trades", 0)
            })
        except Exception as e:
            console.print(f"[red]Dataset save error:[/red] {e}")

    show_markets_table(trending, title="Trending Markets")

    # Save to files
    json_path = save_to_json(trending, "trending_markets.json")
    csv_path  = save_to_csv(trending,  "trending_markets.csv")
    console.print(f"\n[green]✅ Saved JSON → {json_path}[/green]")
    console.print(f"[green]✅ Saved CSV  → {csv_path}[/green]")

    # ── Politics markets ──────────────────────────────────────────
    console.print("\n[bold]🗳️  Fetching Politics Markets...[/bold]")
    politics = get_markets_by_category(category="politics", limit=5)

    # ✅ SAVE LIVE DATASET (AI/ML)
    for market in politics:
        try:
            save_market_data({
                "price": market.get("price", 0),
                "volume": market.get("volume", 0),
                "trades": market.get("trades", 0)
            })
        except Exception as e:
            console.print(f"[red]Dataset save error:[/red] {e}")

    show_markets_table(politics, title="Politics Markets")

    pol_path = save_to_csv(politics, "politics_markets.csv")
    console.print(f"\n[green]✅ Saved CSV  → {pol_path}[/green]")

    # ── Email alerts ──────────────────────────────────────────────
    console.print("\n[bold]🚨 Checking for sharp market moves...[/bold]")

    triggered = check_and_alert(
        markets       = trending,
        threshold     = ALERT_THRESHOLD,
        to_email      = EMAIL_TO,
        from_email    = EMAIL_FROM,
        app_password  = APP_PASSWORD
    )

    if triggered:
        console.print(f"[red]⚠️  {len(triggered)} sharp move(s) detected![/red]")
        for alert in triggered:
            console.print(
                f"[red]   → {alert['question']} "
                f"moved {alert['change']}%[/red]"
            )
        console.print("[green]✅ Email alert sent![/green]")
    else:
        console.print("[green]✅ No sharp moves detected — no alert sent[/green]")


if __name__ == "__main__":
    main()