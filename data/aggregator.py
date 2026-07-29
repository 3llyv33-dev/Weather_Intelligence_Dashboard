import time

from config import CACHE_TTL_SECONDS
from data import weather_api, analytics, insights, history_store
from data.weather_api import WeatherAPIError

_cache = {}
_quick_cache = {}


def get_dashboard_data(city: str, trend_days: int = 7, use_cache: bool = True) -> dict:
    key = f"{city.lower()}::{trend_days}"
    now = time.time()
    if use_cache and key in _cache:
        cached_at, data = _cache[key]
        if now - cached_at < CACHE_TTL_SECONDS:
            return data

    data = _fetch_dashboard_data(city, trend_days)
    _cache[key] = (now, data)
    return data


def get_quick_conditions(city: str) -> dict:
    key = city.lower()
    now = time.time()
    if key in _quick_cache:
        cached_at, data = _quick_cache[key]
        if now - cached_at < CACHE_TTL_SECONDS:
            return data
    data = weather_api.fetch_current(city)
    _quick_cache[key] = (now, data)
    return data


def _fetch_dashboard_data(city: str, trend_days: int) -> dict:
    current = weather_api.fetch_current(city)
    forecast = weather_api.fetch_forecast(city, days=7)

    history_store.record_snapshot(city, current)
    trend_series = history_store.get_trend_series(city, trend_days)

    statistics = analytics.compute_statistics(trend_series)
    comfort = analytics.compute_comfort_index(current["temperature"], current["humidity"])
    weather_score = analytics.compute_weather_score(current, statistics)

    lat, lon = weather_api.geocode_city(city)
    air_raw = weather_api.fetch_air_quality(lat, lon)
    air_quality = analytics.pm25_to_aqi(air_raw["pm2_5"])
    air_quality.update(air_raw)

    aviation = analytics.compute_aviation_status(
        current, weather_score, current.get("cloud_cover", 30)
    )

    return {
        "current": current,
        "forecast": forecast,
        "trend_series": trend_series,
        "statistics": statistics,
        "insights": {
            "messages": insights.generate_insights(current, statistics, comfort),
            "recommendations": insights.generate_recommendations(current, statistics, comfort, weather_score),
            "weather_score": weather_score,
            "comfort_index": comfort,
        },
        "aviation": aviation,
        "air_quality": air_quality,
    }


def get_comparison_data(cities: list, trend_days: int = 7) -> dict:
    result = {}
    for city in cities:
        try:
            current = get_quick_conditions(city)
            history_store.record_snapshot(city, current)
            trend = history_store.get_trend_series(city, trend_days)
            result[city] = {"current": current, "trend_series": trend}
        except Exception:
            continue
    return result
