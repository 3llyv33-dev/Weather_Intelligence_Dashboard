import math
import random
from collections import defaultdict
from datetime import datetime, timedelta

import requests

from config import OPENWEATHERMAP_API_KEY, USE_MOCK_DATA, POPULAR_LOCATIONS

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"

CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Thunderstorm", "Mostly Cloudy", "Clear"]
WIND_DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


class WeatherAPIError(Exception):
    pass


def fetch_current(city: str) -> dict:
    if USE_MOCK_DATA:
        return _mock_current(city)
    try:
        resp = requests.get(
            CURRENT_URL,
            params={"q": city, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"},
            timeout=6,
        )
        resp.raise_for_status()
        raw = resp.json()
        return {
            "city": raw["name"],
            "country": raw.get("sys", {}).get("country", ""),
            "temperature": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"],
            "wind_speed": round(raw["wind"]["speed"] * 3.6, 1),
            "wind_direction": _deg_to_compass(raw["wind"].get("deg", 0)),
            "pressure": raw["main"]["pressure"],
            "visibility": round(raw.get("visibility", 10000) / 1000, 1),
            "cloud_cover": raw.get("clouds", {}).get("all", 0),
            "condition": raw["weather"][0]["main"],
            "rainfall_mm": raw.get("rain", {}).get("1h", 0),
            "sunrise": datetime.fromtimestamp(raw["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(raw["sys"]["sunset"]).strftime("%H:%M"),
        }
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise WeatherAPIError(f"Could not fetch current weather for '{city}': {exc}") from exc


def fetch_forecast(city: str, days: int = 7) -> list:
    if USE_MOCK_DATA:
        return _mock_forecast(city, days)
    try:
        resp = requests.get(
            FORECAST_URL,
            params={"q": city, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"},
            timeout=6,
        )
        resp.raise_for_status()
        raw = resp.json()
        return _group_forecast_by_day(raw["list"])[:days]
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise WeatherAPIError(f"Could not fetch forecast for '{city}': {exc}") from exc


def fetch_air_quality(lat: float, lon: float) -> dict:
    if USE_MOCK_DATA:
        return _mock_air_quality()
    try:
        resp = requests.get(
            AIR_POLLUTION_URL,
            params={"lat": lat, "lon": lon, "appid": OPENWEATHERMAP_API_KEY},
            timeout=6,
        )
        resp.raise_for_status()
        raw = resp.json()["list"][0]["components"]
        return {
            "pm2_5": round(raw.get("pm2_5", 0), 1),
            "pm10": round(raw.get("pm10", 0), 1),
            "o3": round(raw.get("o3", 0), 1),
            "no2": round(raw.get("no2", 0), 1),
            "co": round(raw.get("co", 0) / 1000, 2),
        }
    except (requests.RequestException, KeyError, ValueError, IndexError) as exc:
        raise WeatherAPIError(f"Could not fetch air quality: {exc}") from exc


def geocode_city(city: str):
    if USE_MOCK_DATA:
        return _mock_geocode(city)
    try:
        resp = requests.get(
            GEOCODING_URL,
            params={"q": city, "limit": 1, "appid": OPENWEATHERMAP_API_KEY},
            timeout=6,
        )
        resp.raise_for_status()
        results = resp.json()
        if not results:
            raise WeatherAPIError(f"City '{city}' not found.")
        return results[0]["lat"], results[0]["lon"]
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        raise WeatherAPIError(f"Could not geocode '{city}': {exc}") from exc


def _group_forecast_by_day(entries: list) -> list:
    days = defaultdict(list)
    for e in entries:
        date_str = e["dt_txt"].split(" ")[0]
        days[date_str].append(e)

    today_str = datetime.now().strftime("%Y-%m-%d")
    result = []
    for date_str, blocks in days.items():
        temps = [b["main"]["temp"] for b in blocks]
        mid_block = blocks[len(blocks) // 2]
        d = datetime.strptime(date_str, "%Y-%m-%d")
        result.append({
            "day": "Today" if date_str == today_str else d.strftime("%a"),
            "date": d.strftime("%d %b"),
            "high": round(max(temps)),
            "low": round(min(temps)),
            "rain_chance": round(max(b.get("pop", 0) for b in blocks) * 100),
            "wind_speed": round(mid_block["wind"]["speed"] * 3.6, 1),
            "condition": mid_block["weather"][0]["main"],
            "humidity": mid_block["main"]["humidity"],
        })
    return result


def _deg_to_compass(deg: float) -> str:
    ix = int((deg / 22.5) + 0.5) % 16
    return WIND_DIRECTIONS[ix]


def _city_seed(city: str) -> int:
    return sum(ord(c) for c in city.lower())


def _mock_country(city: str) -> str:
    for loc in POPULAR_LOCATIONS:
        if loc["name"].lower() == city.lower():
            return loc["country"]
    return "TZ"


def _mock_sunrise_sunset(city: str, date: datetime = None) -> tuple:
    if date is None:
        date = datetime.now()
    rnd = random.Random(_city_seed(city) + date.timetuple().tm_yday)
    lat = next((loc["lat"] for loc in POPULAR_LOCATIONS if loc["name"].lower() == city.lower()), -6.0)
    eq_offset = abs(lat) / 90 * 1.5
    season_shift = math.sin(2 * math.pi * (date.timetuple().tm_yday - 81) / 365) * 0.5
    sunrise = 5.8 + eq_offset - season_shift
    sunset = 18.2 - eq_offset + season_shift
    sunrise_h = int(sunrise)
    sunrise_m = int((sunrise - sunrise_h) * 60)
    sunset_h = int(sunset)
    sunset_m = int((sunset - sunset_h) * 60)
    return f"{sunrise_h:02d}:{sunrise_m:02d}", f"{sunset_h:02d}:{sunset_m:02d}"


def _mock_current(city: str) -> dict:
    rnd = random.Random(_city_seed(city) + datetime.now().hour)
    base_temp = 24 + (rnd.random() * 8)
    condition = rnd.choice(CONDITIONS)
    rainfall = 0.0
    if condition == "Thunderstorm":
        rainfall = round(rnd.uniform(6, 15), 1)
    elif condition == "Rainy":
        rainfall = round(rnd.uniform(1, 8), 1)
    sunrise, sunset = _mock_sunrise_sunset(city)
    return {
        "city": city,
        "country": _mock_country(city),
        "temperature": round(base_temp, 1),
        "feels_like": round(base_temp + rnd.uniform(1, 3), 1),
        "humidity": rnd.randint(50, 80),
        "wind_speed": round(rnd.uniform(8, 25), 1),
        "wind_direction": rnd.choice(WIND_DIRECTIONS),
        "pressure": rnd.randint(1005, 1018),
        "visibility": rnd.randint(6, 10),
        "cloud_cover": rnd.randint(10, 80),
        "condition": condition,
        "rainfall_mm": rainfall,
        "sunrise": sunrise,
        "sunset": sunset,
    }


def _mock_forecast(city: str, days: int = 7) -> list:
    rnd = random.Random(_city_seed(city))
    forecast = []
    today = datetime.now()
    for i in range(days):
        date = today + timedelta(days=i)
        high = round(26 + rnd.uniform(0, 6))
        low = round(high - rnd.uniform(4, 8))
        sunrise, sunset = _mock_sunrise_sunset(city, date)
        forecast.append({
            "day": "Today" if i == 0 else date.strftime("%a"),
            "date": date.strftime("%d %b"),
            "high": high,
            "low": low,
            "rain_chance": rnd.randint(5, 80),
            "wind_speed": round(rnd.uniform(8, 22), 1),
            "condition": rnd.choice(CONDITIONS),
            "humidity": rnd.randint(50, 85),
            "sunrise": sunrise,
            "sunset": sunset,
        })
    return forecast


def _mock_air_quality() -> dict:
    rnd = random.Random(datetime.now().day)
    return {
        "pm2_5": round(rnd.uniform(8, 25), 1),
        "pm10": round(rnd.uniform(15, 40), 1),
        "o3": round(rnd.uniform(15, 35), 1),
        "no2": round(rnd.uniform(8, 20), 1),
        "co": round(rnd.uniform(0.2, 0.6), 2),
    }


def _mock_geocode(city: str):
    for loc in POPULAR_LOCATIONS:
        if loc["name"].lower() == city.lower():
            return loc["lat"], loc["lon"]
    rnd = random.Random(_city_seed(city))
    return round(rnd.uniform(-10, 10), 4), round(rnd.uniform(20, 45), 4)
