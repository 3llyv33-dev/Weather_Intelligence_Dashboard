from datetime import datetime


def generate_insights(current: dict, statistics: dict, comfort: dict) -> list:
    messages = []

    trend = statistics["temperature_trend"]
    if trend == "Increasing":
        messages.append("Temperature has been increasing compared to earlier readings this week.")
    elif trend == "Decreasing":
        messages.append("Temperature has been cooling compared to earlier readings this week.")
    else:
        messages.append("Temperature has remained stable over the past week.")

    rain_pct = statistics["condition_distribution"].get("rainy", 0) + \
        statistics["condition_distribution"].get("thunderstorm", 0)
    if rain_pct >= 50:
        messages.append(f"Rain probability is high this week ({rain_pct}% of observed days).")
    elif rain_pct >= 20:
        messages.append(f"Rain probability is moderate this week ({rain_pct}% of observed days).")
    else:
        messages.append("Rain probability is low this week.")

    if statistics["humidity_trend"] == "Stable":
        messages.append("Humidity is comfortable and stable today.")
    else:
        messages.append(f"Humidity is {statistics['humidity_trend'].lower()}.")

    if current["visibility"] >= 8:
        messages.append("Visibility is excellent.")
    elif current["visibility"] >= 5:
        messages.append("Visibility is good.")
    else:
        messages.append("Visibility is reduced — take care during travel.")

    if comfort["status"] in ("Excellent", "Good"):
        messages.append("Overall conditions are good for outdoor activities.")
    else:
        messages.append("Conditions are less favorable for extended outdoor activity.")

    return messages


def generate_recommendations(current: dict, statistics: dict, comfort: dict, weather_score: dict) -> list:
    recs = []

    rain_pct = statistics["condition_distribution"].get("rainy", 0) + \
        statistics["condition_distribution"].get("thunderstorm", 0)
    if rain_pct >= 30:
        recs.append("Carry an umbrella if going out later today.")

    if current["temperature"] >= 30:
        recs.append("High UV exposure likely. Wear sunscreen and stay hydrated.")

    if comfort["heat_risk"] in ("High", "Severe"):
        recs.append("Avoid prolonged outdoor activity during peak heat hours.")
    else:
        recs.append("Good conditions for outdoor activities and travel.")

    if current["wind_speed"] >= 30:
        recs.append("Strong winds expected — avoid small boat travel.")

    if current["visibility"] >= 8 and current["wind_speed"] < 25:
        recs.append("Visibility and wind conditions are suitable for flight operations.")

    if weather_score["value"] < 50:
        recs.append("Consider postponing non-essential outdoor plans today.")

    return recs


def generate_alerts(current: dict, statistics: dict, weather_score: dict) -> list:
    alerts = []
    now = datetime.now().strftime("%H:%M")
    rain_pct = statistics["condition_distribution"].get("rainy", 0) + \
        statistics["condition_distribution"].get("thunderstorm", 0)

    if rain_pct >= 50 or current["condition"].lower() in ("rainy", "rain"):
        alerts.append({
            "level": "danger",
            "title": "Heavy Rain",
            "time": now,
            "description": "Rain conditions expected in the coming hours.",
        })
    if current["wind_speed"] >= 28:
        alerts.append({
            "level": "warning",
            "title": "Strong Wind",
            "time": now,
            "description": f"Gusts up to {round(current['wind_speed'] + 8)} km/h.",
        })
    if current["condition"].lower() == "thunderstorm":
        alerts.append({
            "level": "info",
            "title": "Thunderstorm",
            "time": now,
            "description": "Possible this evening.",
        })
    if not alerts:
        alerts.append({
            "level": "success",
            "title": "All Clear",
            "time": now,
            "description": "No active weather warnings for this area.",
        })
    return alerts
