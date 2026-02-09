import json
from datetime import datetime
import random

signal = random.choice(["BUY", "SELL", "WAIT"])

data = {
    "signals": [
        {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "market": "FOREX",
            "pair": "EUR/USD",
            "signal": signal,
            "confidence": random.randint(60,90),
            "wins": 0,
            "losses": 0
        }
    ]
}

with open("signal.json", "w") as f:
    json.dump(data, f, indent=2)

print("Signal updated")
