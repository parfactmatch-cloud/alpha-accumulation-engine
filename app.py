import concurrent.futures
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# ==============================================================================
# 00. HIGH-END THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="Alpha-Accumulation Quant Suite Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0d1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
    }
    .quant-container {
        background-color: #161b22;
        border-left: 4px solid #58a6ff;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .metric-pass { color: #56d364; font-weight: bold; }
    .metric-warn { color: #e3b341; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Alpha-Accumulation Institutional Quant Suite")
st.caption("Strict Filtration Engine | Only Qualified Assets Rendered")

# ==============================================================================
# 01. EXPANDED UNIVERSE SEEDS (NIFTY 50 + NEW IPOs COMBINED)
# ==============================================================================
st.sidebar.title("🔧 Parameters Tuning Panel")
MIN_MARKET_CAP_CR = st.sidebar.number_input("Minimum Market Cap Gate (Cr)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("Maximum IPO Listing Scope (Years)", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("Target Retail Churn Threshold (%)", 10, 100, 30)

# Expanded Seed List to see distinct results across modes
NIFTY_500_SEEDS = [
    "PAYTM.NS", "ZOMATO.NS", "LIC.NS", "AWL.NS", "DELHIVERY.NS", "NYKAA.NS", 
    "TCS.NS", "ASIANPAINT.NS", "BRITANNIA.NS", "INFY.NS", "RELIANCE.NS", 
    "HDFCBANK.NS", "ICICIBANK.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS"
]

# ==============================================================================
# 02. STRICT FILTRATION CORE LOGICS
# ==============================================================================
def run_mode_1_core(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None, None
        
        first_date = hist.index[0].date()
        listing_age_days = (datetime.date.today() - first_date).days
        listing_age_years = round(listing_age_days / 365.25, 2)
        
        # Rule 1: Age Gate
        if listing_age_days > (MAX_IPO_AGE_YEARS * 365): return None, None
        
        df = hist.tail(int(MAX_IPO_AGE_YEARS * 250))
        info = t.info
        shares = info.get("sharesOutstanding") or info.get("impliedSharesOutstanding") or 1
        f_shares = info.get("floatShares")
        if not f_shares: return None, None
        
        price = df["Close"].iloc[-1]
        mcap = (shares * price) / 10_000_000
        if mcap < MIN_MARKET_CAP_CR: return None, None
        
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
        
        # STRICT FILTER: Show in table ONLY if it's a Buy Trigger or Strong Watchlist
        if not gate_churn and not gate_trend: return None, None
        
        status = "🔥 BUY TRIGGER" if (gate_trend and gate_churn) else "WATCHLIST (Squeezing)"
        
        desc = (
            f"**Listing Analysis:** Stock listed on {first_date} ({listing_age_years} Yrs old). "
            f"Current public retail liquid float capital stands at **₹{ff_mcap:,.2f} Cr**. "
            f"Within the extreme consolidation baseline floor, institutional hands have rotated **₹{base_turnover:,.2f} Cr** in accumulated trades. "
            f"This translates to an absolute **{churn_pct:.2f}% public free-float rotation** against your {TARGET_ABSORPTION_PCT}% barrier."
        )
        
        return {
            "Symbol": symbol.replace(".NS", ""), "Price (₹)": round(price, 2),
            "Market Cap (Cr)": round(mcap, 2), "Free-Float Cap (Cr)": round(ff_mcap, 2),
            "Float Churn Ratio": min(churn_pct / 100.0, 1.0), "Status": status, "Detailed Description": desc
        }, None
    except Exception as e: return None, str(symbol + ": " + str(e))

def run_mode_2_core(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="2y")
        if df.empty or len(df) < 200: return None, None
        
        abs_bs, abs_fi, info = t.balance_sheet, t.financials, t.info
        if abs_bs.empty or abs_fi.empty: return None, None
        
        abs_fi = abs_fi.reindex(columns=sorted(abs_fi.columns, reverse=True))
        abs_bs = abs_bs.reindex(columns=sorted(abs_bs.columns, reverse=True))
        
        price = df["Close"].iloc[-1]
        shares = info.get("sharesOutstanding") or 1
        mcap = (shares * price) / 10_000_000
        
        ebit = abs_fi.loc["Operating Income"].iloc[0] if "Operating Income" in abs_fi.index else 0
        ta = abs_bs.loc["Total Assets"].iloc[0] if "Total Assets" in abs_bs.index else 1
        cl = abs_bs.loc["Total Current Liabilities"].iloc[0] if "Total Current Liabilities" in abs_bs.index else 0
        
        cap_employed = ta - cl
        roce = (ebit / capital_employed) * 100 if cap_employed > 0 else 0
        debt = abs_bs.loc["Total Debt"].iloc[0] if "Total Debt" in abs_bs.index else 0
        equity = abs_bs.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in abs_bs.index else 1
        de = debt / equity
        
        f_shares = info.get("floatShares") or 0
        lock_pct = ((shares - f_shares) / shares) * 100 if shares > 0 else 0
        
        # STRICT FILTER: REJECT instantly if criteria fails
        if roce < 20.0 or de > 0.25 or lock_pct < 70.0: return None, None
        
        df["200_DMA"] = df["Close"].rolling(window=200).mean()
        dma200 = df["200_DMA"].iloc[-1]
        pct_from_200 = ((price - dma200) / dma200) * 100 if dma200 > 0 else 0
        
        status = "⭐ HIGH QUALITY"
        if price <= dma200 * 0.85: status = "🎯 DISCOUNT VALUATION"
            
        desc = (
            f"**Fundamental Breakdown:** Enterprise return architecture yields an annualized **ROCE of {roce:.2f}%** (Passed >=20%). "
            f"Balance Sheet structural leverage profile holds a **Debt-to-Equity of {de:.2f}** (Passed <=0.25). "
            f"Institutional proxy calculation shows **Promoter/Strong Hands control {lock_pct:.2f}%** of equity base float."
        )
        
        return {
            "Symbol": symbol.replace(".NS", ""), "Price (₹)": round(price, 2), "Market Cap (Cr)": round(mcap, 2),
            "ROCE %": round(roce, 2), "Debt/Equity": round(de, 2), "Promoter Lock %": round(lock_pct, 2),
            "Status": status, "Detailed Description": desc
        }, None
    except Exception as e: return None, None

def run_mode_3_core(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(interval="15m", period="5d")
        if df.empty or len(df) < 75: return None, None
        
        r_max = df["High"].tail(60).max()
        price = df["Close"].iloc[-1]
        
        low_t1 = df["Low"].tail(60).iloc[0:25].min()
        low_t2 = df["Low"].tail(35).iloc[0:20].min()
        low_t3 = df["Low"].tail(10).min()
        
        d1 = ((r_max - low_t1) / r_max) * 100
        d2 = ((r_max - low_t2) / r_max) * 100
        d3 = ((r_max - low_t3) / r_max) * 100
        
        # STRICT FILTER: Show ONLY if it matches the Minervini VCP wave sequence
        gate_waves = (3.0 <= d1 <= 6.0) and (1.0 <= d2 <= 2.8) and (0.1 <= d3 <= 0.9) and (d1 > d2 > d3)
        if not gate_waves: return None, None
        
        df["20_SMA"] = df["Close"].rolling(20).mean()
        df["20_STD"] = df["Close"].rolling(20).std()
        bw = ((df["20_SMA"] + (2 * df["20_STD"])) - (df["20_SMA"] - (2 * df["20_STD"]))) / df["20_SMA"]
        live_bw = bw.iloc[-1]
        
        vol_sma = df["Volume"].rolling(20).mean()
        live_vol = df["Volume"].iloc[-1]
        avg_vol = vol_sma.iloc[-1]
        
        status = "🟢 VCP COMPLIANT"
        if live_bw <= bw.tail(30).min() * 1.15 and live_vol >= avg_vol * 2.0:
            status = "⚡ SQUEEZE BREAKOUT ACTIVE"
        
        desc = (
            f"**VCP Structure Squeeze:** 15-min bars match the contraction protocol. "
            f"Wave depths: **W1: {d1:.2f}%** | **W2: {d2:.2f}%** | **W3: {d3:.2f}%**. "
            f"Volatility Squeeze Bandwidth is tight at **{live_bw:.4f}**."
        )
        
        return {
            "Symbol": symbol.replace(".NS", ""), "Live Price (₹)": round(price, 2), "Ceiling Resistance": round(r_max, 2),
            "T1 Wave %": round(d1, 2), "T2 Wave %": round(d2, 2), "T3 Wave %": round(d3, 2),
            "Status": status, "Detailed Description": desc
        }, None
    except Exception as e: return None, None

# ==============================================================================
# 03. HIGH-END FRONT-END MULTI-TAB MATRIX
# ==============================================================================
t1, t2, t3 = st.tabs([
    "🚀 Upgraded Mode 1: IPO Turnaround Suite",
    "💎 Mode 2: Value-Owner Fundamentals",
    "🎯 Mode 3: Intraday VCP Engine"
])

# --- TAB 1 ---
with t1:
    st.markdown('<div class="quant-container"><h3>🚀 Mode 1: IPO Turnaround (Strict Filtered)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute Quantitative IPO Float Sweep"):
        res_m1, err_m1 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_1_core, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(f_dict):
                r, e = f.result()
                if r: res_m1.append(r)
                if e: err_m1.append(e)
        
        if res_m1:
            df1 = pd.DataFrame(res_m1)
            st.data_editor(df1.drop(columns=["Detailed Description"]), column_config={"Float Churn Ratio": st.column_config.ProgressColumn("Public Float Rotation Progress", min_value=0.0, max_value=1.0)}, disabled=True, use_container_width=True, key="m1_view")
            for row in res_m1:
                with st.expander(f"📋 Analysis: {row['Symbol']} — ({row['Status']})"):
                    st.write(row["Detailed Description"])
        else: st.warning("No assets cleared the strict IPO accumulation gates today.")

# --- TAB 2 ---
with t2:
    st.markdown('<div class="quant-container"><h3>💎 Mode 2: Business Owner Corporate Analytics Suite (Filtered)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute Corporate Fundamentals Sweep"):
        res_m2, err_m2 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_2_core, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(f_dict):
                r, e = f.result()
                if r: res_m2.append(r)
        
        if res_m2:
            df2 = pd.DataFrame(res_m2)
            st.data_editor(df2.drop(columns=["Detailed Description"]), column_config={"Promoter Lock %": st.column_config.ProgressColumn("Strong Hands Float Control", min_value=0.0, max_value=100.0)}, disabled=True, use_container_width=True, key="m2_view")
            for row in res_m2:
                with st.expander(f"📋 Analysis: {row['Symbol']}"): st.write(row["Detailed Description"])
        else: st.warning("No assets cleared the strict ROCE >= 20% & Debt <= 0.25 conditions.")

# --- TAB 3 ---
with t3:
    st.markdown('<div class="quant-container"><h3>🎯 Mode 3: Price Action Volatility Contraction Pattern (Strict)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute High-Frequency VCP Squeeze Sweep"):
        res_m3, err_m3 = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_3_core, s): s for s in NIFTY_500_SEEDS}
            for f in concurrent.futures.as_completed(f_dict):
                r, e = f.result()
                if r: res_m3.append(r)
        
        if res_m3:
            df3 = pd.DataFrame(res_m3)
            st.data_editor(df3.drop(columns=["Detailed Description"]), disabled=True, use_container_width=True, key="m3_view")
            for row in res_m3:
                with st.expander(f"📋 Analysis: {row['Symbol']}"): st.write(row["Detailed Description"])
        else: st.warning("No assets currently match the sequential VCP wave rules ($T_1 > T_2 > T_3$).")
