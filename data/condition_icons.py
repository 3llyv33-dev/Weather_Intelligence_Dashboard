_ICON_MAP = {
    "sunny": "bi-sun-fill",
    "clear": "bi-sun-fill",
    "cloudy": "bi-cloud-fill",
    "clouds": "bi-cloud-fill",
    "mostly cloudy": "bi-cloud-sun-fill",
    "rainy": "bi-cloud-rain-fill",
    "rain": "bi-cloud-rain-fill",
    "drizzle": "bi-cloud-drizzle-fill",
    "thunderstorm": "bi-cloud-lightning-rain-fill",
    "fog": "bi-cloud-fog2-fill",
    "mist": "bi-cloud-fog2-fill",
    "haze": "bi-cloud-haze2-fill",
    "wind": "bi-wind",
    "snow": "bi-snow",
}

_COLOR_MAP = {
    "sunny": "condition-warning",
    "clear": "condition-warning",
    "cloudy": "condition-neutral",
    "clouds": "condition-neutral",
    "mostly cloudy": "condition-accent",
    "rainy": "condition-accent",
    "rain": "condition-accent",
    "drizzle": "condition-accent",
    "thunderstorm": "condition-info",
    "fog": "condition-neutral",
    "mist": "condition-neutral",
    "haze": "condition-neutral",
    "wind": "condition-neutral",
    "snow": "condition-neutral",
}


def icon_for_condition(condition: str) -> str:
    return _ICON_MAP.get((condition or "").lower(), "bi-cloud-fill")


def color_class_for_condition(condition: str) -> str:
    return _COLOR_MAP.get((condition or "").lower(), "condition-neutral")
