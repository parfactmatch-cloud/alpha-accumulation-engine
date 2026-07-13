import concurrent.futures
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# ==============================================================================
# 00. ADVANCED INSTITUTIONAL THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="Alpha-Accumulation Quant Terminal",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Bloomberg Dark Theme Realignment */
    .stApp { background-color: #0d1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 8px;
    }
    div[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .quant-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .definition-header {
        color: #58a6ff;
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Alpha-Accumulation Quantitative Suite")
st.caption("Institutional-Grade Matrix Screening Terminal | Live Execution Frame")

# ==============================================================================
# 01. QUANT DEFINITIONS & TUNING (SIDEBAR INTEGRATION)
# ==============================================================================
st.sidebar.title("🛠️ Terminal Core Tuning")

with st.sidebar.expander("📖 Mode 1 Matrix Definitions", expanded=True):
    st.markdown("""
    **Float Churn Ratio:** 
    $$\\frac{\\text{Total Base Volume Traded}}{\\text{Public Free Float Shares}}$$
    *Measures weak retail hands shakeout over consolidation floors.*
    """)

with st.sidebar.expander("📖 Mode 2 Matrix Definitions", expanded=False):
    st.markdown("""
    **Annualized ROCE:** 
    $$\\frac{\\text{EBIT (Operating Income)}}{\\text{Total Assets} - \\text{Current Liabilities}}$$
    *Filters core capital efficiency.*
    
    **Strong Hands Constraint:**
    $$\\text{Promoter Lock} \\ge 70\\%$$
    """)

with st.sidebar.expander("📖 Mode 3 Matrix Definitions", expanded=False):
    st.markdown("""
    **Contraction Array:** 
    $$T_1 (3\\%-6\\%) > T_2 (1\\%-2.8\\%) > T_3 (0.1\\%-0.9\\%)$$
    *Tracks structural volatility exhaustion prior to high-volume breakouts.*
    """)

st.sidebar.write("---")
MIN_MARKET_CAP_CR = st.sidebar.number_input("Min Market Cap (Cr)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("Max IPO Age Window", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("Target Churn Gate (%)", 10, 100, 30)

NIFTY_500_SEEDS = ["PAYTM.NS", "ZOMATO.NS", "LIC.NS", "AWL.NS", "DELHIVERY.NS", "NYKAA.NS", "TCS.NS", "ASIANPAINT.NS", "BRITANNIA.NS"]

# ==============================================================================
# 02. DATA CORE LOGIC SYSTEMS (STABLE BACKENDS)
# ==============================================================================
def execute_mode_1(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None, f"Empty history: {symbol}"
        
        first_date = hist.index[0].date()
        if (datetime.date.today() - first_date).days > (MAX_IPO_AGE_YEARS * 365): return None, None
        
        df = hist.tail(int(MAX_IPO_AGE_YEARS * 250))
        info = t.info
        shares = info.get("sharesOutstanding") or info.get("impliedSharesOutstanding")
        f_shares = info.get("floatShares")
        if not shares or not f_shares: return None, f"Float restricted token data for {symbol}"
        
        price = df["Close"].iloc[-1]
        mcap = (shares * price) / 10_000_000
        if mcap < MIN_MARKET_CAP_CR: return None, None
        
        ff_mcap = (f_shares * price) / 10_000_000
        df["100_DMA"] = df["Close"].rolling(100).mean()
        df["200_DMA"] = df["Close"].rolling(200).mean()
        
        low_p = df["Close"].min()
        base = df[df["Close"] <= low_p * 1.25]
        base_turnover = (base["Volume"] * base["Close"]).sum() / 10_000_000
        churn = min((base_turnover / ff_mcap), 1.0)
        
        status = "WATCHLIST"
        if churn * 100 >= TARGET_ABSORPTION_PCT and df["100_DMA"].iloc[-1] > df["200_DMA"].iloc[-1]:
            status = "🔥 BUY TRIGGER"
            
        return {
            "Symbol": symbol.replace(".NS", ""),
            "Price (₹)": round(price, 2),
            "Market Cap (Cr)": round(mcap, 2),
            "Free-Float Cap (Cr)": round(ff_mcap, 2),
            "Float Churn Ratio": churn,
            "Status": status
        }, None
    except Exception as e: return None, str(e)

def execute_mode_2(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="2y")
        if df.empty or len(df) < 200: return None, f"Insufficient price records: {symbol}"
        
        abs_bs = t.balance_sheet
        abs_fi = t.financials
        info = t.info
        if abs_bs.empty or abs_fi.empty: return None, f"Financials structural block: {symbol}"
        
        abs_fi = abs_fi.reindex(columns=sorted(abs_fi.columns, reverse=True))
        abs_bs = abs_bs.reindex(columns=sorted(abs_bs.columns, reverse=True))
        
        price = df["Close"].iloc[-1]
        shares = info.get("sharesOutstanding") or 1
        mcap = (shares * price) / 10_000_000
        
        ebit = abs_fi.loc["Operating Income"].iloc[0] if "Operating Income" in abs_fi.index else 0
        ta = abs_bs.loc["Total Assets"].iloc[0] if "Total Assets" in abs_bs.index else 1
        cl = abs_bs.loc["Total Current Liabilities"].iloc[0] if "Total Current Liabilities" in abs_bs.index else 0
        
        cap_employed = ta - cl
        roce = (ebit / cap_employed) * 100 if cap_employed > 0 else 0
        debt = abs_bs.loc["Total Debt"].iloc[0] if "Total Debt" in abs_bs.index else 0
        equity = abs_bs.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in abs_bs.index else 1
        de = debt / equity
        
        f_shares = info.get("floatShares", 0) or 0
        lock_pct = ((shares - f_shares) / shares) * 100
        
        df["200_DMA"] = df["Close"].rolling(200).mean()
        dma200 = df["200_DMA"].iloc[-1]
        
        status = "Watchlist Stable"
        if roce >= 20.0 and de <= 0.25 and lock_pct >= 70.0:
            status = "⭐ HIGH QUALITY"
            if price <= dma200 * 0.85: status = "🎯 DISCOUNT VALUATION"
            
        return {
            "Symbol": symbol.replace(".NS", ""),
            "Price (₹)": round(price, 2),
            "Market Cap (Cr)": round(mcap, 2),
            "ROCE %": round(roce, 2),
            "Debt/Equity": round(de, 2),
            "Promoter Lock %": round(lock_pct, 2),
            "Status": status
        }, None
    except Exception as e: return None, str(e)

def execute_mode_3(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(interval="15m", period="5d")
        if df.empty or len(df) < 75: return None, f"Interval limits processing error for {symbol}"
        
        r_max = df["High"].tail(60).max()
        price = df["Close"].iloc[-1]
        
        low_t1 = df["Low"].tail(60).iloc[0:25].min()
        low_t2 = df["Low"].tail(35).iloc[0:20].min()
        low_t3 = df["Low"].tail(10).min()
        
        d1 = ((r_max - low_t1) / r_max) * 100
        d2 = ((r_max - low_t2) / r_max) * 100
        d3 = ((r_max - low_t3) / r_max) * 100
        
        df["20_SMA"] = df["Close"].rolling(20).mean()
        df["20_STD"] = df["Close"].rolling(20).std()
        bw = ((df["20_SMA"] + (2 * df["20_STD"])) - (df["20_SMA"] - (2 * df["20_STD"]))) / df["20_SMA"]
        
        vol_sma = df["Volume"].rolling(20).mean()
        
        status = "Neutral Volatility"
        if (3.0 <= d1 <= 6.0) and (1.0 <= d2 <= 2.8) and (0.1 <= d3 <= 0.9) and (d1 > d2 > d3):
            status = "🟢 COMPLIANT"
            if bw.iloc[-1] <= bw.tail(30).min() * 1.15 and df["Volume"].iloc[-1] >= vol_sma.iloc[-1] * 2.0:
                status = "⚡ SQUEEZE BREAKOUT"
                
        return {
            "Symbol": symbol.replace(".NS", ""),
            "Live Price (₹)": round(price, 2),
            "Ceiling Resistance": round(r_max, 2),
            "T1 Wave %": round(d1, 2),
            "T2 Wave %": round(d2, 2),
            "T3 Wave %": round(d3, 2),
            "Status": status
        }, None
    except Exception as e: return None, str(e)

# ==============================================================================
# 03. HIGH-END FRONT-END COMPILATION INTERFACE
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "🚀 Mode 1: IPO Turnaround Suite", 
    "💎 Mode 2: Value-Owner Fundamentals", 
    "🎯 Mode 3: Intraday VCP Engine"
])

# --- TAB 1: OPERATIONAL INTERFACE ---
with tab1:
    st.markdown('<div class="quant-card"><h3>🚀 Institutional IPO Turnaround Matrix</h3>'
                '<p>Scans the seed array for assets matching strict public float accumulation variables over dynamic multi-year horizons.</p></div>', unsafe_allow_html=True)
    
    if st.button("Run Quantitative IPO Sweep"):
        res_m1, err_m1 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(execute_mode_1, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(futures):
                r, e = f.result()
                if r: res_m1.append(r)
                if e: err_m1.append(e)
                
        st.columns(3)[0].metric("Total Matrix Rows", len(res_m1))
        if res_m1:
            st.data_editor(
                pd.DataFrame(res_m1),
                column_config={
                    "Float Churn Ratio": st.column_config.ProgressColumn("Public Float Rotation", min_value=0.0, max_value=1.0, format="%.2f"),
                    "Status": st.column_config.SelectboxColumn("Signal Validation", options=["🔥 BUY TRIGGER", "🟢 TREND CONFIRMED", "WATCHLIST"])
                },
                disabled=True, use_container_width=True, key="m1_grid"
            )
        if err_m1:
            with st.expander("⚠️ Mode 1 Pipeline Exclusions"):
                for err in err_m1: st.markdown(f"• `{err}`")

# --- TAB 2: OPERATIONAL INTERFACE ---
with tab2:
    st.markdown('<div class="quant-card"><h3>💎 Corporate Business Owner Engine</h3>'
                '<p>Evaluates long-term stability and business efficiency metrics using annualized data streams.</p></div>', unsafe_allow_html=True)
    
    if st.button("Run Annualized Fundamentals Sweep"):
        res_m2, err_m2 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(execute_mode_2, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(futures):
                r, e = f.result()
                if r: res_m2.append(r)
                if e: err_m2.append(e)
                
        st.columns(3)[0].metric("Qualified Value Systems", len(res_m2))
        if res_m2:
            st.data_editor(
                pd.DataFrame(res_m2),
                column_config={
                    "ROCE %": st.column_config.NumberColumn("Return on Capital", format="%.2f%%"),
                    "Debt/Equity": st.column_config.NumberColumn("Leverage Factor", format="%.2f"),
                    "Promoter Lock %": st.column_config.ProgressColumn("Strong Hands Lock", min_value=0.0, max_value=100.0, format="%.1f%%")
                },
                disabled=True, use_container_width=True, key="m2_grid"
            )
        if err_m2:
            with st.expander("⚠️ Mode 2 Pipeline Exclusions"):
                for err in err_m2: st.markdown(f"• `{err}`")

# --- TAB 3: OPERATIONAL INTERFACE ---
with tab3:
    st.markdown('<div class="quant-card"><h3>🎯 Intraday Volatility Contraction Pattern</h3>'
                '<p>Monitors 15-minute price action windows to capture micro-level structure squeezes and structural volume drops.</p></div>', unsafe_allow_html=True)
    
    if st.button("Run Intraday VCP Squeeze Sweep"):
        res_m3, err_m3 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(execute_mode_3, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(futures):
                r, e = f.result()
                if r: res_m3.append(r)
                if e: err_m3.append(e)
                
        st.columns(3)[0].metric("VCP Arrays Captured", len(res_m3))
        if res_m3:
            st.data_editor(
                pd.DataFrame(res_m3),
                column_config={
                    "T1 Wave %": st.column_config.NumberColumn("Wave 1 Depth", format="%.2f%%"),
                    "T2 Wave %": st.column_config.NumberColumn("Wave 2 Depth", format="%.2f%%"),
                    "T3 Wave %": st.column_config.NumberColumn("Wave 3 Depth", format="%.2f%%"),
                },
                disabled=True, use_container_width=True, key="m3_grid"
            )
        if err_m3:
            with st.expander("⚠️ Mode 3 Pipeline Exclusions"):
                for err in err_m3: st.markdown(f"• `{err}`")
        
