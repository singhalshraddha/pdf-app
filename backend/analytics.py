import json
from datetime import datetime

def log_action(action, detail):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "detail": detail
    }
    with open("output/analytics.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
