import yfinance as yf

def execute_value_audit(symbol, min_mcap):
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
        if mcap < min_mcap: return None
        
        ebit = abs_fi.loc["Operating Income"].iloc[0] if "Operating Income" in abs_fi.index else 0
        ta = abs_bs.loc["Total Assets"].iloc[0] if "Total Assets" in abs_bs.index else 1
        cl = abs_bs.loc["Total Current Liabilities"].iloc[0] if "Total Current Liabilities" in abs_bs.index else 0
        
        cap_employed = ta - cl
        roce = (ebit / cap_employed) * 100 if cap_employed > 0 else 0
        debt = abs_bs.loc["Total Debt"].iloc[0] if "Total Debt" in abs_bs.index else 0
        de = debt / (mcap * 10_000_000)
        
        if roce < 12.0 or de > 0.50: return None
        f_shares = info.get("floatShares") or (shares * 0.35)
        
        desc = f"Value metrics operational check completed. Asset market capitalization scores ₹{mcap:,.2f} Cr. Fundamental core audits track return on capital employed at {roce:.2f}% under a strict balance sheet leverage structure matching a Debt/Equity profile of {de:.2f}."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "ROCE %": round(roce, 2), "Debt/Equity": round(de, 2), "Description": desc, "FloatShares": f_shares, "TotalShares": shares}
    except: return None
      
