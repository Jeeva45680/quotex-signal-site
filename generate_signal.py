import yfinance as yf
import json
from datetime import datetime

PAIR = "EURUSD=X"

df = yf.download(PAIR, interval="1m", period="1d")

if df.empty:
    exit()

df["ema5"] = df["Close"].ewm(span=5).mean()
df["ema10"] = df["Close"].ewm(span=10).mean()

delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
df["rsi"] = 100 - (100 / (1 + rs))

ema5 = float(df["ema5"].iloc[-1])
ema10 = float(df["ema10"].iloc[-1])
rsi = float(df["rsi"].iloc[-1])

signal = "NO TRADE"

if ema5 > ema10 and rsi > 50:
    signal = "CALL"
elif ema5 < ema10 and rsi < 50:
    signal = "PUT"

now = datetime.now()

data = {
    "signals": [{
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M"),
        "market": "FOREX",
        "pair": "EUR/USD",
        "signal": signal,
        "confidence": 0,
        "wins": 0,
        "losses": 0
    }]
}

with open("signal.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated:", signal)
