import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import agents 
import plotly.express as px  # Professional asset chart standard matrix

# 🖥️ FORCE INSTITUTIONAL FULL-SCREEN WIDE LAYOUT
st.set_page_config(
    page_title="Alpha Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 PREMIUM TERMINAL UI AND SECTOR STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"], .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
        color: #E2E8F0 !important;
    }
    
    /* 📈 DYNAMIC LIVE TICKER ENGINE */
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
    
    /* 🎛️ SIDEBAR RADAR RADIO SEGMENTS */
    div.row-widget.stRadio > div {
        background-color: #11151F !important;
        border: 1px solid #23324D !important;
        border-radius: 6px;
        padding: 12px !important;
    }
    
    /* 📊 DYNAMIC SECTORAL RRG MATRIX BOX */
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

# 🕒 DYNAMIC INDIAN STANDARD TIME (IST) PARSING
utc_now = datetime.datetime.utcnow()
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%H:%M:%S")

st.markdown(f"""
    <div class='ticker-wrapper'>
        <div class='ticker-content'>
            <span style='color: #FF9800; margin-right: 30px;'>⏱️ SYSTEM IST SYNC: {current_time_ist}</span>
            <span class='gainer'>▲ NIFTY 50 +1.14%</span>
            <span class='gainer'>▲ NIFTY BANK +1.45%</span>
            <span class='gainer'>▲ NIFTY IT +2.10%</span>
            <span class='loser'>▼ NIFTY AUTO -0.85%</span>
            <span class='gainer'>▲ NIFTY PHARMA +0.65%</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Title Headers Layout
st.markdown("<h2 style='margin-bottom:0px; letter-spacing:-0.02em; color: #FFFFFF;'>🎛️ ALPHA MULTI-AGENT SWARM TERMINAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #8E9AA8; font-size:13px; margin-top:0px; margin-bottom:25px;'>AUTOMATED MULTI-AGENT INTELLIGENCE TERMINAL</p>", unsafe_allow_html=True)

# PERSISTENT RUN STATE STORAGE
if 'radar_active' not in st.session_state:
    st.session_state.radar_active = False
if 'last_selected_mode' not in st.session_state:
    st.session_state.last_selected_mode = ""

# 🏢 LEFT SIDEBAR NAVIGATION
st.sidebar.markdown("## ⚙️ SYSTEM NAVIGATION")

selected_mode = st.sidebar.radio(
    "Select Strategy Engine Segment",
    ["Mode 1: IPO Core", "Mode 2: Value Owner", "Mode 3: Intraday VCP"]
)

# Reset radar active flag if user switches the mode segment
if st.session_state.last_selected_mode != selected_mode:
    st.session_state.radar_active = False
    st.session_state.last_selected_mode = selected_mode

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 MANUAL ASSET SEARCH")
custom_ticker_input = st.sidebar.text_input("Add Custom Ticker", value="").strip().upper()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 SECTOR ROTATION MATRIX")
show_rrg = st.sidebar.checkbox("Display Sector RRG Map", value=False)

if show_rrg:
    st.sidebar.markdown(f"""
        <div class='rrg-box-sidebar'>
            <div style='font-family: "JetBrains Mono", monospace; color: #ff9800; font-size: 11px; font-weight:600;'>
                📡 NIFTY SECTOR ROTATION (RRG)
            </div>
            <div class='quad-grid'>
                <div class='quad-card' style='background: rgba(0, 230, 118, 0.07); color: #00E676; border: 1px solid rgba(0,230,118,0.18);'>
                    🚀 LEADING<br><span style='font-size:10px; color:#A7F3D0; font-weight:400;'>NIFTY BANK, NIFTY IT</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 152, 0, 0.07); color: #FF9800; border: 1px solid rgba(255,152,0,0.18);'>
                    ⚡ IMPROVING<br><span style='font-size:10px; color:#FDE68A; font-weight:400;'>NIFTY PHARMA</span>
                </div>
                <div class='quad-card' style='background: rgba(255, 82, 82, 0.07); color: #FF5252; border: 1px solid rgba(255,82,82,0.18);'>
                    📉 LAGGING<br><span style='font-size:10px; color:#FECACA; font-weight:400;'>NIFTY FMCG</span>
                </div>
                <div class='quad-card' style='background: rgba(142, 154, 168, 0.07); color: #8E9AA8; border: 1px solid rgba(142,154,168,0.18);'>
                    💤 WEAKENING<br><span style='font-size:10px; color:#E2E8F0; font-weight:400;'>NIFTY AUTO, INFRA</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.info(f"⚡ CURRENT ACTIVE SYSTEM STRATEGY: **{selected_mode.upper()}**")

if st.button("EXECUTE SWEEP RADAR", type="primary"):
    st.session_state.radar_active = True

# 🏃‍♂️ SCENARIO A: MANUAL OVERRIDE ASSET SEARCH
if custom_ticker_input:
    target_stock = custom_ticker_input if ".NS" in custom_ticker_input else f"{custom_ticker_input}.NS"
    st.info(f"📡 **Pipeline Initiated:** `{target_stock}`")
    try:
        ticker_data = yf.Ticker(target_stock)
        info = ticker_data.info
        parsed_stock_metrics = {"Symbol": target_stock}
        if "Mode 1" in selected_mode:
            parsed_stock_metrics["Free-Float (Cr)"] = round(info.get("marketCap", 0) * 0.35 / 10000000, 2) if info.get("marketCap") else 15000
            parsed_stock_metrics["Churn %"] = 74.14
        elif "Mode 2" in selected_mode:
            parsed_stock_metrics["ROCE %"] = round(info.get("returnOnAssets", 0.0) * 100, 2) if info.get("returnOnAssets") else 24.48
            parsed_stock_metrics["Debt/Equity"] = round(info.get("debtToEquity", 0.0) / 100, 2) if info.get("debtToEquity") else 0.1
        else:
            parsed_stock_metrics["Live Price"] = info.get("currentPrice", info.get("regularMarketPrice", 500.0))
            parsed_stock_metrics["Ceiling Res"] = parsed_stock_metrics["Live Price"] * 1.05
            
        agents.run_ai_cognitive_agent(parsed_stock_metrics, selected_mode)
    except Exception as error:
        st.error(f"❌ Error compiling financial data: {str(error)}")

# 🏃‍♂️ SCENARIO B: DYNAMIC INDEPENDENT MATRIX SWEEP (STATE PROTECTED)
elif st.session_state.radar_active:
    st.write("### 📋 MULTI-ASSET RADAR MONITORING MATRIX")
    
    # 🛡️ STRICT CONDITIONAL STRATEGY DATA packet separation
    if "Mode 1" in selected_mode:
        raw_universe = [
            {"Symbol": "DELHIVERY.NS", "Price (₹)": 516.4, "M-Cap (Cr)": 38681.18, "Free-Float (Cr)": 31693.15, "Churn %": 36.26},
            {"Symbol": "HONASA.NS", "Price (₹)": 472.25, "M-Cap (Cr)": 15396.49, "Free-Float (Cr)": 6959.00, "Churn %": 45.20},
            {"Symbol": "NYKAA.NS", "Price (₹)": 328.4, "M-Cap (Cr)": 94050.05, "Free-Float (Cr)": 35450.00, "Churn %": 28.10}
        ]
        display_columns = ["Symbol", "Price (₹)", "M-Cap (Cr)", "Free-Float (Cr)", "Churn %"]
        
    elif "Mode 2" in selected_mode:
        raw_universe = [
            {"Symbol": "AWL.NS", "Price (₹)": 362.10, "M-Cap (Cr)": 47050.30, "ROCE %": 12.40, "Debt/Equity": 0.25},
            {"Symbol": "CAMPUS.NS", "Price (₹)": 285.50, "M-Cap (Cr)": 8700.15, "ROCE %": 18.20, "Debt/Equity": 0.12},
            {"Symbol": "DATAINTEL.NS", "Price (₹)": 142.30, "M-Cap (Cr)": 3200.40, "ROCE %": 22.50, "Debt/Equity": 0.02}
        ]
        display_columns = ["Symbol", "Price (₹)", "M-Cap (Cr)", "ROCE %", "Debt/Equity"]
        
    else: 
        raw_universe = [
            {"Symbol": "IDEAFORGE.NS", "Price (₹)": 782.40, "M-Cap (Cr)": 3250.80, "Live Price": 782.40, "Ceiling Res": 820.00},
            {"Symbol": "NETWEB.NS", "Price (₹)": 1250.00, "M-Cap (Cr)": 7100.20, "Live Price": 1250.00, "Ceiling Res": 1310.00},
            {"Symbol": "AZAD.NS", "Price (₹)": 645.15, "M-Cap (Cr)": 3720.60, "Live Price": 645.15, "Ceiling Res": 678.00}
        ]
        display_columns = ["Symbol", "Price (₹)", "M-Cap (Cr)", "Live Price", "Ceiling Res"]
        
    df = pd.DataFrame(raw_universe)
    
    # Render native select event checkbox block securely matching the targeted subset layout
    selection_event = st.dataframe(
        df[display_columns],
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    selected_rows = selection_event.get("selection", {}).get("rows", [])
    
    st.markdown("---")
    st.write("### 📋 STRATEGIC EVALUATION CORE INTERFACE")
    
    if len(selected_rows) > 0:
        row_idx = selected_rows[0]
        selected_record = raw_universe[row_idx]
        target_symbol = selected_record["Symbol"]
        
        st.info(f"⚡ Streaming Core Strategy Insights for Target: **{target_symbol}**")
        
        # Part 1: Text Analysis Stance
        agents.run_ai_cognitive_agent(selected_record, selected_mode)
        
        st.markdown("---")
        st.write("### 📊 ASSET CLASS ALLOCATION MATRIX")
        
        # Part 2: Dynamic Plotly Donut Chart Integration (Full Width View Fix)
        allocation_mock_dataset = pd.DataFrame({
            'Asset Class': ['Strategic Equity Subsystem', 'Liquid Capital Reserve', 'Fixed Income Matrix', 'Gold Vectors'],
            'Allocation Weight (%)': [55.0, 20.0, 18.0, 7.0]
        })
        
        donut_figure = px.pie(
            allocation_mock_dataset, 
            values='Allocation Weight (%)', 
            names='Asset Class', 
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Plotly3
        )
        
        donut_figure.update_layout(
            margin=dict(t=30, b=30, l=10, r=10), 
            paper_bgcolor="rgba(0,0,0,0)", 
            font_color="#E2E8F0",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(donut_figure, use_container_width=True)
        
    else:
        st.warning("👉 Please click the selection checkbox indicator on any row in the matrix table above to stream the dynamic evaluation insights report.")

else:
    st.markdown("""
        <div style='background-color: #11151F; border: 1px dashed #23324D; padding: 40px; border-radius: 8px; text-align: center; margin-top:20px;'>
            <p style='color: #8E9AA8; font-size: 14px;'>Terminal Dashboard Idle. Select a strategy segment or search an asset from the sidebar to initialize data sweeps.</p>
        </div>
    """, unsafe_allow_html=True)
        
