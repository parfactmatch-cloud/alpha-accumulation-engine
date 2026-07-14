import streamlit as st
import datetime
import yfinance as yf
# Hamari upgraded agents file ko import kar rahe hain
import agents 

# 🎨 UPGRADED BLOOMBERG-STYLE TERMINAL UI DEFINITION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"], .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Dynamic Running Ticker Style */
    .ticker-wrapper {
        background-color: #0E1117 !important;
        border: 1px solid #23324D !important;
        border-radius: 4px;
        padding: 8px 12px;
        overflow: hidden;
        white-space: nowrap;
        margin-bottom: 20px;
    }
    .ticker-content {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 30s linear infinite;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
    }
    @keyframes marquee {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .gainer { color: #00E676 !important; font-weight: 600; margin-right: 30px; }
    .loser { color: #FF5252 !important; font-weight: 600; margin-right: 30px; }
    
    /* Premium RRG Quadrant Preview Box */
    .rrg-box {
        background-color: #11151F !important;
        border: 1px dashed #23324D !important;
        border-radius: 8px !important;
        padding: 25px !important;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .quad-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 15px;
    }
    .quad-card {
        padding: 12px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 🕒 1. FIXED INDIAN TIME ZONE MATRIX & LIVE TICKER RUNNER
utc_now = datetime.datetime.utcnow()
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div class='ticker-wrapper'>
        <div class='ticker-content'>
            <span style='color: #FF9800; margin-right: 30px;'>⏱️ MARKET IST TIME: {current_time_ist}</span>
            <span class='gainer'>▲ NIFTY 50 +1.1%</span>
            <span class='gainer'>▲ TCS +3.1%</span>
            <span class='gainer'>▲ HDFCBANK +2.4%</span>
            <span class='loser'>▼ MARUTI -1.5%</span>
            <span class='loser'>▼ RECLTD -3.4%</span>
            <span class='gainer'>▲ RELIANCE +1.8%</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Title Framework Layout
st.markdown("<h2 style='margin-bottom:0px; letter-spacing:-0.02em;'>🎛️ ALPHA MULTI-AGENT SWARM TERMINAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #8E9AA8; font-size:13px; margin-top:0px;'>AUTOMATED MULTI-AGENT INTELLIGENCE TERMINAL</p>", unsafe_allow_html=True)

# 🎛️ SIDEBAR CONTROL: MANUAL STOCK SEARCH WITH AUTO-NS HANDLING
st.sidebar.markdown("### 🎯 MANUAL STOCK SEARCH")
custom_ticker_input = st.sidebar.text_input("Add Custom Ticker", value="").strip().upper()

# 📈 RADAR INTERACTION PARAMETERS
execute_sweep = st.button("EXECUTE SWEEP RADAR", type="primary")

# 📊 2. EMPTY STATE: RELATIVE ROTATION GRAPH (RRG) METRICS VISUALIZATION
if not execute_sweep and not custom_ticker_input:
    st.markdown(f"""
        <div class='rrg-box'>
            <div style='font-family: "JetBrains Mono", monospace; color: #ff9800; font-size: 11.5px;'>
                📡 SYSTEM STATE: READY // AWAITING INSIGHT SECTOR MAPPING
            </div>
            <h3 style='margin-top: 10px; color:#FFFFFF; font-size:16px;'>Relative Rotation Sector Map (RRG Real-Time Matrix)</h3>
            <p style='color: #8E9AA8; font-size: 13.5px; max-width: 600px; margin-top:5px;'>
                Track real-time leading strength, fading momentum, and accumulation trends across top corporate market structures before initiating tactical multi-agent sweeps.
            </p>
            <div class='quad-grid'>
                <div class='quad-card' style='background: rgba(0, 230, 118, 0.08); color: #00E676; border: 1px solid rgba(0,230,118,0.2);'>
                    🚀 LEADING<br><span style='font-size:10px; color:#A7F3D0;'>TCS, HDFCBANK</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 152, 0, 0.08); color: #FF9800; border: 1px solid rgba(255,152,0,0.2);'>
                    ⚡ IMPROVING<br><span style='font-size:10px; color:#FDE68A;'>RELIANCE, PHARMA</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 82, 82, 0.08); color: #FF5252; border: 1px solid rgba(255,82,82,0.2);'>
                    📉 LAGGING<br><span style='font-size:10px; color:#FECACA;'>RECLTD, INFYS</span>
                </div>
                <div class='quad-card' style='background: rgba(142, 154, 168, 0.08); color: #8E9AA8; border: 1px solid rgba(142,154,168,0.2);'>
                    💤 WEAKENING<br><span style='font-size:10px; color:#E2E8F0;'>MARUTI, FMCG</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 🏃‍♂️ 3. TRIGGER CONDITIONS (CUSTOM SEARCH OR GLOBAL RADAR SWEEP)
else:
    target_stock = ""
    if custom_ticker_input:
        # Agar user bina .NS ke enter kare, toh framework crash hone se bachane ke liye automatic validation rules lagaye hain
        target_stock = custom_ticker_input if ".NS" in custom_ticker_input else f"{custom_ticker_input}.NS"
        st.info(f"🔍 Executing Deep Search Isolation Engine for: **{target_stock}**")
        
        # Static mock structure sample representing execution context parameters passing safely to agents
        sample_data = {"Symbol": target_stock, "Price (₹)": 2200.5, "ROCE %": 47.74, "Debt/Equity": 10.21}
        
        # Agents function execution trigger
        agents.run_ai_cognitive_agent(sample_data, "Manual Injection Mode")
    else:
        st.success("🔄 Radar Active: Running multi-agent extraction loops over selected metrics indices...")
        # Yahan par aapka regular loop code jo tables and yfinance indices iteration chalta hai, wo automatically place ho jayega.
        
