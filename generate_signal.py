import yfinance as yf
import pandas as pd
import json
from datetime import datetime

ASSETS = {
    "FOREX": {"EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD"},
    "CRYPTO": {"BTC-USD": "BTC/USD"},
    "COMMODITY": {"GC=F": "GOLD"}
}

def ema(s, p):
    return s.ewm(span=p, adjust=False).mean()

def rsi(s, p=14):
    d = s.diff()
    g = d.clip(lower=0)
    l = -d.clip(upper=0)
    rs = g.ewm(com=p-1, adjust=False).mean() / l.ewm(com=p-1, adjust=False).mean()
    return 100 - (100 / (1 + rs))

signals = []

now = datetime.now()
date = now.strftime("%d/%m/%Y")
time = now.strftime("%H:%M")

for market, items in ASSETS.items():
    for symbol, name in items.items():
        df = yf.download(symbol, interval="1m", period="1d", progress=False)
        if len(df) < 20:
            continue

        close = df["Close"]
        ema5 = ema(close, 5).iloc[-1]
        ema10 = ema(close, 10).iloc[-1]
        rsi_val = rsi(close).iloc[-1]

        signal = "NO TRADE"
        confidence = 0

        if ema5 > ema10 and 45 <= rsi_val <= 65:
            signal = "CALL"
            confidence = 70
        elif ema5 < ema10 and 35 <= rsi_val <= 55:
            signal = "PUT"
            confidence = 68

        signals.append({
            "date": date,
            "time": time,
            "market": market,
            "pair": name,
            "signal": signal,
            "confidence": confidence,
            "wins": 0,
            "losses": 0
        })

with open("signal.json", "w") as f:
    json.dump({"signals": signals}, f, indent=2)

print("Signals generated")
