import json
import os
from datetime import datetime, timedelta

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "history")
os.makedirs(HISTORY_DIR, exist_ok=True)


def _history_path(city: str) -> str:
    safe_name = "".join(c if c.isalnum() else "_" for c in city.lower())
    return os.path.join(HISTORY_DIR, f"{safe_name}.json")


def _load(city: str) -> list:
    path = _history_path(city)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(city: str, records: list) -> None:
    try:
        with open(_history_path(city), "w") as f:
            json.dump(records, f, indent=2)
    except OSError:
        pass


def record_snapshot(city: str, current: dict) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    records = _load(city)
    if any(r["date"] == today for r in records):
        return
    records.append({
        "date": today,
        "temperature": current["temperature"],
        "humidity": current["humidity"],
        "wind_speed": current["wind_speed"],
        "rainfall_mm": current.get("rainfall_mm", 0),
        "condition": current["condition"],
    })
    records = records[-90:]
    _save(city, records)


def get_trend_series(city: str, days: int) -> list:
    records = _load(city)
    records_by_date = {r["date"]: r for r in records}

    today = datetime.now()
    series = []
    for i in range(days - 1, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        if date_str in records_by_date:
            r = records_by_date[date_str]
            series.append({
                "date": date_str,
                "label": date.strftime("%a"),
                "temperature": r["temperature"],
                "humidity": r["humidity"],
                "wind_speed": r["wind_speed"],
                "rainfall_mm": r["rainfall_mm"],
                "condition": r["condition"],
                "is_logged": True,
            })
    return series
