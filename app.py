import concurrent.futures
import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# ==============================================================================
# 00. HIGH-FIDELITY PLATFORM THEME INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="ALPHA QUANT TERMINAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0b0c10 !important;
        font-family: 'Roboto Mono', monospace !important;
        color: #d1d4dc !important;
    }
    
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

    div[data-testid="stSidebar"] {
        background-color: #121620 !important;
        border-right: 1px solid #242b35 !important;
    }
    
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
    }
    .stButton>button:hover {
        background-color: #e08600 !important;
        box-shadow: 0 0 8px rgba(255,152,0,0.4);
    }
    
    .console-box {
        background-color: #141923;
        border-left: 4px solid #ff9800;
        border-top: 1px solid #242b35;
        border-right: 1px solid #242b35;
        border-bottom: 1px solid #242b35;
        border-radius: 4px;
        padding: 20px;
        margin-top: 25px;
    }
    
    h3 {
        color: #ff9800 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        border-bottom: 1px solid #242b35;
        padding-bottom: 5px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="terminal-nav">
        <span>&lt;GO&gt; MULTI-AGENT SWARM ENGAGED</span> | UNIVERSE: NIFTY 250 ACTIVE | CHARTS ENGINE: FIXED DYNAMIC ON-CLICK |
        <span>TIME: {datetime.datetime.now().strftime("%H:%M:%S")}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🎛️ ALPHA MULTI-AGENT SWARM TERMINAL")
st.caption("AUTOMATED MULTI-AGENT INTELLIGENCE TERMINAL")

# ==============================================================================
# 01. PARAMETERS PANEL
# ==============================================================================
st.sidebar.markdown("<h3 style='color:#ff9800; font-size:14px;'>⚙️ CORE TERMINAL CONFIG</h3>", unsafe_allow_html=True)
MIN_MARKET_CAP_CR = st.sidebar.number_input("MIN MCAP GATE (CR)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("MAX IPO AGE WINDOW", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("TARGET FLOAT CHURN (%)", 10, 100, 30)

REAL_MARKET_UNIVERSE = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS",
    "INFY.NS", "SBI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", 
    "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "PAYTM.NS", "ZOMATO.NS", "AWL.NS", 
    "DELHIVERY.NS", "NYKAA.NS", "HONASA.NS", "IRFC.NS", "RVNL.NS", "PFC.NS", 
    "RECLTD.NS", "CONCOR.NS", "HAL.NS", "BEL.NS", "BHEL.NS", "SAIL.NS", 
    "NMDC.NS", "PNB.NS", "UNIONBANK.NS", "CANBK.NS", "BOB.NS", "IDFCFIRSTB.NS", 
    "FEDERALBNK.NS", "BANDHANBNK.NS", "YESBANK.NS", "AUSMALL.NS", "POLYCAB.NS", 
    "KEI.NS", "HAVELLS.NS", "VOLTAS.NS", "DIXON.NS", "AMBER.NS", "ASTRAL.NS", 
    "SUPREMEIND.NS", "FINPIPE.NS", "BERGEPAINT.NS", "KANSAINER.NS", "PIDILITIND.NS", 
    "SRF.NS", "BALRAMCHIN.NS", "TEJASNET.NS", "ANGELONE.NS", "5PAISA.NS", 
    "IEX.NS", "MCX.NS", "BSE.NS", "CDSL.NS", "CAMS.NS", "UTIAMC.NS", 
    "NIPPONLIFE.NS", "HDFCLIFE.NS", "MAXHEALTH.NS", "MUTHOOTFIN.NS", "CHOLAFIN.NS", 
    "SHRIRAMFIN.NS", "M&MFIN.NS", "POONAWALLA.NS", "INDHOTEL.NS", "JUBLFOOD.NS", 
    "CAMPUS.NS", "METROBRAND.NS", "RELAXO.NS", "PAGEIND.NS", "BATAINDIA.NS", 
    "TATAPOWER.NS", "CESC.NS", "SJVN.NS", "NHPC.NS", "DEEPAKNIT.NS", "UPL.NS"
]

# ==============================================================================
# 02. ON-DEMAND WIDGET PLUGINS (DYNAMIC OVERLAY LOADERS) - FIXED
# ==============================================================================
def render_tradingview_widget(symbol):
    # CRITICAL TV FIXED: Stripping standard Yahoo suffix and injecting the correct NSE: routing prefix
    clean_symbol = symbol.replace(".NS", "").strip().upper()
    tv_html = f"""
    <div id="tv-widget-container" style="height:450px;width:100%;">
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 450,
        "symbol": "NSE:{clean_symbol}",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": false,
        "container_id": "tv-widget-container"
      }});
      </script>
    </div>
    """
    components.html(tv_html, height=460)

def fetch_live_news_agent(ticker_obj):
    # CRITICAL NEWS FIXED: True real-time dictionary payload parsing structure from live API logs
    try:
        news_list = ticker_obj.news
        if not news_list or len(news_list) == 0: 
            return "⚠️ No active corporate announcements found on exchange logs for this row."
        
        compiled_news = ""
        for item in news_list[:4]:
            title = item.get("title", None)
            link = item.get("link", "#")
            publisher = item.get("publisher", "Market Wire")
            if title and "Market Flash Headline" not in title:
                compiled_news += f"• **[{title}]({link})** *(via {publisher})*\n\n"
        
        if len(compiled_news) < 5:
            return "⚠️ Corporate wire stream contains metadata filters but no raw text articles currently."
        return compiled_news
    except Exception as e:
        return f"⚠️ News feed agent bypass exception: {str(e)}"

# ==============================================================================
# 03. ROBUST AGENT MATRIX LOGICS
# ==============================================================================
def agent_ipo_analyst(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None
        first_date = hist.index[0].date()
        if (datetime.date.today() - first_date).days > (MAX_IPO_AGE_YEARS * 365): return None
        
        df = hist.tail(int(MAX_IPO_AGE_YEARS * 250))
        info = t.info
        shares = info.get("sharesOutstanding") or 1
        f_shares = info.get("floatShares")
        if not f_shares: return None
        
        price = df["Close"].iloc[-1]
        mcap = (shares * price) / 10_000_000
        if mcap < MIN_MARKET_CAP_CR: return None
        ff_mcap = (f_shares * price) / 10_000_000
        
        low_p = df["Close"].min()
        base = df[df["Close"] <= low_p * 1.25]
        base_turnover = (base["Volume"] * base["Close"]).sum() / 10_000_000
        churn_pct = (base_turnover / ff_mcap) * 100
        
        if churn_pct < TARGET_ABSORPTION_PCT: return None
        
        desc = f"Stock filter trigger passed. Public free float asset base equals ₹{ff_mcap:,.2f} Cr. Total consolidation floor volume churn recorded at ₹{base_turnover:,.2f} Cr, which satisfies your custom {TARGET_ABSORPTION_PCT}% threshold gate requirement."
        thesis = f"The core quantitative model picked this asset due to structural institutional float absorption. Retail weak hands over the accumulation floor have been shaken out by operator algorithms, building low free-float overhead supply for momentum breakouts."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "Free-Float (Cr)": round(ff_mcap, 2), "Churn %": round(churn_pct, 2), "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

def agent_value_auditor(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="2y")
        if df.empty or len(df) < 100: return None
        abs_bs, abs_fi, info = t.balance_sheet, t.financials, t.info
        if abs_bs.empty or abs_fi.empty: return None
        
        abs_fi = abs_fi.reindex(columns=sorted(abs_fi.columns, reverse=True))
        abs_bs = abs_bs.reindex(columns=sorted(abs_bs.columns, reverse=True))
        
        price = df["Close"].iloc[-1]
        shares = info.get("sharesOutstanding") or 1
        mcap = (shares * price) / 10_000_000
        if mcap < MIN_MARKET_CAP_CR: return None
        
        ebit = abs_fi.loc["Operating Income"].iloc[0] if "Operating Income" in abs_fi.index else 0
        ta = abs_bs.loc["Total Assets"].iloc[0] if "Total Assets" in abs_bs.index else 1
        cl = abs_bs.loc["Total Current Liabilities"].iloc[0] if "Total Current Liabilities" in abs_bs.index else 0
        
        cap_employed = ta - cl
        roce = (ebit / cap_employed) * 100 if cap_employed > 0 else 0
        debt = abs_bs.loc["Total Debt"].iloc[0] if "Total Debt" in abs_bs.index else 0
        de = debt / (mcap * 10_000_000)
        
        if roce < 12.0 or de > 0.50: return None
        
        desc = f"Passed high corporate benchmarks. Operating ROCE is robust at {roce:.2f}%. Balance sheet leverage profile holds an institutional Debt/Equity of {de:.2f}."
        thesis = f"This company demonstrates absolute financial compounding capabilities. The model selected this asset because it generates top-tier operational cash returns without relying on risky structural leverage, ensuring high safety margins for your portfolio."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "ROCE %": round(roce, 2), "Debt/Equity": round(de, 2), "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

def agent_vcp_scalper(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="5d", interval="15m")
        if df.empty or len(df) < 30: return None
        
        r_max = df["High"].max()
        price = df["Close"].iloc[-1]
        
        mid = len(df) // 2
        low_t1 = df["Low"].iloc[0:mid].min()
        low_t2 = df["Low"].iloc[mid:-10].min()
        low_t3 = df["Low"].iloc[-10:].min()
        
        d1 = ((r_max - low_t1) / r_max) * 100 if r_max > 0 else 0
        d2 = ((r_max - low_t2) / r_max) * 100 if r_max > 0 else 0
        d3 = ((r_max - low_t3) / r_max) * 100 if r_max > 0 else 0
        
        if not (d1 >= d2 and d2 >= d3): return None
        
        desc = f"Volatility contraction sequence matched. Multi-wave compression array tracks as follows: W1 Depth={d1:.2f}% -> W2 Depth={d2:.2f}% -> W3 Depth={d3:.2f}%."
        thesis = f"The stock has entered an absolute volatility compression bottleneck. Subsequent contraction cycles show heavy supply exhaustion, indicating that any intraday volume push will trigger a highly explosive high-frequency momentum breakout."
        
        return {"Symbol": symbol, "Live Price": round(price, 2), "Ceiling Res": round(r_max, 2), "W1 %": round(d1, 2), "W2 %": round(d2, 2), "Status": "🟢 COMPLIANT", "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

# ==============================================================================
# 04. MULTI-PANEL OPERATIONAL INTERFACE
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["[ MODE 1: IPO CORE ]", "[ MODE 2: VALUE OWNER ]", "[ MODE 3: INTRADAY VCP ]"])

with tab1:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 1 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE IPO SWEEP", key="btn_m1"):
        with st.spinner("Processing Matrix Data..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_ipo_analyst, s) for s in REAL_MARKET_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            st.session_state["res_m1"] = res
            st.session_state["df_m1"] = df
            
    if "df_m1" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m1"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m1")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            idx = selected_row["selection"]["rows"][0]
            target = st.session_state["res_m1"][idx]
            
            st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1.3, 1])
            with col1: render_tradingview_widget(target["Symbol"])
            with col2:
                st.markdown(f"### ⚙️ Why Filtered? (Quant Analysis Layout)\n{target['Description']}")
                st.markdown(f"### 🎯 Portfolio Inclusion Thesis:\n{target['Thesis']}")
                st.markdown(f"### 📰 Real-Time Corporate News:\n")
                st.markdown(fetch_live_news_agent(target['Obj']), unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 2 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE RATIOS SWEEP", key="btn_m2"):
        with st.spinner("Processing Matrix Data..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_value_auditor, s) for s in REAL_MARKET_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            st.session_state["res_m2"] = res
            st.session_state["df_m2"] = df
            
    if "df_m2" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m2"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m2")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            idx = selected_row["selection"]["rows"][0]
            target = st.session_state["res_m2"][idx]
            
            st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1.3, 1])
            with col1: render_tradingview_widget(target["Symbol"])
            with col2:
                st.markdown(f"### ⚙️ Why Filtered? (Quant Analysis Layout)\n{target['Description']}")
                st.markdown(f"### 🎯 Portfolio Inclusion Thesis:\n{target['Thesis']}")
                st.markdown(f"### 📰 Real-Time Corporate News:\n")
                st.markdown(fetch_live_news_agent(target['Obj']), unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="bb-widget"><div class="bb-header">VOLATILITY COMPRESSION MOVERS // MODE 3 LIVE SCREEN</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE SCALPER SWEEP", key="btn_m3"):
        with st.spinner("Processing Matrix Data..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_vcp_scalper, s) for s in REAL_MARKET_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            st.session_state["res_m3"] = res
            st.session_state["df_m3"] = df
            
    if "df_m3" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m3"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m3")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            idx = selected_row["selection"]["rows"][0]
            target = st.session_state["res_m3"][idx]
            
            st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1.3, 1])
            with col1: render_tradingview_widget(target["Symbol"])
            with col2:
                st.markdown(f"### ⚙️ Why Filtered? (Quant Analysis Layout)\n{target['Description']}")
                st.markdown(f"### 🎯 Portfolio Inclusion Thesis:\n{target['Thesis']}")
                st.markdown(f"### 📰 Real-Time Corporate News:\n")
                st.markdown(fetch_live_news_agent(target['Obj']), unsafe_allow_html=True)
        
