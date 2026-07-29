_ICON_MAP = {
    "sunny": "bi-sun-fill",
    "clear": "bi-sun-fill",
    "cloudy": "bi-cloud-fill",
    "clouds": "bi-cloud-fill",
    "mostly cloudy": "bi-cloud-sun-fill",
    "overcast": "bi-clouds-fill",
    "rainy": "bi-cloud-rain-fill",
    "rain": "bi-cloud-rain-fill",
    "drizzle": "bi-cloud-drizzle-fill",
    "thunderstorm": "bi-cloud-lightning-rain-fill",
    "fog": "bi-cloud-fog2-fill",
    "mist": "bi-cloud-fog2-fill",
    "haze": "bi-cloud-haze2-fill",
    "smoke": "bi-cloud-fog2-fill",
    "dust": "bi-cloud-haze2-fill",
    "sand": "bi-cloud-haze2-fill",
    "ash": "bi-cloud-fog2-fill",
    "squall": "bi-wind",
    "tornado": "bi-tornado",
    "wind": "bi-wind",
    "snow": "bi-snow",
    "sleet": "bi-cloud-sleet-fill",
}

_COLOR_MAP = {
    "sunny": "condition-warning",
    "clear": "condition-warning",
    "cloudy": "condition-neutral",
    "clouds": "condition-neutral",
    "mostly cloudy": "condition-accent",
    "overcast": "condition-neutral",
    "rainy": "condition-accent",
    "rain": "condition-accent",
    "drizzle": "condition-accent",
    "thunderstorm": "condition-info",
    "fog": "condition-neutral",
    "mist": "condition-neutral",
    "haze": "condition-neutral",
    "smoke": "condition-neutral",
    "dust": "condition-neutral",
    "sand": "condition-neutral",
    "ash": "condition-neutral",
    "squall": "condition-info",
    "tornado": "condition-danger",
    "wind": "condition-neutral",
    "snow": "condition-neutral",
    "sleet": "condition-accent",
}


def icon_for_condition(condition: str) -> str:
    return _ICON_MAP.get((condition or "").lower(), "bi-cloud-fill")


def color_class_for_condition(condition: str) -> str:
    return _COLOR_MAP.get((condition or "").lower(), "condition-neutral")
