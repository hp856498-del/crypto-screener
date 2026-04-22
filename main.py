import streamlit as st
from data import get_symbols, get_ohlcv
from scanner import detect_patterns

st.set_page_config(page_title="Crypto Screener", layout="wide")

st.title("🚀 Crypto Screener")

# ================= SIDEBAR =================

st.sidebar.header("⚙️ Settings")

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["15m", "30m", "1h", "3h", "4h", "1d"]
)

patterns = st.sidebar.multiselect(
    "Select Patterns",
    ["Inside Bar", "Bullish Harami", "Bearish Harami", "Bullish Engulfing", "Bearish Engulfing"],
    default=["Inside Bar"]
)

coin_limit = st.sidebar.selectbox(
    "Number of Coins",
    [50, 100, 200, 300],
    index=2
)

enable_backscan = st.sidebar.checkbox("Scan Previous Candles")

backscan_range = st.sidebar.selectbox(
    "Backscan Range",
    [5, 10, 15],
    index=1
)

start = st.sidebar.button("🚀 Start Scanning")

# ================= MAIN =================

if start:
    st.info("Scanning market... please wait ⏳")

    symbols = get_symbols(coin_limit)

    results = []

    progress = st.progress(0)

    for i, symbol in enumerate(symbols):
        df = get_ohlcv(symbol, timeframe)

        if df is None or len(df) < 10:
            continue

        matches = detect_patterns(
            df,
            selected_patterns=patterns,
            backscan=enable_backscan,
            backscan_range=backscan_range
        )

        for m in matches:
            results.append({
                "Symbol": symbol,
                "Pattern": m["pattern"],
                "Signal": m["signal"],
                "Time": m["time"]
            })

        progress.progress((i + 1) / len(symbols))

    st.success(f"{len(results)} patterns found")

    if results:
        st.dataframe(results)
    else:
        st.warning("No patterns found")