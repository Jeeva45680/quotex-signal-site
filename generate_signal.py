import json
from datetime import datetime

now = datetime.now()

data = {
    "signals": [
        {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M"),
            "market": "FOREX",
            "pair": "EUR/USD",
            "signal": "BUY",
            "confidence": 75,
            "wins": 1,
            "losses": 0
        }
    ]
}

with open("signal.json", "w") as f:
    json.dump(data, f, indent=2)

print("Signal updated")
