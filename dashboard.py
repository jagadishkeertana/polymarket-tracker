import streamlit as st
import plotly.express as px
import pandas as pd
import json
from client.api import get_trending_markets, get_markets_by_category

st.set_page_config(
    page_title="Polymarket Tracker",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Polymarket Tracker")
st.caption("Live prediction market data from Polymarket")

# Sidebar controls
st.sidebar.header("⚙️ Filters")
category = st.sidebar.selectbox("Category", [
    "Trending", "politics", "crypto", "sports", "science"
])
limit = st.sidebar.slider("Number of markets", 5, 20, 10)
st.sidebar.button("🔄 Refresh Data")

# Fetch data
@st.cache_data(ttl=60)
def fetch_markets(category, limit):
    if category == "Trending":
        return get_trending_markets(limit=limit)
    return get_markets_by_category(category=category, limit=limit)

markets = fetch_markets(category, limit)

# Parse into dataframe
rows = []
for m in markets:
    prices = json.loads(m.get("outcomePrices", '["0","0"]'))

    yes_raw = float(prices[0])
    no_raw  = float(prices[1])
    yes_pct = round(yes_raw if yes_raw > 1 else yes_raw * 100, 1)
    no_pct  = round(no_raw  if no_raw  > 1 else no_raw  * 100, 1)

    rows.append({
        "Question":        m.get("question", "N/A"),
        "Yes %":           yes_pct,
        "No %":            no_pct,
        "24hr Volume ($)": round(float(m.get("volume24hr", 0)), 2),
        "Total Volume ($)":round(float(m.get("volume", 0)), 2),
        "Ends":            m.get("endDate", "N/A")[:10],
        "Category":        m.get("category") or "General"
    })

df = pd.DataFrame(rows)

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("📊 Markets Shown",       len(df))
col2.metric("💰 Total 24hr Volume",   f"${df['24hr Volume ($)'].sum():,.0f}")
col3.metric("🔥 Top Market Volume",   f"${df['24hr Volume ($)'].max():,.0f}")

st.divider()

# Bar chart
st.subheader("📈 Top Markets by 24hr Volume")
fig = px.bar(
    df.head(10),
    x="24hr Volume ($)",
    y="Question",
    orientation="h",
    color="Yes %",
    color_continuous_scale="RdYlGn",
    range_color=[0, 100],
    title="24hr Trading Volume"
)
fig.update_layout(yaxis=dict(autorange="reversed"), height=500)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Full table
st.subheader("📋 Market Details")
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "Yes %": st.column_config.ProgressColumn(
            "Yes %", min_value=0, max_value=100, format="%.1f%%"
        ),
        "No %": st.column_config.ProgressColumn(
            "No %", min_value=0, max_value=100, format="%.1f%%"
        ),
        "24hr Volume ($)": st.column_config.NumberColumn(
            "24hr Volume ($)", format="$%.2f"
        ),
    }
)