import yfinance as yf
import pandas as pd
import json
from datetime import datetime

ASSETS = {
    "FOREX": {"EURUSD=X": "EUR/USD"},
}

signals = []

for market, items in ASSETS.items():
    for symbol, pair_name in items.items():

        df = yf.download(symbol, interval="1m", period="1d", progress=False)

        if len(df) < 20:
            continue

        close = df["Close"]

        ema5 = close.ewm(span=5).mean().iloc[-1]
        ema10 = close.ewm(span=10).mean().iloc[-1]

        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        rs = gain.rolling(14).mean() / loss.rolling(14).mean()
        rsi_val = (100 - (100 / (1 + rs))).iloc[-1]

        signal = "NO TRADE"
        confidence = 0

        if ema5 > ema10 and 45 <= rsi_val <= 65:
            signal = "CALL"
            confidence = 70
        elif ema5 < ema10 and 35 <= rsi_val <= 60:
            signal = "PUT"
            confidence = 70

        now = datetime.now()
        signals.append({
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M"),
            "market": market,
            "pair": pair_name,
            "signal": signal,
            "confidenceConfidence": confidence,
            "wins": 0,
            "losses": 0
        })

# SAVE JSON
with open("signal.json", "w") as f:
    json.dump({"signals": signals}, f, indent=2)

print("Signals generated successfully")
