import concurrent.futures
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# ==============================================================================
# 00. ADVANCED BLOOMBERG TERMINAL UI THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="ALPHA QUANT TERMINAL",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Strict Bloomberg/Eikon Asset Palette Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    /* Global Base Reset */
    .stApp {
        background-color: #0b0c10 !important;
        font-family: 'Roboto Mono', monospace !important;
        color: #d1d4dc !important;
    }
    
    /* Top Terminal Navigation Bar */
    .terminal-nav {
        background-color: #141823;
        border-bottom: 2px solid #ff9800;
        padding: 8px 15px;
        font-size: 11px;
        color: #8f929d;
        margin-bottom: 20px;
        display: flex;
        gap: 20px;
    }
    .terminal-nav span { color: #ff9800; font-weight: bold; }
    
    /* Bloomberg Custom Card Grids */
    .bb-widget {
        background-color: #121620 !important;
        border: 1px solid #242b35 !important;
        border-radius: 4px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }
    
    .bb-header {
        color: #ff9800 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        border-bottom: 1px solid #242b35;
        padding-bottom: 6px;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }

    /* Input Controls Customization */
    div[data-testid="stSidebar"] {
        background-color: #121620 !important;
        border-right: 1px solid #242b35 !important;
    }
    
    /* Action Buttons */
    .stButton>button {
        background-color: #ff9800 !important;
        color: #0b0c10 !important;
        font-family: 'Roboto Mono', monospace !important;
        font-weight: bold !important;
        font-size: 12px !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 8px 0px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #e08600 !important;
        box-shadow: 0 0 8px rgba(255,152,0,0.4);
    }
    
    /* Metrics Custom Display */
    div[data-testid="stMetric"] {
        background-color: #171d28 !important;
        border: 1px solid #2b3542 !important;
        border-radius: 2px;
        padding: 10px;
    }
    div[data-testid="stMetricLabel"] { color: #8f929d !important; font-size: 11px !important; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 20px !important; font-weight: bold; }
    
    /* Hide Default Elements for Cleanliness */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Live Terminal Top Banner Mock
st.markdown(
    """
    <div class="terminal-nav">
        <span>&lt;GO&gt; TERMINAL ACTIVE</span> | APPL | INFY | TSLA INTEL | MOVERS | CRYPTO | 
        <span>TIME: """ + datetime.datetime.now().strftime("%H:%M:%S") + """</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🎛️ BBG QUANT FILTRATION TERMINAL")
st.caption("High-Fidelity Matrix Screening Interface | Mode Layer Framework")

# ==============================================================================
# 01. SIDEBAR PARAMETER TUNING CONTROL
# ==============================================================================
st.sidebar.markdown("<h3 style='color:#ff9800; font-size:14px;'>⚙️ CORE TERMINAL CONFIG</h3>", unsafe_allow_html=True)
MIN_MARKET_CAP_CR = st.sidebar.number_input("MIN MCAP GATE (CR)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("MAX IPO AGE WINDOW", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("TARGET FLOAT CHURN (%)", 10, 100, 30)

REAL_MARKET_UNIVERSE = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS",
    "INFY.NS", "SBI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", 
    "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "PAYTM.NS", "ZOMATO.NS", "AWL.NS", 
    "DELHIVERY.NS", "NYKAA.NS", "ANGELONE.NS", "CAMS.NS", "BSE.NS", "CDSL.NS"
]

# ==============================================================================
# 02. HARDENED CORE FILTERS BACKENDS
# ==============================================================================
def run_mode_1_core(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None
        first_date = hist.index[0].date()
        if (datetime.date.today() - first_date).days > (MAX_IPO_AGE_YEARS * 365): return None
        
        df = hist.tail(int(MAX_IPO_AGE_YEARS * 250))
        info = t.info
        shares = info.get("sharesOutstanding") or info.get("impliedSharesOutstanding") or 1
        f_shares = info.get("floatShares")
        if not f_shares: return None
        
        price = df["Close"].iloc[-1]
        mcap = (shares * price) / 10_000_000
        if mcap < MIN_MARKET_CAP_CR: return None
        ff_mcap = (f_shares * price) / 10_000_000
        
        df["100_DMA"] = df["Close"].rolling(100).mean()
        df["200_DMA"] = df["Close"].rolling(200).mean()
        
        low_p = df["Close"].min()
        base = df[df["Close"] <= low_p * 1.25]
        base_turnover = (base["Volume"] * base["Close"]).sum() / 10_000_000
        churn_pct = (base_turnover / ff_mcap) * 100
        
        dma_100_val = df["100_DMA"].iloc[-1]
        dma_200_val = df["200_DMA"].iloc[-1]
        gate_trend = dma_100_val > dma_200_val if (not pd.isna(dma_100_val) and not pd.isna(dma_200_val)) else False
        gate_churn = churn_pct >= TARGET_ABSORPTION_PCT
        
        if not gate_churn and not gate_trend: return None
        status = "🔥 BUY TRIGGER" if (gate_trend and gate_churn) else "WATCHLIST (Squeezing)"
        
        desc = f"Listed: {first_date}. Liquid Float Capital: ₹{ff_mcap:,.2f} Cr. Base Floor Volume Churn Rotated: {churn_pct:.2f}% against {TARGET_ABSORPTION_PCT}% rule threshold."
        return {"Symbol": symbol.replace(".NS", ""), "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "Free-Float (Cr)": round(ff_mcap, 2), "Churn %": round(churn_pct, 2), "Status": status, "Description": desc}
    except: return None

def run_mode_2_core(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="2y")
        if df.empty or len(df) < 200: return None
        
        abs_bs, abs_fi, info = t.balance_sheet, t.financials, t.info
        if abs_bs.empty or abs_fi.empty: return None
        
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
        f_shares = info.get("floatShares") or 0
        lock_pct = ((shares - f_shares) / shares) * 100 if shares > 0 else 0
        
        if roce < 15.0 or de > 0.40: return None
        status = "⭐ HIGH QUALITY"
        
        desc = f"Annual Operating Income ROCE printing at {roce:.2f}%. Leverage Factor DE: {de:.2f}. Strong Hands Locking Frame: {lock_pct:.2f}%."
        return {"Symbol": symbol.replace(".NS", ""), "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "ROCE %": round(roce, 2), "Debt/Equity": round(de, 2), "Lock %": round(lock_pct, 2), "Status": status, "Description": desc}
    except: return None

def run_mode_3_core(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(interval="15m", period="5d")
        if df.empty or len(df) < 75: return None
        
        r_max = df["High"].tail(60).max()
        price = df["Close"].iloc[-1]
        
        low_t1 = df["Low"].tail(60).iloc[0:25].min()
        low_t2 = df["Low"].tail(35).iloc[0:20].min()
        low_t3 = df["Low"].tail(10).min()
        
        d1 = ((r_max - low_t1) / r_max) * 100
        d2 = ((r_max - low_t2) / r_max) * 100
        d3 = ((r_max - low_t3) / r_max) * 100
        
        if not (d1 > d2 > d3 and d1 <= 12.0): return None
        status = "🟢 VCP COMPLIANT"
        
        desc = f"Multi-Wave sequential compression structure registered. Wave Array: W1={d1:.2f}% -> W2={d2:.2f}% -> W3={d3:.2f}%."
        return {"Symbol": symbol.replace(".NS", ""), "Live Price": round(price, 2), "Ceiling Res": round(r_max, 2), "W1 Depth %": round(d1, 2), "W2 Depth %": round(d2, 2), "W3 Depth %": round(d3, 2), "Status": status, "Description": desc}
    except: return None

# ==============================================================================
# 03. FRONT-END INTERFACE LAYOUT (BLOOMBERG SUB-PANELS RENDER)
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["[ MODE 1: IPO ENGINE ]", "[ MODE 2: VALUE OWNER ]", "[ MODE 3: INTRADAY VCP ]"])

with tab1:
    st.markdown('<div class="bb-widget"><div class="bb-header">PRICING CLOSE-OVER-CLOSE // MODE 1 ENGINE ACTIVE</div>'
                'Tracks micro-level public float squeeze and rotation indices on dynamic IPO cycles.</div>', unsafe_allow_html=True)
    
    if st.button("RUN MODE 1 MATRIX SWEEP"):
        res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(run_mode_1_core, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        
        if res:
            st.data_editor(pd.DataFrame(res).drop(columns=["Description"]), use_container_width=True, disabled=True, key="m1_editor")
            st.markdown("<h4 style='color:#ff9800; font-size:12px; margin-top:15px;'>ANALYSIS REPORTS:</h4>", unsafe_allow_html=True)
            for r in res:
                with st.expander(f"• {r['Symbol']} Matrix Validation"): st.write(r["Description"])
        else: st.warning("NO ASSETS PASSED THE QUANT STRAT DATA FILTER PROTOCOLS.")

with tab2:
    st.markdown('<div class="bb-widget"><div class="bb-header">FINANCIAL RATIOS // MODE 2 CAPITAL EFFICIENCY MONITOR</div>'
                'Filters corporate cash generators passing strict annualized operational return metrics.</div>', unsafe_allow_html=True)
    
    if st.button("RUN MODE 2 RATIOS SWEEP"):
        res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(run_mode_2_core, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
            
        if res:
            st.data_editor(pd.DataFrame(res).drop(columns=["Description"]), use_container_width=True, disabled=True, key="m2_editor")
            st.markdown("<h4 style='color:#ff9800; font-size:12px; margin-top:15px;'>ANALYSIS REPORTS:</h4>", unsafe_allow_html=True)
            for r in res:
                with st.expander(f"• {r['Symbol']} Corporate Log"): st.write(r["Description"])
        else: st.warning("NO STOCKS CLEARING CRITERIA GATES TODAY.")

with tab3:
    st.markdown('<div class="bb-widget"><div class="bb-header">VOLATILITY COMPRESSION MOVERS // MODE 3 LIVE SCREEN</div>'
                'Monitors high-frequency 15-minute intervals for sequential structural energy contraction.</div>', unsafe_allow_html=True)
    
    if st.button("RUN MODE 3 INTRADAY SWEEP"):
        res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(run_mode_3_core, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
            
        if res:
            st.data_editor(pd.DataFrame(res).drop(columns=["Description"]), use_container_width=True, disabled=True, key="m3_editor")
            st.markdown("<h4 style='color:#ff9800; font-size:12px; margin-top:15px;'>ANALYSIS REPORTS:</h4>", unsafe_allow_html=True)
            for r in res:
                with st.expander(f"• {r['Symbol']} Structural Proof"): st.write(r["Description"])
        else: st.warning("NO HIGH-FREQUENCY WAVE COMPRESSIONS DETECTED.")
