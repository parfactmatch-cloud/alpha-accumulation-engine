import concurrent.futures
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# ==============================================================================
# 00. PREMIUM FINANCIAL THEME INJECTION
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
st.caption("Expanded Nifty 250 (Large & Midcap) Multi-Engine Terminal")

# ==============================================================================
# 01. PARAMETERS & EXPANDED MARKET UNIVERSE (NIFTY 250 BENCHMARK ARRAY)
# ==============================================================================
st.sidebar.title("🔧 Parameters Tuning Panel")
MIN_MARKET_CAP_CR = st.sidebar.number_input("Minimum Market Cap Gate (Cr)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("Maximum IPO Listing Scope (Years)", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("Target Retail Churn Threshold (%)", 10, 100, 30)

# True Nifty 250 Heavyweight and Midcap Core Screener Base Array
REAL_MARKET_UNIVERSE = [
    # Top Heavyweights & Liquid Core (Nifty 50 Base)
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS",
    "INFY.NS", "SBI.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", 
    "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", 
    "KOTAKBANK.NS", "TITAN.NS", "AXISBANK.NS", "DMART.NS", "ONGC.NS", "NTPC.NS", 
    "TATAMOTORS.NS", "ULTRACEMCO.NS", "COALINDIA.NS", "ASIANPAINT.NS", "BAJAJFINSV.NS", 
    "JIOFIN.NS", "POWERGRID.NS", "NESTLEIND.NS", "JSWSTEEL.NS", "M&M.NS", "TATASTEEL.NS", 
    "ADANIPORTS.NS", "GRASIM.NS", "SBILIFE.NS", "TECHM.NS", "WIPRO.NS", "HINDALCO.NS", 
    "INDUSINDBK.NS", "EICHERMOT.NS", "CIPLA.NS", "DIVISLAB.NS", "BAJAJ-AUTO.NS", 
    "BPCL.NS", "DRREDDY.NS", "BRITANNIA.NS", "TATACONSUM.NS", "APOLLOHOSP.NS", "HEROMOTOCO.NS",
    # Dynamic New Age & Midcap High Growth Layer (Nifty Next 50 & Midcap 100 Cores)
    "PAYTM.NS", "ZOMATO.NS", "AWL.NS", "DELHIVERY.NS", "NYKAA.NS", "HONASA.NS",
    "IRFC.NS", "RVNL.NS", "PFC.NS", "RECLTD.NS", "CONCOR.NS", "HAL.NS", "BEL.NS",
    "BHEL.NS", "SAIL.NS", "NMDC.NS", "PNB.NS", "UNIONBANK.NS", "CANBK.NS", "BOB.NS",
    "IDFCFIRSTB.NS", "FEDERALBNK.NS", "BANDHANBNK.NS", "YESBANK.NS", "AUSMALL.NS",
    "J&KBANK.NS", "SOUTHBANK.NS", "POLYCAB.NS", "KEI.NS", "HAVELLS.NS", "VOLTAS.NS",
    "DIXON.NS", "AMBER.NS", "ASTRAL.NS", "SUPREMEIND.NS", "FINPIPE.NS", "BERGEPAINT.NS",
    "KANSAINER.NS", "PIDILITIND.NS", "SRF.NS", "BALRAMCHIN.NS", "RENUKA.NS", "EIDPARRY.NS",
    "TATACOMM.NS", "HFCL.NS", "ITI.NS", "TEJASNET.NS", "ROUTE.NS", "ZAGGLE.NS",
    "LTIM.NS", "COFORGE.NS", "PERSISTENT.NS", "MPHASIS.NS", "KPITTECH.NS", "LTTS.NS",
    "TATAELXSI.NS", "CYIENT.NS", "SONACOMS.NS", "UNOMINDA.NS", "ENDURANCE.NS", "BALKRISIND.NS",
    "MRF.NS", "APOLLOTYRE.NS", "JKTYRE.NS", "CEATLTD.NS", "BHARATFORG.NS", "PEL.NS",
    "PVRINOX.NS", "SUNTV.NS", "ZEEL.NS", "NAUKRI.NS", "JUSTDIAL.NS", "TATAINVEST.NS",
    "ANGELONE.NS", "5PAISA.NS", "IEX.NS", "MCX.NS", "BSE.NS", "CDSL.NS", "CAMS.NS",
    "UTIAMC.NS", "NIPPONLIFE.NS", "HDFCLIFE.NS", "MAXHEALTH.NS", "GLOBALHEALTH.NS", "NH.NS",
    "FORTIS.NS", "METROPOLIS.NS", "LALPATHLAB.NS", "SYNGENE.NS", "BIOCON.NS", "GLENMARK.NS",
    "AUBANK.NS", "MUTHOOTFIN.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "M&MFIN.NS", "POONAWALLA.NS",
    "L&TFH.NS", "MANAPPURAM.NS", "CREDITACC.NS", "TAJMANS.NS", "INDHOTEL.NS", "EIHOTEL.NS",
    "DEVYANI.NS", "JUBLFOOD.NS", "WESTLIFE.NS", "CAMPUS.NS", "METROBRAND.NS", "RELAXO.NS",
    "PAGEIND.NS", "BATAINDIA.NS", "VGUARD.NS", "CROMPTON.NS", "BLUESTARCO.NS", "WHIRLPOOL.NS",
    "GLAXO.NS", "SANOFI.NS", "PFIZER.NS", "ABBOTINDIA.NS", "ALKEM.NS", "IPCALAB.NS",
    "TORNTPHARM.NS", "ZYDUSLIFE.NS", "AARTIIND.NS", "DEEPAKNIT.NS", "ATUL.NS", "TATACHEM.NS",
    "UPL.NS", "PIIND.NS", "COROMANDEL.NS", "GNFC.NS", "GSFC.NS", "CHAMBLFERT.NS",
    "FACT.NS", "RCF.NS", "NFL.NS", "TATAPOWER.NS", "CESC.NS", "SJVN.NS", "NHPC.NS",
    "GREENPANEL.NS", "CENTURYPLY.NS", "KAIARICER.NS", "SOMANYCERA.NS", "CERA.NS", "JACOB.NS"
]

# ==============================================================================
# 02. CORE QUANT FILTERS BACKENDS
# ==============================================================================
def run_mode_1_core(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None, None
        
        first_date = hist.index[0].date()
        listing_age_days = (datetime.date.today() - first_date).days
        listing_age_years = round(listing_age_days / 365.25, 2)
        
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
        
        if not gate_churn and not gate_trend: return None, None
        status = "🔥 BUY TRIGGER" if (gate_trend and gate_churn) else "WATCHLIST (Squeezing)"
        
        desc = f"Listed on {first_date} ({listing_age_years} Yrs). Free-Float Churn: {churn_pct:.2f}%."
        return {
            "Symbol": symbol.replace(".NS", ""), "Price (₹)": round(price, 2),
            "Market Cap (Cr)": round(mcap, 2), "Free-Float Cap (Cr)": round(ff_mcap, 2),
            "Float Churn Ratio": min(churn_pct / 100.0, 1.0), "Status": status, "Detailed Description": desc
        }, None
    except Exception as e: return None, None

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
        roce = (ebit / cap_employed) * 100 if cap_employed > 0 else 0
        debt = abs_bs.loc["Total Debt"].iloc[0] if "Total Debt" in abs_bs.index else 0
        equity = abs_bs.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in abs_bs.index else 1
        de = debt / equity
        
        f_shares = info.get("floatShares") or 0
        lock_pct = ((shares - f_shares) / shares) * 100 if shares > 0 else 0
        
        # Broadened optimal gates for Nifty 250 spectrum
        if roce < 15.0 or de > 0.40: return None, None
        
        df["200_DMA"] = df["Close"].rolling(window=200).mean()
        dma200 = df["200_DMA"].iloc[-1]
        
        status = "⭐ HIGH QUALITY"
        if dma200 and price <= dma200 * 0.95: status = "🎯 DISCOUNT VALUATION"
            
        desc = f"Annualized ROCE: {roce:.2f}% | Debt/Equity: {de:.2f} | Promoter/Strong Hands Lock: {lock_pct:.2f}%."
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
        
        # Fluid structure tracking for extended midcap parameters
        gate_waves = (d1 > d2 > d3) and (d1 <= 12.0)
        if not gate_waves: return None, None
        
        status = "🟢 VCP COMPLIANT STRUCTURE"
        desc = f"Intraday Multi-Wave contraction tracking active. W1: {d1:.2f}% | W2: {d2:.2f}% | W3: {d3:.2f}%."
        
        return {
            "Symbol": symbol.replace(".NS", ""), "Live Price (₹)": round(price, 2), "Ceiling Resistance": round(r_max, 2),
            "T1 Wave %": round(d1, 2), "T2 Wave %": round(d2, 2), "T3 Wave %": round(d3, 2),
            "Status": status, "Detailed Description": desc
        }, None
    except Exception as e: return None, None

# ==============================================================================
# 03. FRONT-END RENDERING
# ==============================================================================
t1, t2, t3 = st.tabs([
    "🚀 Upgraded Mode 1: IPO Turnaround",
    "💎 Mode 2: Value-Owner Fundamentals",
    "🎯 Mode 3: Intraday VCP Engine"
])

with t1:
    st.markdown('<div class="quant-container"><h3>🚀 Mode 1: IPO Turnaround Scope (Nifty 250)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute IPO Sweep"):
        res_m1 = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_1_core, s): s for s in REAL_MARKET_UNIVERSE}
            for f in concurrent.futures.as_completed(f_dict):
                r, _ = f.result()
                if r: res_m1.append(r)
        if res_m1:
            st.data_editor(pd.DataFrame(res_m1).drop(columns=["Detailed Description"]), use_container_width=True, disabled=True, key="m1_grid")
        else: st.warning("No recent IPO layer entities matched within the current tuning parameters.")

with t2:
    st.markdown('<div class="quant-container"><h3>💎 Mode 2: Capital Value Systems (Nifty 250)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute Corporate Fundamentals Sweep"):
        res_m2 = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_2_core, s): s for s in REAL_MARKET_UNIVERSE}
            for f in concurrent.futures.as_completed(f_dict):
                r, _ = f.result()
                if r: res_m2.append(r)
        if res_m2:
            st.data_editor(pd.DataFrame(res_m2).drop(columns=["Detailed Description"]), use_container_width=True, disabled=True, key="m2_grid")
            for row in res_m2:
                with st.expander(f"📋 Insights: {row['Symbol']}"): st.write(row["Detailed Description"])
        else: st.warning("No Nifty 250 assets cleared the strict efficiency benchmarks.")

with t3:
    st.markdown('<div class="quant-container"><h3>🎯 Mode 3: Intraday Price Action Squeeze (Nifty 250 Live)</h3></div>', unsafe_allow_html=True)
    if st.button("Execute High-Frequency VCP Sweep"):
        res_m3 = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            f_dict = {ex.submit(run_mode_3_core, s): s for s in REAL_MARKET_UNIVERSE}
            for f in concurrent.futures.as_completed(f_dict):
                r, _ = f.result()
                if r: res_m3.append(r)
        if res_m3:
            st.data_editor(pd.DataFrame(res_m3).drop(columns=["Detailed Description"]), use_container_width=True, disabled=True, key="m3_grid")
            for row in res_m3:
                with st.expander(f"📋 Structure Proof: {row['Symbol']}"): st.write(row["Detailed Description"])
        else: st.warning("No Nifty 250 components are currently printing tight compression envelopes.")
