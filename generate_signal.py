import json
from datetime import datetime

data = {
    "signals": [
        {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "market": "FOREX",
            "pair": "EUR/USD",
            "signal": "WAIT",
            "confidence": 0,
            "wins": 0,
            "losses": 0
        }
    ]
}

with open("signal.json", "w") as f:
    json.dump(data, f, indent=2)
