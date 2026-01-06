from streamlit_autorefresh import st_autorefresh  # pyright: ignore[reportMissingImports]

import streamlit as st  # pyright: ignore[reportMissingImports]
st.title("Stock Volatility Explorer")
st.write("This app allows you to explore the volatility of different stocks.")

# User Guide Section
with st.expander("📖 How to Use This App", expanded=True):
    st.markdown("""
    ### Getting Started
    
    1. **Select Stock Tickers**: Use the sidebar on the left to choose one or more stock tickers from the dropdown menu. 
       - Choose from 20+ popular stocks across various sectors
       - You can select multiple tickers to compare their volatility side-by-side
    
    2. **Enable Auto-Refresh** (Optional): Check the "Enable auto-refresh" box in the sidebar to automatically update the data every 60 seconds. 
       - This is useful for monitoring real-time changes in stock volatility
       - Uncheck it if you prefer manual refreshes
    
    3. **Adjust Start Date** (Optional): Use the date picker in the sidebar to change the historical data range (default: January 1, 2020)
    
    ### Understanding the Results
    
    Once you've selected your tickers, the app will display:
    
    - **Recent Price Data**: A table showing the latest closing prices for your selected stocks
    
    - **Stock Prices Chart**: A line chart displaying the historical closing prices for all selected stocks over time
    
    - **Relative Performance Chart**: Shows how each stock has performed relative to its starting value (normalized to 100), making it easy to compare performance regardless of absolute price differences
    
    - **Annualized Volatility Table**: Displays the calculated volatility metric for each stock, which measures the degree of variation in stock prices over time
    
    - **Volatility Insights**: The app automatically identifies:
      - The stock with the **highest volatility** and provides context about why it might be volatile
      - The stock with the **lowest volatility** and explains factors contributing to its stability
    
    ### Tips
    
    - Select at least one ticker to begin the analysis
    - Compare different sectors (e.g., tech stocks vs. financial stocks) to see how volatility varies
    - Use the relative performance chart to identify which stocks have outperformed others over the selected time period
    - Higher volatility indicates greater price swings, which can mean both higher risk and potential for higher returns
    """)

st.sidebar.header("Controls")

# Option to enable/disable auto-refresh
auto_refresh = st.sidebar.checkbox("Enable auto-refresh (every 60s)", value=True)
if auto_refresh:
    st_autorefresh(interval=60 * 1000, key="refresh")

# Default tickers
default_tickers = ["AAPL", "MSFT", "TSLA", "JPM", "SPY", "NVDA", "AMD", "SBUX", "BABA", "INTC", "HOOD", "AVGO", "IREN", "META", "SHOP", "RKLB", "LLY", "GLD", "AMZN", "PLTR"]

# Multiselect for stock tickers
selected_tickers = st.sidebar.multiselect(
    "Select Stock Tickers",
    options=default_tickers,
    default=[],
    help="Choose one or more stock tickers to analyze"
)

# Check if at least one ticker is selected
if len(selected_tickers) == 0:
    st.warning("⚠️ Please select at least one stock ticker to proceed with the analysis.")
import yfinance as yf  # pyright: ignore[reportMissingImports]
import pandas as pd  # pyright: ignore[reportMissingImports]
from datetime import datetime

@st.cache_data(ttl=60)  # Cache expires after 60 seconds for real-time updates
def load_data(tickers_tuple):
    # Convert tuple back to list for yfinance
    tickers = list(tickers_tuple)
    data = yf.download(tickers, start="2020-01-01", progress=False)["Close"]
    return data

@st.cache_data(ttl=60)
def compute_metrics(prices):
    """Cache expensive computations"""
    normalized = prices / prices.iloc[0] * 100
    returns = prices.pct_change()
    volatility = returns.std() * (252 ** 0.5)
    return normalized, returns, volatility

def get_volatility_insight(ticker, is_highest=True):
    """Generate insights about why a stock has high or low volatility"""
    insights = {
        "AAPL": {
            "high": "Apple's volatility is typically moderate due to its large market cap and diversified product portfolio. Higher volatility may stem from product launch cycles, supply chain disruptions, or broader tech sector sentiment.",
            "low": "Apple maintains relatively stable volatility as a mega-cap tech company with strong brand loyalty, recurring revenue streams, and a massive cash position providing financial stability."
        },
        "MSFT": {
            "high": "Microsoft's volatility can increase due to enterprise contract cycles, cloud computing competition, or regulatory concerns. Recent volatility may reflect shifting market dynamics in the tech sector.",
            "low": "Microsoft demonstrates low volatility thanks to its diversified business model (software, cloud, gaming), strong enterprise relationships, and consistent dividend payments that attract stable investors."
        },
        "TSLA": {
            "high": "Tesla exhibits high volatility driven by CEO sentiment, production numbers, regulatory news, and competitive pressures in the EV market. Retail investor enthusiasm and short-term trading activity also contribute to price swings.",
            "low": "Unlikely for Tesla - this stock is typically highly volatile due to its growth-oriented nature, media attention, and sensitivity to market sentiment."
        },
        "JPM": {
            "high": "JPMorgan's volatility can increase during financial stress, interest rate changes, regulatory changes, or economic uncertainty. Banking stocks are sensitive to credit cycles and monetary policy.",
            "low": "JPMorgan shows lower volatility as a well-established financial institution with diversified revenue streams, strong capital ratios, and operations spanning consumer banking, investment banking, and asset management."
        },
        "SPY": {
            "high": "SPY (S&P 500 ETF) typically has moderate volatility as it represents the broad market. Higher volatility may indicate market-wide stress, economic uncertainty, or significant geopolitical events.",
            "low": "SPY demonstrates lower volatility as a diversified index fund representing 500 large-cap stocks. Diversification naturally reduces volatility compared to individual stocks."
        },
        "NVDA": {
            "high": "NVIDIA's volatility can spike due to AI chip demand cycles, gaming market fluctuations, data center spending trends, and competitive dynamics in the semiconductor industry. The stock is sensitive to tech sector sentiment and product launch cycles.",
            "low": "NVIDIA maintains lower volatility when demand is stable, with strong market position in AI and data center chips, consistent revenue from gaming, and diversified business segments providing stability."
        },
        "AMD": {
            "high": "AMD's volatility increases with competitive pressures from Intel and NVIDIA, product cycle timing, PC market demand fluctuations, and data center adoption rates. The stock is sensitive to semiconductor industry cycles.",
            "low": "AMD shows lower volatility when maintaining strong market share in CPUs and GPUs, with consistent product execution, growing data center presence, and stable demand from enterprise customers."
        },
        "SBUX": {
            "high": "Starbucks volatility can increase due to commodity price fluctuations (coffee beans), consumer spending patterns, international expansion challenges, labor costs, and competitive pressures in the food service industry.",
            "low": "Starbucks demonstrates lower volatility as a well-established brand with loyal customer base, consistent revenue from recurring customers, global diversification, and strong brand recognition providing stability."
        },
        "BABA": {
            "high": "Alibaba's volatility is significantly influenced by regulatory changes in China, geopolitical tensions, economic conditions in China, competitive pressures, and investor sentiment toward Chinese tech stocks.",
            "low": "Alibaba shows lower volatility when regulatory environment is stable, with strong market position in e-commerce and cloud services in China, diversified revenue streams, and consistent operational performance."
        },
        "INTC": {
            "high": "Intel's volatility increases with competitive pressures from AMD and other chip manufacturers, manufacturing challenges, market share losses, capital expenditure concerns, and shifts in PC/data center demand.",
            "low": "Intel maintains lower volatility when executing well on manufacturing transitions, maintaining market leadership, with strong enterprise relationships, and consistent dividend payments attracting stable investors."
        },
        "HOOD": {
            "high": "Robinhood exhibits high volatility driven by retail trading activity, regulatory scrutiny, competition from established brokers, cryptocurrency market conditions, and dependence on transaction-based revenue.",
            "low": "Unlikely for Robinhood - this stock is typically highly volatile due to its business model tied to trading volumes, regulatory uncertainties, and sensitivity to market sentiment and retail investor behavior."
        },
        "AVGO": {
            "high": "Broadcom's volatility can increase with semiconductor industry cycles, acquisition activity, regulatory approvals for deals, customer concentration risks, and competitive dynamics in networking and wireless chips.",
            "low": "Broadcom shows lower volatility as a diversified semiconductor company with strong positions in networking, wireless, and enterprise software, consistent cash generation, and stable customer relationships."
        },
        "IREN": {
            "high": "Iris Energy's volatility is driven by Bitcoin mining profitability, energy costs, regulatory changes affecting crypto mining, Bitcoin price movements, and operational challenges in data center operations.",
            "low": "Iris Energy maintains lower volatility when Bitcoin prices are stable, with efficient mining operations, low energy costs, and consistent hash rate production providing operational stability."
        },
        "META": {
            "high": "Meta's volatility increases with regulatory concerns, privacy policy changes, advertising market fluctuations, competition from TikTok and other platforms, metaverse investment uncertainty, and user engagement trends.",
            "low": "Meta demonstrates lower volatility when maintaining strong advertising revenue, with dominant market position in social media, consistent user growth, and diversified revenue streams from multiple platforms."
        },
        "SHOP": {
            "high": "Shopify's volatility spikes with e-commerce growth trends, competitive pressures from Amazon and other platforms, merchant churn, economic conditions affecting small businesses, and shifts in consumer spending.",
            "low": "Shopify shows lower volatility when e-commerce growth is steady, with strong merchant retention, expanding product offerings, international growth, and consistent subscription revenue providing stability."
        },
        "RKLB": {
            "high": "Rocket Lab exhibits high volatility typical of space industry stocks, driven by launch success rates, contract wins, competitive pressures, regulatory approvals, and investor sentiment toward space commercialization.",
            "low": "Rocket Lab maintains lower volatility when achieving consistent launch success, securing long-term contracts, demonstrating operational reliability, and showing clear path to profitability."
        },
        "LLY": {
            "high": "Eli Lilly's volatility can increase with drug trial results, FDA approval decisions, patent expirations, competitive drug launches, pricing pressures, and regulatory changes in the pharmaceutical industry.",
            "low": "Eli Lilly demonstrates lower volatility as an established pharmaceutical company with diversified drug portfolio, strong pipeline, consistent revenue from blockbuster drugs, and stable dividend payments."
        },
        "GLD": {
            "high": "GLD (Gold ETF) volatility increases with inflation expectations, currency movements, geopolitical tensions, central bank policies, and shifts in investor risk sentiment driving demand for safe-haven assets.",
            "low": "GLD shows lower volatility when economic conditions are stable, with gold serving as a store of value, low correlation to equities, and consistent demand from central banks and investors providing stability."
        },
        "AMZN": {
            "high": "Amazon's volatility can spike with e-commerce growth trends, AWS competitive dynamics, regulatory scrutiny, labor costs, international expansion challenges, and shifts in consumer spending patterns.",
            "low": "Amazon maintains lower volatility as a diversified tech giant with dominant positions in e-commerce and cloud computing, consistent revenue growth, and multiple revenue streams providing stability."
        },
        "PLTR": {
            "high": "Palantir exhibits high volatility driven by government contract wins/losses, enterprise sales cycles, competitive pressures, stock-based compensation concerns, and investor sentiment toward data analytics companies.",
            "low": "Palantir shows lower volatility when securing long-term government contracts, demonstrating consistent revenue growth, expanding commercial customer base, and showing clear path to profitability."
        }
    }
    
    key = "high" if is_highest else "low"
    return insights.get(ticker, {}).get(key, f"{ticker} volatility is influenced by market conditions, sector dynamics, and company-specific factors.")

if len(selected_tickers) > 0:
    # Load and cache data
    prices = load_data(tuple(sorted(selected_tickers)))  # Sort for consistent cache key
    
    # Compute metrics with caching
    normalized, returns, volatility = compute_metrics(prices)
    
    # Display last update time
    st.caption(f"🔄 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.write(prices.tail())

    st.subheader("Stock Prices")
    st.line_chart(prices)

    st.subheader("Relative Performance (Base = 100)")
    st.line_chart(normalized)

    st.subheader("Annualized Volatility")
    st.dataframe(volatility.rename("Volatility"))

    start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2020-01-01"))

    best = normalized.iloc[-1].idxmax()
    st.success(f"📈 Highest volatility: {best}")

    worst = normalized.iloc[-1].idxmin()
    st.error(f"📉 Lowest volatility: {worst}")
    
    # Find highest and lowest volatility stocks
    highest_vol_ticker = volatility.idxmax()
    lowest_vol_ticker = volatility.idxmin()
    
    st.success(f"📈 Highest volatility: {highest_vol_ticker} ({volatility[highest_vol_ticker]:.2%})")
    st.info(f"💡 **Insight:** {get_volatility_insight(highest_vol_ticker, is_highest=True)}")

    st.error(f"📉 Lowest volatility: {lowest_vol_ticker} ({volatility[lowest_vol_ticker]:.2%})")
    st.info(f"💡 **Insight:** {get_volatility_insight(lowest_vol_ticker, is_highest=False)}")
