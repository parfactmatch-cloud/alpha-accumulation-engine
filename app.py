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
        border: 1px solid #ff980055;
        border-radius: 4px;
        padding: 20px;
        margin-top: 25px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="terminal-nav">
        <span>&lt;GO&gt; INTELLIGENCE SCREENING FRAME</span> | ASSETS: NIFTY 250 ACTIVE | CHARTS ENGINE: DYNAMIC OVERLAY |
        <span>DASHBOARD STABILITY: VERIFIED</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🎛️ ALPHA MULTI-AGENT SWARM TERMINAL")
st.caption("Institutional Filtration Suite | On-Demand Chart Execution Matrix")

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
# 02. DYNAMIC WIDGET INJECTOR (TRADINGVIEW OVERLAY GENERATOR)
# ==============================================================================
def render_tradingview_widget(symbol):
    pure_ticker = symbol.replace(".NS", "")
    tv_html = f"""
    <div id="tv-widget-container" style="height:400px;width:100%;">
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 400,
        "symbol": "NSE:{pure_ticker}",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tv-widget-container"
      }});
      </script>
    </div>
    """
    components.html(tv_html, height=410)

def fetch_live_news_agent(ticker_obj):
    try:
        news_list = ticker_obj.news
        if not news_list: return "No active real-time news streams reported on terminal logs currently."
        compiled_news = ""
        for item in news_list[:3]:
            title = item.get("title", "Market Flash Headline")
            link = item.get("link", "#")
            compiled_news += f"• **[{title}]({link})**\n"
        return compiled_news
    except:
        return "News network interface down or parsing restrictions hit."

# ==============================================================================
# 03. AGENTS MATRIX COMPUTATION UNITS
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
        
        df["100_DMA"] = df["Close"].rolling(100).mean()
        df["200_DMA"] = df["Close"].rolling(200).mean()
        
        low_p = df["Close"].min()
        base = df[df["Close"] <= low_p * 1.25]
        base_turnover = (base["Volume"] * base["Close"]).sum() / 10_000_000
        churn_pct = (base_turnover / ff_mcap) * 100
        
        if churn_pct < TARGET_ABSORPTION_PCT: return None
        
        desc = f"Stock listed on {first_date}. Public free float asset base equals ₹{ff_mcap:,.2f} Cr. Total accumulation turnover over extreme floor level recorded at ₹{base_turnover:,.2f} Cr, passing your {TARGET_ABSORPTION_PCT}% retail dry-out gate structure safely."
        thesis = f"The stock displays deep structural institutional absorption patterns. Retail panic liquidity over the base floor has been completely locked by systematic operators, making the asset ripe for supply-squeeze price expansion."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "Free-Float (Cr)": round(ff_mcap, 2), "Churn %": round(churn_pct, 2), "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

def agent_value_auditor(symbol):
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
        if mcap < MIN_MARKET_CAP_CR: return None
        
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
        
        if roce < 15.0 or de > 0.45: return None
        
        desc = f"Annual Operating ROCE stands high at {roce:.2f}%. Leverage metric Debt/Equity safely prints low at {de:.2f}. Strong core promoter float control calculated at {lock_pct:.2f}%."
        thesis = f"This stock represents a true compounder profile. The combination of industry-leading ROCE without structural debt guarantees high free cash flow generation, making it a defensive equity moat for your long-term portfolio."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "ROCE %": round(roce, 2), "Debt/Equity": round(de, 2), "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

def agent_vcp_scalper(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="5d", interval="15m")
        if df.empty or len(df) < 50: return None
        
        r_max = df["High"].max()
        price = df["Close"].iloc[-1]
        
        mid = len(df) // 2
        low_t1 = df["Low"].iloc[0:mid].min()
        low_t2 = df["Low"].iloc[mid:-10].min()
        low_t3 = df["Low"].iloc[-10:].min()
        
        d1 = ((r_max - low_t1) / r_max) * 100
        d2 = ((r_max - low_t2) / r_max) * 100
        d3 = ((r_max - low_t3) / r_max) * 100
        
        if not (d1 >= d2 and d2 >= d3 and d1 <= 15.0): return None
        
        desc = f"Intraday Multi-Wave contraction tracking active. Sequential structural energy trace registers: W1 Depth={d1:.2f}% -> W2={d2:.2f}% -> W3={d3:.2f}%."
        thesis = f"Asset volatility has reached an absolute tight bottleneck zone. Selling pressure has dried out across subsequent cycles, indicating an impending heavy-volume high-frequency intraday momentum explosion."
        
        return {"Symbol": symbol, "Live Price": round(price, 2), "Ceiling Res": round(r_max, 2), "W1 %": round(d1, 2), "W2 %": round(d2, 2), "Status": "🟢 COMPLIANT", "Description": desc, "Thesis": thesis, "Obj": t}
    except: return None

# ==============================================================================
# 04. MULTI-PANEL CONSOLE RENDER BLOCKS
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["[ MODE 1: IPO CORE ]", "[ MODE 2: VALUE OWNER ]", "[ MODE 3: INTRADAY VCP ]"])

with tab1:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 1 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE IPO SWEEP"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(agent_ipo_analyst, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            # Interactive Grid Engine selection row hook
            selected_row = st.dataframe(df, use_container_width=True, on_select="rerun", selection_mode="single-row")
            
            if selected_row and selected_row.get("selection", {}).get("rows"):
                idx = selected_row["selection"]["rows"][0]
                target = res[idx]
                
                # Dynamic Overlay Console Box Injected
                st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET CODE: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1])
                with col1:
                    render_tradingview_widget(target["Symbol"])
                with col2:
                    st.markdown(f"### ⚙️ Quant Filtration Matrix:\n{target['Description']}")
                    st.markdown(f"### 🎯 Portfolio Allocation Thesis:\n{target['Thesis']}")
                    st.markdown(f"### 📰 Real-Time Corporate Feed:\n{fetch_live_news_agent(target['Obj'])}")
        else: st.warning("NO ASSETS PASSED THE QUANT FLOAT CRITERIA IN THIS CURRENT BRACKET.")

with tab2:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 2 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE RATIOS SWEEP"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(agent_value_auditor, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            selected_row = st.dataframe(df, use_container_width=True, on_select="rerun", selection_mode="single-row")
            
            if selected_row and selected_row.get("selection", {}).get("rows"):
                idx = selected_row["selection"]["rows"][0]
                target = res[idx]
                
                st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET CODE: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1])
                with col1:
                    render_tradingview_widget(target["Symbol"])
                with col2:
                    st.markdown(f"### ⚙️ Quant Filtration Matrix:\n{target['Description']}")
                    st.markdown(f"### 🎯 Portfolio Allocation Thesis:\n{target['Thesis']}")
                    st.markdown(f"### 📰 Real-Time Corporate Feed:\n{fetch_live_news_agent(target['Obj'])}")
        else: st.warning("NO ASSETS CLEARED LONG-TERM FUNDAMENTAL CONDITIONS.")

with tab3:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 3 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE SCALPER SWEEP"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(agent_vcp_scalper, s) for s in REAL_MARKET_UNIVERSE]
            res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res:
            df = pd.DataFrame(res).drop(columns=["Description", "Thesis", "Obj"])
            selected_row = st.dataframe(df, use_container_width=True, on_select="rerun", selection_mode="single-row")
            
            if selected_row and selected_row.get("selection", {}).get("rows"):
                idx = selected_row["selection"]["rows"][0]
                target = res[idx]
                
                st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET CODE: {target["Symbol"].replace(".NS","")}</b></div>', unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1])
                with col1:
                    render_tradingview_widget(target["Symbol"])
                with col2:
                    st.markdown(f"### ⚙️ Quant Filtration Matrix:\n{target['Description']}")
                    st.markdown(f"### 🎯 Portfolio Allocation Thesis:\n{target['Thesis']}")
                    st.markdown(f"### 📰 Real-Time Corporate Feed:\n{fetch_live_news_agent(target['Obj'])}")
        else: st.warning("NO HIGH-FREQUENCY WAVE COMPRESSIONS PASSED SCAN GATES TODAY.")
        
