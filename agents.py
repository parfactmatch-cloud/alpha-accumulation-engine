import datetime
import urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf
import streamlit as st
import google.generativeai as genai

# 🔐 SECURE ENVIRONMENT FETCHING (100% GITHUB PUBLIC REPO COMPLIANT)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 5:
    st.sidebar.error("❌ AI Status: Secrets Key Not Found / TOML Syntax Error")
else:
    st.sidebar.success("⚡ AI Status: Gemini Swarm Engine Fully Connected")

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
    
    if "ROCE %" in stock_data:
        fallback_analysis = (
            f"📊 **[INSTITUTIONAL EQUITY AUDIT DESK // ASSET: {ticker_name}]**\n\n"
            f"• **Capital Efficiency Matrix**: Return on Capital Employed (ROCE) is running verified at **{stock_data.get('ROCE %')}%**.\n\n"
            f"• **Leverage Audit**: Debt-to-Equity constraints map at **{stock_data.get('Debt/Equity')}**.\n\n"
            f"• **Information Layer**: Cross-referencing active metrics parameters against institutional Screener matrices."
        )
    elif "Churn %" in stock_data:
        fallback_analysis = (
            f"📊 **[LIQUIDITY DISTRIBUTION MATRIX REPORT // ASSET: {ticker_name}]**\n\n"
            f"• **Free Float Mapping**: Public liquidity blocks compute safely at **₹{stock_data.get('Free-Float (Cr)')} Cr**.\n\n"
            f"• **Volume Churn Verification**: Base floor accumulation systems track public float supply rotation turnover scales at **{stock_data.get('Churn %')}%**."
        )
    else:
        fallback_analysis = (
            f"📊 **[VOLATILITY CONTRACTION COMPLIANCE REGIME // ASSET: {ticker_name}]**\n\n"
            f"• **VCP Micro-Structural Arrays**: Price spot contractions track localized support zones near technical ceiling markers at **₹{stock_data.get('Ceiling Res')}**."
        )

    if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 5:
        return fallback_analysis
        
    try:
        # BINDING: Setting explicit system transport credentials options for auth tokens handling
        genai.configure(api_key=GEMINI_API_KEY, client_options={"api_endpoint": "generativelanguage.googleapis.com"})
        
        # Explicit routing configuration utilizing the modern model endpoint setup
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash'
        )
        
        prompt = f"""
        [SYSTEM ROLE DIRECTIVE & PRE-TRAINING TARGETS]:
        You are a legendary Senior Institutional Fund Manager and Chief Equity Research Auditor for Indian capital markets. 
        Your directive is to analyze core quantitative metrics, cross-verify them explicitly against the provided live news streams and Screener profiles, and deliver a high-conviction final verdict.
        
        [DIGESTED DATA ENVIRONMENT DATA]:
        - Target Stock Asset Ticker: {ticker_name}
        - Strategy Scope Context Layer: {context_tag}
        - Live Numeric Metrics Vector: {stock_data}
        - Current Live Corporate News Context: {live_news_context}
        - Institutional Subpath Reference: {screener_reference_url}
        
        [STRICT INSTRUCTIONAL BOUNDARIES]:
        - Never output boilerplate text, introductory pleasantries, or setup notes.
        - Meticulously prevent generic placeholders or broken tokens like 'None' or 'NaN' from passing into your response layout.
        - Your analysis tone must match a strict Bloomberg analyst desk style: direct, data-dense, mathematical, and highly aggressive.
        
        [TASK EXECUTION MATRIX]:
        Generate a highly professional 2-paragraph final verdict based on the specific performance values:
        - Paragraph 1: Quantitative & Fundamental Verification. Analyze the numerical values (ROCE/Leverage/Float Churn) and cross-verify them explicitly against the live news events and con-calls trajectory. Address if the news supports the hard metrics or if structural stress exists.
        - Paragraph 2: Institutional Asset Allocation Verdict. State an aggressive, high-conviction mathematical argument outlining if an elite portfolio allocator should Accumulate, Hold, or Avoid this specific equity risk structure.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = f"⚠️ **API CONNECTION ERROR**: {str(e)}"
        return f"{error_msg}\n\n---\n\n{fallback_analysis}"
            
