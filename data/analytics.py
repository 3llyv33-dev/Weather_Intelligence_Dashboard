import math
from collections import Counter


def compute_statistics(trend_series: list) -> dict:
    temps = [d["temperature"] for d in trend_series]
    rainfall = [d["rainfall_mm"] for d in trend_series]
    winds = [d["wind_speed"] for d in trend_series]
    humidity = [d["humidity"] for d in trend_series]
    conditions = [d["condition"] for d in trend_series]

    avg_temp = round(sum(temps) / len(temps), 1) if temps else 0
    max_temp = max(temps) if temps else 0
    min_temp = min(temps) if temps else 0

    condition_counts = Counter(conditions)
    total = sum(condition_counts.values()) or 1
    distribution = {
        cond.lower(): round((count / total) * 100)
        for cond, count in condition_counts.items()
    }

    return {
        "average_temperature": avg_temp,
        "highest_temperature": round(max_temp, 1),
        "lowest_temperature": round(min_temp, 1),
        "temperature_range": round(max_temp - min_temp, 1),
        "temperature_trend": _detect_trend(temps),
        "total_rainfall_mm": round(sum(rainfall), 1),
        "average_daily_rainfall_mm": round(sum(rainfall) / len(rainfall), 1) if rainfall else 0,
        "rainy_days_count": sum(1 for r in rainfall if r >= 1.0),
        "average_wind_speed": round(sum(winds) / len(winds), 1) if winds else 0,
        "max_wind_speed": round(max(winds), 1) if winds else 0,
        "average_humidity": round(sum(humidity) / len(humidity)) if humidity else 0,
        "humidity_trend": _detect_trend(humidity),
        "condition_distribution": distribution,
        "wettest_day": _label_of_max(trend_series, "rainfall_mm"),
    }


def _detect_trend(values: list, threshold: float = 0.5) -> str:
    if len(values) < 2:
        return "Stable"
    mid = len(values) // 2
    first_half_avg = sum(values[:mid]) / mid if mid else values[0]
    second_half_avg = sum(values[mid:]) / (len(values) - mid)
    delta = second_half_avg - first_half_avg
    if delta > threshold:
        return "Increasing"
    if delta < -threshold:
        return "Decreasing"
    return "Stable"


def _label_of_max(series: list, key: str) -> str:
    if not series:
        return "N/A"
    best = max(series, key=lambda d: d[key])
    return best.get("label", best.get("date", "N/A"))


def compute_comfort_index(temperature: float, humidity: float) -> dict:
    if temperature <= 28 and humidity <= 60:
        return {"status": "Excellent", "heat_risk": "Low"}
    if temperature <= 32 and humidity <= 70:
        return {"status": "Good", "heat_risk": "Low"}
    if temperature <= 34 and humidity <= 80:
        return {"status": "Moderate", "heat_risk": "Moderate"}
    if temperature <= 38:
        return {"status": "Poor", "heat_risk": "High"}
    return {"status": "Critical", "heat_risk": "Severe"}


def compute_weather_score(current: dict, statistics: dict) -> dict:
    score = 100.0

    temp = current["temperature"]
    if temp < 15 or temp > 36:
        score -= 25
    elif temp < 18 or temp > 32:
        score -= 12
    elif temp < 20 or temp > 29:
        score -= 5

    humidity = current["humidity"]
    if humidity > 85 or humidity < 20:
        score -= 15
    elif humidity > 70 or humidity < 30:
        score -= 8

    if current["wind_speed"] > 40:
        score -= 15
    elif current["wind_speed"] > 25:
        score -= 7

    if current["pressure"] < 1000:
        score -= 10
    elif current["pressure"] < 1008:
        score -= 4

    if current["visibility"] < 3:
        score -= 15
    elif current["visibility"] < 6:
        score -= 6

    rain_pct = statistics["condition_distribution"].get("rainy", 0) + \
        statistics["condition_distribution"].get("thunderstorm", 0)
    score -= rain_pct * 0.15

    score = max(0, min(100, round(score)))
    return {"value": score, "status": _score_status(score)}


def _score_status(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Moderate"
    if score >= 25:
        return "Poor"
    return "Critical"


def pm25_to_aqi(pm25: float) -> dict:
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]
    pm25 = max(0.0, pm25)
    for c_low, c_high, aqi_low, aqi_high in breakpoints:
        if c_low <= pm25 <= c_high:
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (pm25 - c_low) + aqi_low
            return {"aqi": round(aqi), "status": _aqi_status(round(aqi))}
    return {"aqi": 500, "status": "Hazardous"}


def _aqi_status(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy (Sensitive)"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def compute_aviation_status(current: dict, weather_score: dict, cloud_cover: int) -> dict:
    wind_speed = current["wind_speed"]
    crosswind = round(wind_speed * math.sin(math.radians(45)), 1)

    is_wet = current["condition"].lower() in ("rainy", "thunderstorm", "rain")
    runway_condition = "WET" if is_wet else "DRY"
    runway_quality = "Caution" if is_wet else "Good"

    score = weather_score["value"]
    if score >= 85 and current["visibility"] >= 8 and wind_speed < 30:
        flight_condition, risk_label = "EXCELLENT", "Safe for Operations"
    elif score >= 65 and current["visibility"] >= 5:
        flight_condition, risk_label = "GOOD", "Safe for Operations"
    elif score >= 40:
        flight_condition, risk_label = "MODERATE", "Caution Advised"
    else:
        flight_condition, risk_label = "POOR", "Operations Not Recommended"

    return {
        "flight_condition": flight_condition,
        "cloud_cover_percent": cloud_cover,
        "crosswind_kmh": crosswind,
        "runway_condition": runway_condition,
        "runway_quality": runway_quality,
        "weather_risk": risk_label,
    }
