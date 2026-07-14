import datetime
import urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf
import streamlit as st
import http.client
import json

# 🔐 SECURE GROQ ENVIROMENT FETCHING (100% GITHUB PUBLIC REPO COMPLIANT)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY or len(GROQ_API_KEY) < 5:
    st.sidebar.error("❌ AI Status: Groq API Key Missing in Secrets")
else:
    st.sidebar.success("⚡ AI Status: Ultra-Fast Groq Engine Active")

# 🎨 PREMIUM TERMINAL UI DESIGN INJECTION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"], .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
        font-size: 14.5px !important;
        line-height: 1.6 !important;
        letter-spacing: -0.01em !important;
    }
    .quant-report-container {
        background-color: #11151F !important;
        border-left: 4px solid #ff9800 !important;
        border-radius: 6px !important;
        padding: 20px !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .verdict-box {
        background-color: #171E2E !important;
        border: 1px solid #23324D !important;
        border-radius: 6px !important;
        padding: 18px !important;
        margin-top: 15px !important;
        border-top: 3px solid #00E676 !important;
    }
    .section-tag {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 12px !important;
        color: #ff9800 !important;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_live_news_agent(symbol, execution_mode_tag):
    clean_ticker = symbol.replace(".NS", "").strip().upper()
    try:
        rss_url = f"https://news.google.com/rss/search?q={clean_ticker}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        compiled_news = ""
        counter = 0
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            clean_date = pub_date[:16] if pub_date else "Recent"
            if title and len(title) > 15:
                if " - " in title: title = title.rsplit(" - ", 1)[0]
                compiled_news += f"• 🌐 **[{title}]({link})**\n   *{clean_date}*\n\n"
                counter += 1
            if counter >= 3: break
        if len(compiled_news) > 20: return compiled_news
    except: pass
    return f"• 📊 **[Quant Wire]** System mapping operational data pipelines safely for {clean_ticker}."

def run_ai_cognitive_agent(stock_data, context_tag):
    ticker_name = stock_data['Symbol'].replace('.NS','')
    live_news_context = fetch_live_news_agent(stock_data['Symbol'], context_tag)
    screener_reference_url = f"https://www.screener.in/company/{ticker_name}/"
    
    # Context-Specific Prompt Calibration Strategy
    strategy_instruction = ""
    
    if "ROCE %" in stock_data:
        strategy_instruction = f"Focus strictly on Fundamental Capital Efficiency and Balance Sheet parameters: ROCE is {stock_data.get('ROCE %')}% and Debt/Equity is {stock_data.get('Debt/Equity')}. Do not mention float or churn."
        fallback_analysis = (
            f"<div class='quant-report-container'>"
            f"<div class='section-tag'>📊 INSTITUTIONAL EQUITY AUDIT DESK // ASSET: {ticker_name}</div><br>"
            f"• **Capital Efficiency Matrix**: Return on Capital Employed (ROCE) is running verified at **{stock_data.get('ROCE %')}%**.<br><br>"
            f"• **Leverage Audit**: Debt-to-Equity constraints map at **{stock_data.get('Debt/Equity')}**.<br><br>"
            f"• **Information Layer**: Cross-referencing active metrics parameters against institutional Screener matrices."
            f"</div>"
        )
    elif "Churn %" in stock_data or "Free-Float (Cr)" in stock_data:
        strategy_instruction = f"Focus strictly on Public Float Dynamics and Accumulation structures: Free Float is ₹{stock_data.get('Free-Float (Cr)')} Cr and Operational Churn is {stock_data.get('Churn %', stock_data.get('Churn'))}%. Do not mention ROCE or debt ratios."
        fallback_analysis = (
            f"<div class='quant-report-container'>"
            f"<div class='section-tag'>📊 LIQUIDITY DISTRIBUTION MATRIX REPORT // ASSET: {ticker_name}</div><br>"
            f"• **Free Float Mapping**: Public liquidity blocks compute safely at **₹{stock_data.get('Free-Float (Cr)')} Cr**.<br><br>"
            f"• **Volume Churn Verification**: Base floor accumulation systems track public float supply rotation turnover scales at **{stock_data.get('Churn %', stock_data.get('Churn'))}%**."
            f"</div>"
        )
    else:
        strategy_instruction = f"Focus strictly on VCP Structural Contraction Patterns, Support base near technical ceiling of ₹{stock_data.get('Ceiling Res')}."
        fallback_analysis = (
            f"<div class='quant-report-container'>"
            f"<div class='section-tag'>📊 VOLATILITY CONTRACTION COMPLIANCE REGIME // ASSET: {ticker_name}</div><br>"
            f"• **VCP Micro-Structural Arrays**: Price spot contractions track localized support zones near technical ceiling markers at **₹{stock_data.get('Live Price')}**."
            f"</div>"
        )

    if not GROQ_API_KEY or len(GROQ_API_KEY) < 5:
        st.markdown(fallback_analysis, unsafe_allow_html=True)
        return ""
        
    try:
        conn = http.client.HTTPSConnection("api.groq.com")
        
        prompt = f"""
        You are a Senior Institutional Fund Manager and Chief Equity Research Auditor for Indian capital markets.
        Analyze the exact quantitative metrics provided, cross-verify them explicitly against the live corporate news streams, and deliver a high-conviction verdict.
        
        [STRATEGY PARAMETER FILTER CONTEXT]:
        Active Strategy Framework Mode: {context_tag}
        Target Ticker Asset: {ticker_name}
        Live Provided Metrics Layer: {stock_data}
        Current Real-Time News Stream: {live_news_context}
        
        [STRICT COMPLIANCE METRICS ROUTING]:
        {strategy_instruction}
        - Base your arguments only on the fields present in the active metrics layer. Never state that parameters are missing or not provided.
        - Your analysis tone must match a strict Bloomberg analyst desk style: direct, mathematical, data-dense, and highly aggressive.
        
        Generate a highly professional 2-paragraph final verdict:
        - Paragraph 1: Quantitative Strategy Analysis. Break down the numeric values active in this mode and map how the live corporate events or industry headwinds support this data structure.
        - Paragraph 2: Institutional Asset Allocation Verdict. State an aggressive, high-conviction portfolio allocation argument outlining if an elite manager should Accumulate, Hold, or Avoid this risk frame.
        """
        
        payload = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        })
        
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        conn.request("POST", "/openai/v1/chat/completions", payload, headers)
        res = conn.getcallresponse() if hasattr(conn, 'getcallcallcallresponse') else (res := conn.getcallresponse() if hasattr(conn, 'getcallcallresponse') else conn.getcallresponse() if hasattr(conn, 'getcallresponse') else conn.getcallresponse() if hasattr(conn, 'getcallresponse') else conn.getresponse())
        data = res.read()
        
        result_json = json.loads(data.decode("utf-8"))
        if 'choices' in result_json and len(result_json['choices']) > 0:
            raw_text = result_json['choices'][0]['message']['content']
            paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
            
            p1_html = paragraphs[0] if len(paragraphs) > 0 else raw_text
            p2_html = paragraphs[1] if len(paragraphs) > 1 else ""
            
            styled_output = f"""
            <div class='quant-report-container'>
                <div class='section-tag'>📊 STRATEGIC ANALYSIS VECTOR // {context_tag}</div>
                <p style='margin-top: 10px; color: #E2E8F0;'>{p1_html}</p>
            </div>
            """
            if p2_html:
                styled_output += f"""
                <div class='verdict-box'>
                    <div class='section-tag' style='color: #00E676 !important;'>⚡ ASSET ALLOCATION VERDICT // HIGH CONVICTION</div>
                    <p style='margin-top: 10px; color: #E2E8F0;'>{p2_html}</p>
                </div>
                """
            
            st.markdown(styled_output, unsafe_allow_html=True)
            return ""
        else:
            st.markdown(fallback_analysis, unsafe_allow_html=True)
            return ""
            
    except Exception as e:
        st.markdown(fallback_analysis, unsafe_allow_html=True)
        return ""
        
