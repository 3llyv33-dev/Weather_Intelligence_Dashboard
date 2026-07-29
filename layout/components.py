from dash import html

from data.condition_icons import icon_for_condition, color_class_for_condition
from data import aggregator


def format_temp(value_c: float, unit: str) -> str:
    if unit == "F":
        return f"{round(value_c * 9 / 5 + 32)}\u00b0F"
    return f"{round(value_c)}\u00b0C"


def build_location_list_item(city_name: str, active: bool = False):
    try:
        current = aggregator.get_quick_conditions(city_name)
        temp = f"{round(current['temperature'])}\u00b0C"
        icon = icon_for_condition(current["condition"])
        color_class = color_class_for_condition(current["condition"])
    except Exception:
        temp = "\u2014"
        icon = "bi-question-circle"
        color_class = "condition-neutral"

    return html.Div(
        className=f"location-list-item{' active' if active else ''}",
        id={"type": "location-item", "city": city_name},
        n_clicks=0,
        children=[
            html.I(className=f"bi {icon} {color_class}"),
            html.Span(city_name, className="location-name"),
            html.Span(temp, className="location-temp"),
        ],
    )


def build_alert_card(alert: dict):
    icon_map = {
        "danger": "bi-cloud-rain-heavy-fill",
        "warning": "bi-wind",
        "info": "bi-cloud-lightning-fill",
        "success": "bi-check-circle-fill",
    }
    return html.Div(
        className=f"alert-card alert-{alert['level']}",
        children=[
            html.Div(html.I(className=f"bi {icon_map.get(alert['level'], 'bi-bell-fill')}"), className="alert-icon"),
            html.Div(
                children=[
                    html.Div(
                        [html.Span(alert["title"], className="alert-title"), html.Span(alert["time"], className="alert-time")],
                        className="alert-title-row",
                    ),
                    html.Div(alert["description"], className="alert-description"),
                ]
            ),
        ],
    )


def build_aviation_stat(label: str, value: str, sub: str):
    return html.Div(
        className="aviation-stat",
        children=[
            html.Div(value, className="aviation-stat-value"),
            html.Div(label, className="aviation-stat-label"),
            html.Div(sub, className="aviation-stat-sub"),
        ],
    )


def build_aq_metric(label: str, value):
    return html.Div(
        className="aq-metric-row",
        children=[
            html.Span(label, className="aq-metric-label"),
            html.Span(str(value), className="aq-metric-value"),
        ],
    )


def build_forecast_detail_body(day: dict, unit: str = "C"):
    rows = [
        ("High", format_temp(day["high"], unit)),
        ("Low", format_temp(day["low"], unit)),
        ("Humidity", f"{day['humidity']}%"),
        ("Rain Chance", f"{day['rain_chance']}%"),
        ("Wind", f"{day['wind_speed']} km/h"),
        ("Sunrise", day["sunrise"]),
        ("Sunset", day["sunset"]),
        ("Condition", day["condition"]),
    ]
    return html.Div(
        className="forecast-detail-grid",
        children=[
            html.Div(
                [html.Div(v, className="detail-value"), html.Div(k, className="detail-label")],
                className="detail-cell",
            )
            for k, v in rows
        ],
    )
