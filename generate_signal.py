import json
from datetime import datetime

now = datetime.now()

signal_data = {
    "signals": [
        {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M"),
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
    json.dump(signal_data, f, indent=2)

print("Signal generated successfully")
