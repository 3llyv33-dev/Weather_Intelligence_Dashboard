import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "").strip()

_env_mock_flag = os.getenv("USE_MOCK_DATA")
if _env_mock_flag is not None:
    USE_MOCK_DATA = _env_mock_flag.strip().lower() == "true"
else:
    USE_MOCK_DATA = not bool(OPENWEATHERMAP_API_KEY)

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "600"))
AUTO_REFRESH_MS = int(os.getenv("AUTO_REFRESH_MS", str(CACHE_TTL_SECONDS * 1000)))
COLORS = {
    "primary": "#0F172A",
    "secondary": "#1E3A8A",
    "accent": "#38BDF8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#8B5CF6",
    "background": "#F1F5F9",
    "card": "#FFFFFF",
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
}

WEATHER_SCORE_TIERS = [
    (90, "Excellent", COLORS["success"]),
    (75, "Good", COLORS["success"]),
    (50, "Moderate", COLORS["warning"]),
    (25, "Poor", COLORS["danger"]),
    (0, "Critical", COLORS["danger"]),
]

FONT_FAMILY = "'Inter', 'Manrope', 'Poppins', sans-serif"
POPULAR_LOCATIONS = [
    {"name": "Dar es Salaam", "country": "TZ", "lat": -6.7924, "lon": 39.2083},
    {"name": "Dodoma", "country": "TZ", "lat": -6.1630, "lon": 35.7516},
    {"name": "Arusha", "country": "TZ", "lat": -3.3869, "lon": 36.6830},
    {"name": "Mwanza", "country": "TZ", "lat": -2.5164, "lon": 32.9175},
    {"name": "Mbeya", "country": "TZ", "lat": -8.9094, "lon": 33.4608},
    {"name": "Zanzibar", "country": "TZ", "lat": -6.1659, "lon": 39.2026},
]

DEFAULT_CITY = "Dar es Salaam"

TIME_RANGES = [
    {"label": "Today", "value": "1"},
    {"label": "3 Days", "value": "3"},
    {"label": "7 Days", "value": "7"},
    {"label": "30 Days", "value": "30"},
]
