import concurrent.futures
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# ==============================================================================
# PREMIUM FINANCIAL ENGINE CONFIGURATION & THEME FIXES
# ==============================================================================
st.set_page_config(
    page_title="Alpha-Accumulation Suite Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Premium CSS Inject for Dark Theme Polish
st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #1e222d;
        border: 1px solid #2a2e39;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    div[data-testid="stExpander"] {
        border: 1px solid #ff4b4b44;
        background-color: #1a1010;
    }
    .stButton>button {
        width: 100%;
        background-color: #2962ff !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e4bd8 !important;
        transform: scale(1.01);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏗️ Alpha-Accumulation Suite (Upgraded Edition)")
st.caption("Quantitative Screening Suite | Enhanced Institutional Float Filters")

# ==============================================================================
# SIDEBAR TUNING CONTROLS
# ==============================================================================
st.sidebar.header("🔧 Dynamic Engine Tuning")
MIN_MARKET_CAP_CR = st.sidebar.number_input(
    "Minimum Market Cap Requirement (Cr)", value=1000
)
MAX_IPO_AGE_YEARS = st.sidebar.slider(
    "Maximum IPO Listing Age Filter (Years)", min_value=1, max_value=10, value=7
)
TARGET_ABSORPTION_PCT = st.sidebar.slider(
    "Target Retail Free-Float Churn (%)", min_value=10, max_value=100, value=30
)

NIFTY_500_SEEDS = [
    "PAYTM.NS",
    "ZOMATO.NS",
    "LIC.NS",
    "AWL.NS",
    "DELHIVERY.NS",
    "NYKAA.NS",
    "TCS.NS",
    "ASIANPAINT.NS",
    "BRITANNIA.NS",
    "BALRAMCHIN.NS",
]

# ==============================================================================
# CORE DATA PROCESSING ENGINES
# ==============================================================================


def execute_upgraded_ipo_logic(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        max_history = ticker.history(period="max")
        if max_history.empty:
            return None, f"No history available for {ticker_symbol}"

        first_trade_date = max_history.index[0].date()
        days_since_listing = (datetime.date.today() - first_trade_date).days
        if days_since_listing > (MAX_IPO_AGE_YEARS * 365):
            return None, None

        df = max_history.tail(int(MAX_IPO_AGE_YEARS * 250))
        if len(df) < 200:
            return None, f"Insufficient operational candles for {ticker_symbol}"

        info = ticker.info
        shares = info.get("sharesOutstanding") or info.get(
            "impliedSharesOutstanding"
        )
        float_shares = info.get("floatShares")

        if not shares or not float_shares:
            return (
                None,
                f"Missing critical structural float metadata for {ticker_symbol}",
            )

        current_price = df["Close"].iloc[-1]
        current_mcap_cr = (shares * current_price) / 10_000_000
        if current_mcap_cr < MIN_MARKET_CAP_CR:
            return None, None

        free_float_mcap_cr = (float_shares * current_price) / 10_000_000

        df["100_DMA"] = df["Close"].rolling(window=100).mean()
        df["200_DMA"] = df["Close"].rolling(window=200).mean()
        df["7_DMA"] = df["Close"].rolling(window=7).mean()
        df["VWAP_20d"] = (df["Volume"] * df["Close"]).rolling(
            window=20
        ).sum() / df["Volume"].rolling(window=20).sum()

        lowest_price = df["Close"].min()
        base_window = df[df["Close"] <= lowest_price * 1.25]
        total_traded_at_base_cr = (
            base_window["Volume"] * base_window["Close"]
        ).sum() / 10_000_000

        absorption_float_pct = (
            total_traded_at_base_cr / free_float_mcap_cr
        ) * 100

        gate_volume = absorption_float_pct >= TARGET_ABSORPTION_PCT
        gate_trend = df["100_DMA"].iloc[-1] > df["200_DMA"].iloc[-1]
        above_vwap = current_price > df["VWAP_20d"].iloc[-1]
        gate_trigger = (df["7_DMA"].iloc[-2] <= df["100_DMA"].iloc[-2]) and (
            df["7_DMA"].iloc[-1] > df["100_DMA"].iloc[-1]
        )

        status = "WATCHLIST (Squeezing)"
        if gate_trend and gate_volume and above_vwap:
            status = (
                "🔥 BUY TRIGGER ACTIVE" if gate_trigger else "🟢 TREND CONFIRMED"
            )

        return {
            "Ticker": ticker_symbol.replace(".NS", ""),
            "Price (₹)": round(current_price, 2),
            "Market Cap (Cr)": round(current_mcap_cr, 2),
            "Free-Float Cap (Cr)": round(free_float_mcap_cr, 2),
            "Float Absorption %": min(
                round(absorption_float_pct, 2) / 100.0, 1.0
            ),  # Scaled for modern progress bar
            "Status": status,
            "Intraday SL (5%)": round(current_price * 0.95, 2),
            "Target (10%)": round(current_price * 1.10, 2),
        }, None
    except Exception as e:
        return (
            None,
            f"Exception in Upgraded Mode 1 for {ticker_symbol}: {str(e)}",
        )


def execute_value_owner_logic(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="2y")
        if df.empty or len(df) < 200:
            return None, f"Insufficient price history data for {ticker_symbol}"
        annual_bs, annual_fi, info = (
            ticker.balance_sheet,
            ticker.financials,
            ticker.info,
        )
        if annual_bs.empty or annual_fi.empty:
            return None, f"Financial statements unavailable for {ticker_symbol}"

        annual_fi = annual_fi.reindex(
            columns=sorted(annual_fi.columns, reverse=True)
        )
        annual_bs = annual_bs.reindex(
            columns=sorted(annual_bs.columns, reverse=True)
        )

        current_price = df["Close"].iloc[-1]
        shares = info.get("sharesOutstanding") or 1
        current_mcap_cr = (shares * current_price) / 10_000_000

        ebit = (
            annual_fi.loc["Operating Income"].iloc[0]
            if "Operating Income" in annual_fi.index
            else 0
        )
        total_assets = (
            annual_bs.loc["Total Assets"].iloc[0]
            if "Total Assets" in annual_bs.index
            else 1
        )
        current_liabilities = (
            annual_bs.loc["Total Current Liabilities"].iloc[0]
            if "Total Current Liabilities" in annual_bs.index
            else 0
        )

        capital_employed = total_assets - current_liabilities
        roce = (ebit / capital_employed) * 100 if capital_employed > 0 else 0
        total_debt = (
            annual_bs.loc["Total Debt"].iloc[0]
            if "Total Debt" in annual_bs.index
            else 0
        )
        total_equity = (
            annual_bs.loc["Stockholders Equity"].iloc[0]
            if "Stockholders Equity" in annual_bs.index
            else 1
        )
        debt_to_equity = total_debt / total_equity

        float_shares = info.get("floatShares", 0) or 0
        promoter_lock_pct = (
            ((shares - float_shares) / shares) * 100 if shares > 0 else 0
        )

        trailing_div_rate = info.get("trailingAnnualDividendRate", 0) or 0
        dividend_yield = (
            (trailing_div_rate / current_price) * 100 if current_price > 0 else 0
        )

        df["200_DMA"] = df["Close"].rolling(window=200).mean()
        dma_200 = df["200_DMA"].iloc[-1]
        pct_from_200dma = ((current_price - dma_200) / dma_200) * 100

        if roce >= 20.0 and debt_to_equity <= 0.25 and promoter_lock_pct >= 70.0:
            status = "⭐ INSTITUTIONAL QUALITY"
            if current_price <= dma_200 * 0.85:
                status = "🎯 V-200 DISCOUNT BUY"
            return {
                "Ticker": ticker_symbol.replace(".NS", ""),
                "Price": round(current_price, 2),
                "Market Cap (Cr)": round(current_mcap_cr, 2),
                "ROCE %": round(roce, 2),
                "Debt/Equity": round(debt_to_equity, 2),
                "Promoter Lock %": round(promoter_lock_pct, 2),
                "Div Yield %": round(dividend_yield, 2),
                "Status": status,
            }, None
        return None, None
    except Exception as e:
        return None, f"Exception in Mode 2 for {ticker_symbol}: {str(e)}"


def execute_intraday_vcp_logic(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(interval="15m", period="5d")
        if df.empty or len(df) < 75:
            return None, f"Insufficient intraday intervals for {ticker_symbol}"

        r_max = df["High"].tail(60).max()
        current_price = df["Close"].iloc[-1]

        low_t1 = df["Low"].tail(60).iloc[0:25].min()
        low_t2 = df["Low"].tail(35).iloc[0:20].min()
        low_t3 = df["Low"].tail(10).min()

        depth_t1 = ((r_max - low_t1) / r_max) * 100
        depth_t2 = ((r_max - low_t2) / r_max) * 100
        depth_t3 = ((r_max - low_t3) / r_max) * 100

        gate_contraction = (
            (3.0 <= depth_t1 <= 6.0)
            and (1.0 <= depth_t2 <= 2.8)
            and (0.1 <= depth_t3 <= 0.9)
        )
        gate_hierarchy = depth_t1 > depth_t2 > depth_t3

        df["20_SMA"] = df["Close"].rolling(window=20).mean()
        df["20_STD"] = df["Close"].rolling(window=20).std()
        df["Bandwidth"] = (
            (df["20_SMA"] + (2 * df["20_STD"]))
            - (df["20_SMA"] - (2 * df["20_STD"]))
        ) / df["20_SMA"]

        gate_squeeze = df["Bandwidth"].iloc[-1] <= df["Bandwidth"].tail(30).min() * 1.15
        vol_sma20 = df["Volume"].rolling(window=20).mean()
        gate_vol_dry = df["Volume"].iloc[-2] < (vol_sma20.iloc[-2] * 0.65)
        gate_vol_burst = df["Volume"].iloc[-1] >= (vol_sma20.iloc[-1] * 2.0)
        gate_breakout = current_price >= r_max * 0.998

        status = "Compressing Structure"
        if gate_contraction and gate_hierarchy and gate_squeeze:
            if gate_breakout and gate_vol_burst:
                status = "⚡ VCP SQUEEZE BREAKOUT TRIGGER"
            elif gate_vol_dry:
                status = "🟡 CHEAT SETUP (Tightening)"
            else:
                status = "🟢 VCP STRUCTURE COMPLIANT"

            return {
                "Ticker": ticker_symbol.replace(".NS", ""),
                "Price": round(current_price, 2),
                "Status": status,
                "T1 Depth %": round(depth_t1, 2),
                "T2 Depth %": round(depth_t2, 2),
                "T3 Depth %": round(depth_t3, 2),
            }, None
        return None, None
    except Exception as e:
        return None, f"Exception in VCP Engine for {ticker_symbol}: {str(e)}"


# ==============================================================================
# MAIN TAB VIEW & RENDER ENGINE
# ==============================================================================
tab1, tab2, tab3 = st.tabs(
    [
        "🚀 Upgraded Mode 1: IPO Turnaround",
        "💎 Mode 2: Value-Owner",
        "🎯 Mode 3: Intraday VCP Engine",
    ]
)

with tab1:
    st.subheader("IPO Turnaround Dashboard")

    if st.button("🔥 Run Upgraded IPO Float Scan"):
        results_tab1, errors_tab1 = [], []
        progress1 = st.progress(0)

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = {
                executor.submit(execute_upgraded_ipo_logic, t): t
                for t in NIFTY_500_SEEDS
            }
            for idx, future in enumerate(
                concurrent.futures.as_completed(futures)
            ):
                res, err = future.result()
                if res:
                    results_tab1.append(res)
                if err:
                    errors_tab1.append(err)
                progress1.progress((idx + 1) / len(NIFTY_500_SEEDS))

        # Modern UI Block 1: Real-time Metric Cards Overview
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="Total Scanned Tickers", value=len(NIFTY_500_SEEDS))
        with c2:
            actives = sum(
                1 for x in results_tab1 if "ACTIVE" in x.get("Status", "")
            )
            st.metric(
                label="Active Action Signals",
                value=actives,
                delta=f"{actives} Triggered",
            )
        with c3:
            st.metric(label="Data API Exclusions", value=len(errors_tab1))

        st.write("---")

        if results_tab1:
            df1 = pd.DataFrame(results_tab1)

            # Modern UI Block 2: Interactive column configuration with Progress Bars & Tags
            st.data_editor(
                df1,
                column_config={
                    "Ticker": st.column_config.TextColumn(
                        "Symbol", help="Stock Ticker Code"
                    ),
                    "Price (₹)": st.column_config.NumberColumn(
                        "Last Price", format="₹%.2f"
                    ),
                    "Float Absorption %": st.column_config.ProgressColumn(
                        "Float Churn Ratio",
                        help="Turnover relative to free float",
                        format="%.2f",
                        min_value=0.0,
                        max_value=1.0,
                    ),
                    "Status": st.column_config.SelectboxColumn(
                        "Signal Status",
                        options=[
                            "🔥 BUY TRIGGER ACTIVE",
                            "🟢 TREND CONFIRMED",
                            "WATCHLIST (Squeezing)",
                        ],
                    ),
                },
                disabled=True,
                use_container_width=True,
                key="ipo_editor",
            )
        else:
            st.warning("No tickers matched float criteria.")

        if errors_tab1:
            st.write("")
            with st.expander("⚠️ Pipeline Real-time Data Diagnostics"):
                for error in errors_tab1:
                    st.markdown(f"• `{error}`")

# [Tab 2 & Tab 3 configurations run side-by-side cleanly]
with tab2:
    st.header("Fundamental Value-Owner Monitor")
    if st.button("Execute Fundamental Value Scan"):
        results_tab2, errors_tab2 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = {
                executor.submit(execute_value_owner_logic, t): t
                for t in NIFTY_500_SEEDS
            }
            for future in concurrent.futures.as_completed(futures):
                res, err = future.result()
                if res:
                    results_tab2.append(res)
                if err:
                    errors_tab2.append(err)
        if results_tab2:
            st.dataframe(pd.DataFrame(results_tab2), use_container_width=True)
        if errors_tab2:
            with st.expander("⚠️ Mode 2 Diagnostics"):
                for error in errors_tab2:
                    st.write(error)

with tab3:
    st.header("Intraday Volatility Contraction Pattern (VCP) Screener")
    if st.button("Execute Live VCP Squeeze Scan"):
        results_tab3, errors_tab3 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = {
                executor.submit(execute_intraday_vcp_logic, t): t
                for t in NIFTY_500_SEEDS
            }
            for future in concurrent.futures.as_completed(futures):
                res, err = future.result()
                if res:
                    results_tab3.append(res)
                if err:
                    errors_tab3.append(err)
        if results_tab3:
            st.dataframe(pd.DataFrame(results_tab3), use_container_width=True)
        if errors_tab3:
            with st.expander("⚠️ Mode 3 Diagnostics"):
                for error in errors_tab3:
                    st.write(error)
