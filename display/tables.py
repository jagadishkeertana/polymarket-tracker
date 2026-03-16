import json
from rich.table import Table
from rich.console import Console

console = Console()

def show_markets_table(markets, title="🔮 Prediction Markets"):
    """Display a list of markets as a rich table."""
    table = Table(title=title)
    table.add_column("#",            style="dim",     width=3)
    table.add_column("Question",     style="cyan",    max_width=45)
    table.add_column("24hr Volume",  style="green",   justify="right")
    table.add_column("Yes %",        style="magenta", justify="right")
    table.add_column("No %",         style="red",     justify="right")
    table.add_column("Category",     style="yellow")

    for i, m in enumerate(markets):
        prices   = json.loads(m.get("outcomePrices", '["0","0"]'))
        yes_pct  = f"{float(prices[0]) * 100:.1f}%"
        no_pct   = f"{float(prices[1]) * 100:.1f}%"
        volume   = f"${float(m.get('volume24hr', 0)):,.0f}"
        category = m.get("category") or "General"

        table.add_row(
            str(i + 1),
            m.get("question", "N/A"),
            volume,
            yes_pct,
            no_pct,
            category
        )

    console.print(table)


def show_order_book(order_book):
    """Display bids and asks from an order book."""
    table = Table(title="📖 Order Book")
    table.add_column("Side", style="cyan")
    table.add_column("Price", style="green", justify="right")
    table.add_column("Size",  style="yellow", justify="right")

    for bid in order_book.get("bids", [])[:5]:
        table.add_row("BID 🟢", bid.get("price"), bid.get("size"))

    for ask in order_book.get("asks", [])[:5]:
        table.add_row("ASK 🔴", ask.get("price"), ask.get("size"))

    console.print(table)