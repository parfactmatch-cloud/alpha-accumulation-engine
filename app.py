import concurrent.futures
import datetime
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Import modular blocks from separate file code execution sheet
from agents import (
    agent_ipo_analyst, 
    agent_value_auditor, 
    agent_vcp_scalper, 
    run_ai_cognitive_agent, 
    fetch_live_news_agent
)

# ==============================================================================
# THEME CONFIGURATION SETUP
# ==============================================================================
st.set_page_config(page_title="ALPHA AI QUANT TERMINAL", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    .stApp { background-color: #0b0c10 !important; font-family: 'Roboto Mono', monospace !important; color: #d1d4dc !important; }
    .terminal-nav { background-color: #141823; border-bottom: 2px solid #ff9800; padding: 8px 15px; font-size: 11px; color: #8f929d; margin-bottom: 20px; display: flex; gap: 20px; }
    .terminal-nav span { color: #ff9800; font-weight: bold; }
    .bb-widget { background-color: #121620 !important; border: 1px solid #242b35 !important; border-radius: 4px !important; padding: 15px !important; margin-bottom: 15px !important; }
    .bb-header { color: #ff9800 !important; font-size: 13px !important; font-weight: bold !important; text-transform: uppercase; border-bottom: 1px solid #242b35; padding-bottom: 6px; margin-bottom: 12px; letter-spacing: 1px; }
    div[data-testid="stSidebar"] { background-color: #121620 !important; border-right: 1px solid #242b35 !important; }
    .stButton>button { background-color: #ff9800 !important; color: #0b0c10 !important; font-family: 'Roboto Mono', monospace !important; font-weight: bold !important; font-size: 12px !important; border: none !important; border-radius: 2px !important; padding: 8px 0px !important; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button:hover { background-color: #e08600 !important; box-shadow: 0 0 8px rgba(255,152,0,0.4); }
    .console-box { background-color: #141923; border-left: 4px solid #ff9800; border-top: 1px solid #242b35; border-right: 1px solid #242b35; border-bottom: 1px solid #242b35; border-radius: 4px; padding: 20px; margin-top: 25px; }
    h3 { color: #ff9800 !important; font-size: 14px !important; font-weight: bold !important; margin-top: 15px !important; border-bottom: 1px solid #242b35; padding-bottom: 5px; }
    .report-link { display: inline-block; background-color: #171d28; border: 1px solid #ff980088; color: #ff9800 !important; padding: 6px 12px; border-radius: 2px; text-decoration: none; font-weight: bold; font-size: 12px; margin-top: 5px; }
    .report-link:hover { background-color: #ff9800; color: #0b0c10 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="terminal-nav"><span>&lt;GO&gt; MODULAR ENGINE DISPATCHED</span> | UNIVERSE: NIFTY 250 OPTIMIZED | <span>TIME: {datetime.datetime.now().strftime("%H:%M:%S")}</span></div>', unsafe_allow_html=True)
st.title("🎛️ ALPHA MULTI-AGENT SWARM TERMINAL")
st.caption("AUTOMATED MULTI-AGENT INTELLIGENCE TERMINAL")

# ==============================================================================
# SIDEBAR GATEWAYS
# ==============================================================================
st.sidebar.markdown("<h3 style='color:#ff9800; font-size:14px;'>🔑 GEMINI AI PRO GATEWAY</h3>", unsafe_allow_html=True)
GEMINI_API_KEY = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.markdown("<h3 style='color:#ff9800; font-size:14px;'>🎯 MANUAL STOCK OVERRIDE</h3>", unsafe_allow_html=True)
MANUAL_INPUT = st.sidebar.text_input("Add Custom Ticker", "").strip().upper()

st.sidebar.markdown("<h3 style='color:#ff9800; font-size:14px;'>⚙️ CONFIGURATION</h3>", unsafe_allow_html=True)
MIN_MARKET_CAP_CR = st.sidebar.number_input("MIN MCAP GATE (CR)", value=1000)
MAX_IPO_AGE_YEARS = st.sidebar.slider("MAX IPO AGE WINDOW", 1, 10, 7)
TARGET_ABSORPTION_PCT = st.sidebar.slider("TARGET FLOAT CHURN (%)", 10, 100, 30)

BASE_UNIVERSE = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS", "INFY.NS", "SBI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "PAYTM.NS", "ZOMATO.NS", "AWL.NS", "DELHIVERY.NS", "NYKAA.NS", "HONASA.NS", "IRFC.NS", "RVNL.NS", "PFC.NS", "RECLTD.NS", "CONCOR.NS", "HAL.NS", "BEL.NS", "BHEL.NS", "SAIL.NS", "NMDC.NS", "PNB.NS", "UNIONBANK.NS", "CANBK.NS", "BOB.NS", "IDFCFIRSTB.NS", "FEDERALBNK.NS", "BANDHANBNK.NS", "YESBANK.NS", "AUSMALL.NS", "POLYCAB.NS", "KEI.NS", "HAVELLS.NS", "VOLTAS.NS", "DIXON.NS", "AMBER.NS", "ASTRAL.NS", "SUPREMEIND.NS", "FINPIPE.NS", "BERGEPAINT.NS", "KANSAINER.NS", "PIDILITIND.NS", "SRF.NS", "BALRAMCHIN.NS", "TEJASNET.NS", "ANGELONE.NS", "BSE.NS", "CDSL.NS", "CAMS.NS"]

if MANUAL_INPUT:
    formatted_manual = MANUAL_INPUT if MANUAL_INPUT.endswith(".NS") else f"{MANUAL_INPUT}.NS"
    if formatted_manual not in BASE_UNIVERSE: BASE_UNIVERSE.insert(0, formatted_manual)

def render_tradingview_widget(symbol):
    clean_ticker = symbol.replace(".NS", "").replace(".BO", "").strip().upper()
    tv_url = f"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_quant&symbol=NSE%3A{clean_ticker}&interval=D&symboledit=0&saveimage=0&toolbarbg=f1f3f6&theme=dark&style=1&timezone=Asia%2FKolkata"
    components.iframe(tv_url, height=480, scrolling=False)

tab1, tab2, tab3 = st.tabs(["[ MODE 1: IPO CORE ]", "[ MODE 2: VALUE OWNER ]", "[ MODE 3: INTRADAY VCP ]"])

with tab1:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 1 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE IPO SWEEP", key="btn_m1"):
        with st.spinner("Processing..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_ipo_analyst, s, MAX_IPO_AGE_YEARS, MIN_MARKET_CAP_CR, TARGET_ABSORPTION_PCT) for s in BASE_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res: st.session_state["res_m1"], st.session_state["df_m1"] = res, pd.DataFrame(res).drop(columns=["Description"])
            
    if "df_m1" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m1"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m1")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            target = st.session_state["res_m1"][selected_row["selection"]["rows"][0]]
            clean_name = target["Symbol"].replace(".NS","")
            
            st.markdown(f'<div class="console-box"> 📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {clean_name}</b></div>', unsafe_allow_html=True)
            c1, c2 = st.columns([1.3, 1])
            with c1: render_tradingview_widget(target["Symbol"])
            with c2:
                st.markdown(f"### 🤖 Live AI Pro Forecast Matrix ({clean_name}):")
                with st.spinner("AI parsing..."): st.markdown(run_ai_cognitive_agent(target, "IPO Turnaround Layer", GEMINI_API_KEY))
                st.markdown(f"### 📁 Institutional Reports ({clean_name}):\n<a href='https://www.screener.in/company/{clean_name}/documents/' target='_blank' class='report-link'>📂 Open Screener.in Documents Tab ↗</a>", unsafe_allow_html=True)
                st.markdown(f"### 📰 Real-Time Corporate News:\n{fetch_live_news_agent(target['Symbol'], 'IPO')}")

with tab2:
    st.markdown('<div class="bb-widget"><div class="bb-header">MODE 2 ENGINE LAYER // ON-DEMAND CONTROL</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE RATIOS SWEEP", key="btn_m2"):
        with st.spinner("Processing..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_value_auditor, s, MIN_MARKET_CAP_CR) for s in BASE_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res: st.session_state["res_m2"], st.session_state["df_m2"] = res, pd.DataFrame(res).drop(columns=["Description"])
            
    if "df_m2" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m2"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m2")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            target = st.session_state["res_m2"][selected_row["selection"]["rows"][0]]
            clean_name = target["Symbol"].replace(".NS","")
            
            st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {clean_name}</b></div>', unsafe_allow_html=True)
            c1, c2 = st.columns([1.3, 1])
            with c1: render_tradingview_widget(target["Symbol"])
            with c2:
                st.markdown(f"### 🤖 Live AI Pro Forecast Matrix ({clean_name}):")
                with st.spinner("AI parsing..."): st.markdown(run_ai_cognitive_agent(target, "Long-Term Moats", GEMINI_API_KEY))
                st.markdown(f"### 📁 Institutional Reports ({clean_name}):\n<a href='https://www.screener.in/company/{clean_name}/documents/' target='_blank' class='report-link'>📂 Open Screener.in Documents Tab ↗</a>", unsafe_allow_html=True)
                st.markdown(f"### 📰 Real-Time Corporate News:\n{fetch_live_news_agent(target['Symbol'], 'VALUE')}")

with tab3:
    st.markdown('<div class="bb-widget"><div class="bb-header">VOLATILITY COMPRESSION MOVERS // MODE 3 LIVE SCREEN</div></div>', unsafe_allow_html=True)
    if st.button("EXECUTE SCALPER SWEEP", key="btn_m3"):
        with st.spinner("Processing..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                futures = [ex.submit(agent_vcp_scalper, s) for s in BASE_UNIVERSE]
                res = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
        if res: st.session_state["res_m3"], st.session_state["df_m3"] = res, pd.DataFrame(res).drop(columns=["Description"])
            
    if "df_m3" in st.session_state:
        selected_row = st.dataframe(st.session_state["df_m3"], use_container_width=True, on_select="rerun", selection_mode="single-row", key="grid_m3")
        if selected_row and selected_row.get("selection", {}).get("rows"):
            target = st.session_state["res_m3"][selected_row["selection"]["rows"][0]]
            clean_name = target["Symbol"].replace(".NS","")
            
            st.markdown(f'<div class="console-box">📊 <b style="color:#ff9800;">UNIFIED INTELLIGENCE PANEL // ASSET: {clean_name}</b></div>', unsafe_allow_html=True)
            c1, c2 = st.columns([1.3, 1])
            with c1: render_tradingview_widget(target["Symbol"])
            with c2:
                st.markdown(f"### 🤖 Live AI Pro Forecast Matrix ({clean_name}):")
                with st.spinner("AI parsing..."): st.markdown(run_ai_cognitive_agent(target, "VCP Bottleneck", GEMINI_API_KEY))
                st.markdown(f"### 📁 Institutional Reports ({clean_name}):\n<a href='https://www.screener.in/company/{clean_name}/documents/' target='_blank' class='report-link'>📂 Open Screener.in Documents Tab ↗</a>", unsafe_allow_html=True)
                st.markdown(f"### 📰 Real-Time Corporate News:\n{fetch_live_news_agent(target['Symbol'], 'VCP')}")
                
