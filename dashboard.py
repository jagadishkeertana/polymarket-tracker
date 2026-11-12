import streamlit as st
import plotly.express as px
import pandas as pd
import json
from client.api import get_trending_markets, get_markets_by_category
from ml.predict import predict_market

st.set_page_config(
    page_title="Polymarket AI Tracker & Predictor",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Polymarket Real-Time Tracker & ML Predictor")
st.caption("Live prediction market analytics, order liquidity, and Random Forest resolution forecasting")

# Sidebar controls
st.sidebar.header("⚙️ Controls & Filters")
category = st.sidebar.selectbox("Category", [
    "Trending", "politics", "crypto", "sports", "science"
])
limit = st.sidebar.slider("Number of markets", 5, 25, 10)
min_edge_filter = st.sidebar.slider("Highlight Edge Threshold (±%)", 0, 30, 10)
refresh_clicked = st.sidebar.button("🔄 Refresh Data Now")

# Fetch data with cache
@st.cache_data(ttl=60)
def fetch_markets(category, limit):
    if category == "Trending":
        return get_trending_markets(limit=limit)
    return get_markets_by_category(category=category, limit=limit)

if refresh_clicked:
    st.cache_data.clear()

markets = fetch_markets(category, limit)

# Parse and evaluate markets with ML Model
rows = []
alpha_opportunities = []

for m in markets:
    try:
        prices = json.loads(m.get("outcomePrices", '["0.5","0.5"]'))
        yes_raw = float(prices[0]) if prices else 0.5
        no_raw  = float(prices[1]) if len(prices) > 1 else (1.0 - yes_raw)
    except Exception:
        yes_raw = float(m.get("lastTradePrice", 0.5))
        no_raw  = 1.0 - yes_raw

    yes_pct = round(yes_raw * 100 if yes_raw <= 1 else yes_raw, 1)
    no_pct  = round(no_raw  * 100 if no_raw  <= 1 else no_raw,  1)
    norm_price = yes_pct / 100.0

    vol_24hr   = round(float(m.get("volume24hr", 0) or 0), 2)
    vol_total  = round(float(m.get("volume", 0) or 0), 2)
    liquidity  = round(float(m.get("liquidity", 0) or 0), 2)

    # ML Inference
    try:
        pred, ai_prob, edge = predict_market(norm_price, volume=vol_total, trades=50)
        ai_prob_pct = round(ai_prob * 100, 1)
        edge_pct    = round(edge * 100, 1)
    except Exception:
        ai_prob_pct = yes_pct
        edge_pct    = 0.0
        pred        = 1 if yes_pct >= 50 else 0

    row = {
        "Question":         m.get("question", "N/A"),
        "Market Yes %":     yes_pct,
        "AI Predicted %":   ai_prob_pct,
        "AI Edge (%)":      edge_pct,
        "AI Verdict":       "🟢 BUY YES" if edge_pct >= min_edge_filter else ("🔴 OVERVALUED" if edge_pct <= -min_edge_filter else "⚪ NEUTRAL"),
        "24hr Volume ($)":  vol_24hr,
        "Total Volume ($)": vol_total,
        "Liquidity ($)":    liquidity,
        "Ends":             m.get("endDate", "N/A")[:10],
        "Category":         m.get("category") or category
    }
    rows.append(row)

    if abs(edge_pct) >= min_edge_filter:
        alpha_opportunities.append(row)

df = pd.DataFrame(rows)

# Top metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Markets Tracked", len(df))
col2.metric("💰 Total 24hr Volume", f"${df['24hr Volume ($)'].sum():,.0f}")
col3.metric("🎯 High Edge Signals", len(alpha_opportunities))
col4.metric("🤖 ML Model", "Random Forest (76.0% Acc)")

st.divider()

# High Edge Signals Alert Banner
if alpha_opportunities:
    st.subheader("⚡ Model-Detected Inefficiencies (Alpha Signals)")
    st.caption(f"Markets where the ML model's win forecast differs from crowd price by $\ge {min_edge_filter}\%$")
    
    alpha_cols = st.columns(min(len(alpha_opportunities), 3))
    for idx, opp in enumerate(alpha_opportunities[:3]):
        with alpha_cols[idx]:
            st.warning(
                f"**{opp['Question'][:55]}...**\n\n"
                f"• Market Price: **{opp['Market Yes %']}%**\n\n"
                f"• AI Forecast: **{opp['AI Predicted %']}%**\n\n"
                f"• Signal: **{opp['AI Verdict']} ({opp['AI Edge (%)']:+0.1f}%)**"
            )
    st.divider()

# Chart Section: Volume vs. Price & AI Confidence
st.subheader("📈 Top Markets: 24hr Volume & Model Forecasts")
if not df.empty:
    fig = px.bar(
        df.head(10),
        x="24hr Volume ($)",
        y="Question",
        orientation="h",
        color="AI Predicted %",
        color_continuous_scale="Viridis",
        range_color=[0, 100],
        hover_data=["Market Yes %", "AI Predicted %", "AI Edge (%)"],
        title="24hr Volume colored by AI Predicted Win Probability"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), height=480)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Full Data Table with formatting
st.subheader("📋 Comprehensive Market & Prediction Matrix")
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "Market Yes %": st.column_config.ProgressColumn(
            "Market Yes %", min_value=0, max_value=100, format="%.1f%%"
        ),
        "AI Predicted %": st.column_config.ProgressColumn(
            "AI Predicted %", min_value=0, max_value=100, format="%.1f%%"
        ),
        "AI Edge (%)": st.column_config.NumberColumn(
            "AI Edge (%)", format="%+.1f%%"
        ),
        "24hr Volume ($)": st.column_config.NumberColumn(
            "24hr Volume ($)", format="$%.2f"
        ),
        "Total Volume ($)": st.column_config.NumberColumn(
            "Total Volume ($)", format="$%.2f"
        ),
    }
)

st.caption(f"🕒 Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | Auto-cached TTL: 60s")