import os
import json
import json, os, datetime

HISTORY_PATH = "data/value_history.json"

def append_history(value):
    today = datetime.date.today().isoformat()
    data = {}
    if os.path.exists(HISTORY_PATH):
        data = json.load(open(HISTORY_PATH))
    data.setdefault(today, []).append({"timestamp": datetime.datetime.now().isoformat(), "value": value})
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def compute_report(range_days):
    if not os.path.exists(HISTORY_PATH):
        return None

    data = json.load(open(HISTORY_PATH))
    cutoff = datetime.date.today() - datetime.timedelta(days=range_days)
    values = []
    for day_str, entries in data.items():
        day = datetime.date.fromisoformat(day_str)
        if day >= cutoff:
            values.append(entries[-1]["value"])
    if not values: return None
    start = values[0]
    end = values[-1]
    pct = (end - start) / start * 100
    return {"from": cutoff.isoformat(), "to": datetime.date.today().isoformat(), "start": start, "end": end, "change_pct": round(pct,2)}
