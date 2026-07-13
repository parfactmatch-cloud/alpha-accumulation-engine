import datetime
import yfinance as yf

def execute_ipo_analysis(symbol, max_age, min_mcap, target_churn):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="max")
        if hist.empty: return None
        first_date = hist.index[0].date()
        if (datetime.date.today() - first_date).days > (max_age * 365): return None
        
        df = hist.tail(int(max_age * 250))
        info = t.info
        shares = info.get("sharesOutstanding") or 1
        f_shares = info.get("floatShares")
        if not f_shares: return None
        
        price = df["Close"].iloc[-1]
        mcap = (shares * price) / 10_000_000
        if mcap < min_mcap: return None
        ff_mcap = (f_shares * price) / 10_000_000
        
        low_p = df["Close"].min()
        base = df[df["Close"] <= low_p * 1.25]
        base_turnover = (base["Volume"] * base["Close"]).sum() / 10_000_000
        churn_pct = (base_turnover / ff_mcap) * 100
        
        if churn_pct < target_churn: return None
        
        desc = f"IPO core parameters matched. Listing date tracked from {first_date}. Market Cap at ₹{mcap:,.2f} Cr, Public Float Base records at ₹{ff_mcap:,.2f} Cr with an operational consolidation floor accumulation churn hitting {churn_pct:.2f}%."
        
        return {"Symbol": symbol, "Price (₹)": round(price, 2), "M-Cap (Cr)": round(mcap, 2), "Free-Float (Cr)": round(ff_mcap, 2), "Churn %": round(churn_pct, 2), "Description": desc, "FloatShares": f_shares, "TotalShares": shares}
    except: return None
      
