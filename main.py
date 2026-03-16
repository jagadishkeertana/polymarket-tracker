from client.api import get_trending_markets, get_markets_by_category
from display.tables import show_markets_table
from saver.export import save_to_json, save_to_csv
from rich.console import Console

console = Console()

def main():
    console.print("\n[bold cyan]🔮 Polymarket Tracker[/bold cyan]\n")

    # Trending markets
    console.print("[bold]📈 Trending Markets (Top 10 by 24hr Volume)[/bold]")
    trending = get_trending_markets(limit=10)
    show_markets_table(trending, title="Trending Markets")

    json_path = save_to_json(trending, "trending_markets.json")
    csv_path  = save_to_csv(trending,  "trending_markets.csv")
    console.print(f"\n[green]✅ Saved JSON → {json_path}[/green]")
    console.print(f"[green]✅ Saved CSV  → {csv_path}[/green]")

    # Politics markets
    console.print("\n[bold]🗳️  Politics Markets[/bold]")
    politics = get_markets_by_category(category="politics", limit=5)
    show_markets_table(politics, title="Politics Markets")

    pol_path = save_to_csv(politics, "politics_markets.csv")
    console.print(f"\n[green]✅ Saved CSV  → {pol_path}[/green]")

if __name__ == "__main__":
    main()