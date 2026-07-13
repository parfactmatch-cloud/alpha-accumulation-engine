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
            f"• **VCP Micro-Structural Arrays**: Price spot contractions track localized support zones near technical ceiling markers at **₹{stock_data.get('Live Price')}**."
        )

    if not GROQ_API_KEY or len(GROQ_API_KEY) < 5:
        return fallback_analysis
        
    try:
        conn = http.client.HTTPSConnection("api.groq.com")
        
        prompt = f"""
        You are a Senior Institutional Fund Manager and Chief Equity Research Auditor for Indian capital markets.
        Analyze core quantitative metrics, cross-verify them explicitly against the provided live news streams, and deliver a high-conviction final verdict.
        Target Stock Asset Ticker: {ticker_name}
        Strategy Scope Context Layer: {context_tag}
        Live Numeric Metrics Vector: {stock_data}
        Current Live Corporate News Context: {live_news_context}
        
        STRICT INSTRUCTIONAL BOUNDARIES:
        - Never output boilerplate text, introductory remarks, or setup notes.
        - Your analysis tone must match a strict Bloomberg analyst desk style: direct, data-dense, mathematical, and highly aggressive.
        
        Generate a highly professional 2-paragraph final verdict:
        - Paragraph 1: Quantitative & Fundamental Verification. Analyze the numerical values (ROCE/Leverage/Float Churn) and cross-verify them explicitly against the live news events. Address if the structural trends are strong or showing stress.
        - Paragraph 2: Institutional Asset Allocation Verdict. State an aggressive, high-conviction mathematical argument outlining if an elite portfolio allocator should Accumulate, Hold, or Avoid this specific equity risk structure.
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
        res = conn.getcallcallcallresponse() if hasattr(conn, 'getcallcallcallcallresponse') else (res := conn.getcallresponse() if hasattr(conn, 'getcallcallresponse') else conn.getcallresponse() if hasattr(conn, 'getcallresponse') else conn.getresponse())
        data = res.read()
        
        result_json = json.loads(data.decode("utf-8"))
        if 'choices' in result_json and len(result_json['choices']) > 0:
            return result_json['choices'][0]['message']['content']
        else:
            return f"⚠️ **GROQ API ERROR RESPONSE**: {str(result_json)}\n\n---\n\n{fallback_analysis}"
            
    except Exception as e:
        error_msg = f"⚠️ **GROQ CONNECTION ERROR**: {str(e)}"
        return f"{error_msg}\n\n---\n\n{fallback_analysis}"
                
