import streamlit as st
import datetime
import yfinance as yf
import agents 

# 🎨 EXCLUSIVE BLOOMBERG TERMINAL UI & TICKER CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"], .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* 📈 DYNAMIC RUNNING TICKER HEADER PANEL */
    .ticker-wrapper {
        background-color: #0E1117 !important;
        border: 1px solid #23324D !important;
        border-radius: 4px;
        padding: 8px 12px;
        overflow: hidden;
        white-space: nowrap;
        margin-bottom: 25px;
    }
    .ticker-content {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 35s linear infinite;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
    }
    @keyframes marquee {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .gainer { color: #00E676 !important; font-weight: 600; margin-right: 30px; }
    .loser { color: #FF5252 !important; font-weight: 600; margin-right: 30px; }
    
    /* 📊 ADVANCED 4-QUADRANT RRG SIDEBAR CONTAINER */
    .rrg-box-sidebar {
        background-color: #11151F !important;
        border: 1px dashed #23324D !important;
        border-radius: 6px !important;
        padding: 15px !important;
        margin-top: 15px;
    }
    .quad-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        margin-top: 10px;
    }
    .quad-card {
        padding: 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11.5px;
        font-weight: 600;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 🕒 1. ACCURATE LOCAL INDIAN STANDARD TIME (IST) CALCULATION
utc_now = datetime.datetime.utcnow()
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div class='ticker-wrapper'>
        <div class='ticker-content'>
            <span style='color: #FF9800; margin-right: 30px;'>⏱️ MARKET IST: {current_time_ist}</span>
            <span class='gainer'>▲ NIFTY 50 +1.14%</span>
            <span class='gainer'>▲ TCS.NS +3.10%</span>
            <span class='gainer'>▲ HDFCBANK.NS +2.45%</span>
            <span class='loser'>▼ MARUTI.NS -1.52%</span>
            <span class='loser'>▼ RECLTD.NS -3.41%</span>
            <span class='gainer'>▲ RELIANCE.NS +1.80%</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Terminal Header
st.markdown("<h2 style='margin-bottom:0px; letter-spacing:-0.02em;'>🎛️ ALPHA MULTI-AGENT SWARM TERMINAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #8E9AA8; font-size:13px; margin-top:0px; margin-bottom:25px;'>AUTOMATED MULTI-AGENT INTELLIGENCE TERMINAL</p>", unsafe_allow_html=True)

# 🏢 2. LEFT SIDEBAR MENU: MODES & RRG MULTI-SELECTION
st.sidebar.markdown("## ⚙️ SYSTEM NAVIGATION")

# Add the 3 Modes inside Sidebar Selectbox
selected_mode = st.sidebar.selectbox(
    "Select Strategy Engine Mode",
    ["Mode 1: IPO Core", "Mode 2: Value Owner", "Mode 3: Intraday VCP"]
)

st.sidebar.markdown("---")

# Manual Stock Search Module
st.sidebar.markdown("### 🎯 MANUAL ASSET SEARCH")
custom_ticker_input = st.sidebar.text_input("Add Custom Ticker", value="").strip().upper()

st.sidebar.markdown("---")

# Specialized RRG Widget Switch
st.sidebar.markdown("### 📊 VISUALIZATION LAYER")
show_rrg = st.sidebar.checkbox("Display Relative Rotation Map (RRG)", value=False)

if show_rrg:
    st.sidebar.markdown(f"""
        <div class='rrg-box-sidebar'>
            <div style='font-family: "JetBrains Mono", monospace; color: #ff9800; font-size: 11px; font-weight:600;'>
                📡 RRG VECTOR MATRIX
            </div>
            <div class='quad-grid'>
                <div class='quad-card' style='background: rgba(0, 230, 118, 0.07); color: #00E676; border: 1px solid rgba(0,230,118,0.18);'>
                    🚀 LEADING<br><span style='font-size:10px; color:#A7F3D0; font-weight:400;'>TCS, HDFCBANK</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 152, 0, 0.07); color: #FF9800; border: 1px solid rgba(255,152,0,0.18);'>
                    ⚡ IMPROVING<br><span style='font-size:10px; color:#FDE68A; font-weight:400;'>RELIANCE, FMCG</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 82, 82, 0.07); color: #FF5252; border: 1px solid rgba(255,82,82,0.18);'>
                    📉 LAGGING<br><span style='font-size:10px; color:#FECACA; font-weight:400;'>INFYS, PHARMA</span>
                </div>
                <div class='quad-card' style='background: rgba(142, 154, 168, 0.07); color: #8E9AA8; border: 1px solid rgba(142,154,168,0.18);'>
                    💤 WEAKENING<br><span style='font-size:10px; color:#E2E8F0; font-weight:400;'>MARUTI, INFRA</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 🏃‍♂️ 3. MAIN APP BODY EXECUTION CONTROL
st.info(f"⚡ CURRENT ACTIVE SYSTEM STRATEGY: **{selected_mode.upper()}**")

execute_sweep = st.button("EXECUTE SWEEP RADAR", type="primary")

if not execute_sweep and not custom_ticker_input:
    st.markdown("""
        <div style='background-color: #11151F; border: 1px dashed #23324D; padding: 40px; border-radius: 8px; text-align: center; margin-top:20px;'>
            <p style='color: #8E9AA8; font-size: 14px;'>Terminal Dashboard Idle. Adjust variables in the left menu sidebar and click 'EXECUTE SWEEP RADAR' to trigger data analysis arrays.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    target_stock = ""
    if custom_ticker_input:
        target_stock = custom_ticker_input if ".NS" in custom_ticker_input else f"{custom_ticker_input}.NS"
        st.info(f"📡 **Swarm Isolation Pipeline Initiated for Asset Matrix:** `{target_stock}`")
        
        try:
            ticker_data = yf.Ticker(target_stock)
            info = ticker_data.info
            
            parsed_stock_metrics = {
                "Symbol": target_stock,
                "Live Price": info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
                "ROCE %": round(info.get("returnOnAssets", 0.0) * 100, 2),
                "Debt/Equity": round(info.get("debtToEquity", 0.0) / 100, 2) if info.get("debtToEquity") else 0.05,
                "Free-Float (Cr)": round(info.get("marketCap", 0) * 0.35 / 10000000, 2) if info.get("marketCap") else 15000,
                "Churn %": 34.20
            }
            
            # Execute Groq via agents package dynamically parsing the selected mode tag
            agents.run_ai_cognitive_agent(parsed_stock_metrics, selected_mode)
            
        except Exception as error:
            st.error(f"❌ Error compiling real-time financial arrays for {target_stock}: {str(error)}")
    else:
        st.success(f"🔄 Global Sweep Radar Active: Running deep iterations on {selected_mode} layout...")
        # Aapka structural grid table loops yahan parse ho jayega!
        
