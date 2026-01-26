import yfinance as yf
import pandas as pd
import json
from datetime import datetime

# ======================
# SETTINGS
# ======================
SYMBOL = "EURUSD=X"   # change later if needed

# ======================
# INDICATORS
# ======================
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period-1, adjust=False).mean()
    avg_loss = loss.ewm(com=period-1, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ======================
# FETCH DATA (1 MIN)
# ======================
df = yf.download(SYMBOL, interval="1m", period="1d", progress=False)

if len(df) < 20:
    print("Not enough data")
    exit()

close = df["Close"].astype(float)

# ======================
# CALCULATE VALUES (SINGLE NUMBERS ONLY)
# ======================
ema5 = float(ema(close, 5).iloc[-1])
ema10 = float(ema(close, 10).iloc[-1])
rsi_val = float(rsi(close).iloc[-1])

last = float(close.iloc[-1])
prev = float(close.iloc[-2])

# ======================
# SIGNAL LOGIC
# ======================
signal = "NO TRADE"

if ema5 > ema10 and 40 <= rsi_val <= 65 and last > prev:
    signal = "CALL"
elif ema5 < ema10 and 35 <= rsi_val <= 60 and last < prev:
    signal = "PUT"

# ======================
# OUTPUT
# ======================
now = datetime.now().strftime("%H:%M")

data = {
    "time": now,
    "pair": "EUR/USD",
    "ema5": ema5,
    "ema10": ema10,
    "rsi": rsi_val,
    "signal": signal
}

with open("signal.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Signal generated:", signal)
