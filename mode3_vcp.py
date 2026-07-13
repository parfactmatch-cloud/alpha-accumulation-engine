import yfinance as yf

def execute_vcp_scalp(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="5d", interval="15m")
        if df.empty or len(df) < 30: return None
        
        r_max = df["High"].max()
        price = df["Close"].iloc[-1]
        info = t.info
        shares = info.get("sharesOutstanding") or 1
        f_shares = info.get("floatShares") or (shares * 0.40)
        
        mid = len(df) // 2
        low_t1 = df["Low"].iloc[0:mid].min()
        low_t2 = df["Low"].iloc[mid:-10].min()
        low_t3 = df["Low"].iloc[-10:].min()
        
        d1 = ((r_max - low_t1) / r_max) * 100 if r_max > 0 else 0
        d2 = ((r_max - low_t2) / r_max) * 100 if r_max > 0 else 0
        d3 = ((r_max - low_t3) / r_max) * 100 if r_max > 0 else 0
        
        if not (d1 >= d2 and d2 >= d3): return None
        
        desc = f"Volatility Compression Array matched on current high-frequency matrix data tracking bounds. Current price verified at ₹{price} near immediate cycle overhead boundaries at ₹{r_max}."
        
        return {"Symbol": symbol, "Live Price": round(price, 2), "Ceiling Res": round(r_max, 2), "W1 %": round(d1, 2), "W2 %": round(d2, 2), "Status": "🟢 COMPLIANT", "Description": desc, "FloatShares": f_shares, "TotalShares": shares}
    except: return None
      
