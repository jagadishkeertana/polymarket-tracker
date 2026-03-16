import requests
import json
from rich.table import Table
from rich.console import Console

BASE_GAMMA = "https://gamma-api.polymarket.com"
console = Console()

response = requests.get(f"{BASE_GAMMA}/markets", params={
    "active": "true",
    "closed": "false",
    "limit": 10,
    "order": "volume24hr",
    "ascending": "false"
})

markets = response.json()

table = Table(title="🔮 Trending Prediction Markets")
table.add_column("#", style="dim", width=3)
table.add_column("Question", style="cyan", max_width=45)
table.add_column("24hr Volume", style="green", justify="right")
table.add_column("Yes %", style="magenta", justify="right")
table.add_column("No %", style="red", justify="right")
table.add_column("Category", style="yellow")

for i, m in enumerate(markets):
    prices = json.loads(m.get("outcomePrices", '["0", "0"]'))
    yes_pct = f"{float(prices[0]) * 100:.1f}%"
    no_pct  = f"{float(prices[1]) * 100:.1f}%"
    volume  = f"${float(m.get('volume24hr', 0)):,.0f}"
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