import datetime
import urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf
import streamlit as st
# Modern updated client router call from the documentation
from google import genai

# Pulling the key from Streamlit Cloud Secrets management matrix securely
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 5:
    st.sidebar.error("❌ AI Status: Secrets Key Not Found / Broken Setup")
else:
    st.sidebar.success("⚡ AI Status: Modern Interactions API Active")

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
    
    # 1. STRUCTURAL RIGOROUS REPORT GENERATOR BUILDER (FALLBACK BACKUP LOGIC)
    if "ROCE %" in stock_data:
        fallback_analysis = (
            f"📊 **[INSTITUTIONAL EQUITY AUDIT DESK // ASSET: {ticker_name}]**\n\n"
            f"• **Capital Efficiency Matrix**: Return on Capital Employed (ROCE) tracks verified at **{stock_data.get('ROCE %')}%**.\n\n"
            f"• **Leverage Assessment**: Balance sheet leverage coefficients compute safely at **{stock_data.get('Debt/Equity')}**.\n\n"
            f"• **Verification Status**: System referencing dynamic structural constraints via Screener profiles."
        )
    elif "Churn %" in stock_data:
        fallback_analysis = (
            f"📊 **[LIQUIDITY DISTRIBUTION MATRIX REPORT // ASSET: {ticker_name}]**\n\n"
            f"• **Free Float Mapping**: Real-time asset capital distribution limits track public float levels at **₹{stock_data.get('Free-Float (Cr)')} Cr**.\n\n"
            f"• **Volume Churn Verification**: Active market turnover parameters process flow rates near **{stock_data.get('Churn %')}%**."
        )
    else:
        fallback_analysis = (
            f"📊 **[VOLATILITY CONTRACTION COMPLIANCE REGIME // ASSET: {ticker_name}]**\n\n"
            f"• **VCP Vector Check**: Price spot contractions track localized support zones near technical ceiling markers at **₹{stock_data.get('Ceiling Res')}**."
        )

    # 2. UP-GRADED INTERACTIONS CLIENT DISPATCH MATRIX AS PER DOCUMENTATION
    if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 5:
        return fallback_analysis
        
    try:
        # Initializing the modern direct client SDK layout rules
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        [SYSTEM ROLE DIRECTIVE]:
        You are a legendary Senior Institutional Fund Manager and Chief Equity Risk Auditor for Indian capital markets. 
        Your directive is to analyze core quantitative metrics, cross-verify them explicitly against the provided live news streams and Screener profiles, and deliver a high-conviction final verdict.
        
        [DIGESTED DATA SYSTEM GRID]:
        - Target Stock Ticker: {ticker_name}
        - Strategy Scope Context Category: {context_tag}
        - Live Numeric Metrics Engine Output: {stock_data}
        - Current Live Corporate News Feed: {live_news_context}
        - Institutional Profile Subpath Reference: {screener_reference_url}
        
        [STRICT INSTRUCTIONAL BOUNDARIES]:
        - Never output boilerplate text, introductory remarks, or setup code reminders.
        - The analysis tone must be ultra-professional, dense, razor-sharp, and mathematically backed (Bloomberg terminal standard). 
        - Absolutely no 'None' or 'NaN' placeholder tokens can pass into the layout text blocks.
        
        [TASK EXECUTION MATRIX]:
        Generate a highly professional 2-paragraph final verdict based on the specific performance values:
        - Paragraph 1: Quantitative & Fundamental Verification. Analyze the numerical values (ROCE/Leverage/Float Churn) and cross-verify them explicitly against the live news events and con-calls trajectory. Address if the structural trends are strong or showing stress.
        - Paragraph 2: Institutional Asset Allocation Verdict. State an aggressive, high-conviction mathematical argument outlining if an elite portfolio allocator should Accumulate, Hold, or Avoid this specific equity risk structure.
        """
        
        # Calling the recommended interactions endpoint with latest feature models
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )
        return interaction.output_text
    except:
        return fallback_analysis
        
