from dash import html

KPI_DEFS = [
    {"key": "temperature", "label": "TEMPERATURE", "icon": "bi-thermometer-half", "color": "danger"},
    {"key": "humidity", "label": "HUMIDITY", "icon": "bi-droplet-fill", "color": "accent"},
    {"key": "wind_speed", "label": "WIND SPEED", "icon": "bi-wind", "color": "success"},
    {"key": "visibility", "label": "VISIBILITY", "icon": "bi-eye-fill", "color": "info"},
    {"key": "pressure", "label": "PRESSURE", "icon": "bi-speedometer2", "color": "secondary"},
]


def build_kpi_cards():
    return html.Div(
        id="section-current-weather",
        className="kpi-row",
        children=[
            html.Div(
                className=f"kpi-card kpi-{kpi['color']}",
                id=f"kpi-card-{kpi['key']}",
                children=[
                    html.Div(html.I(className=f"bi {kpi['icon']}"), className="kpi-icon"),
                    html.Div(id=f"kpi-value-{kpi['key']}", className="kpi-value"),
                    html.Div(kpi["label"], className="kpi-label"),
                    html.Div(id=f"kpi-trend-{kpi['key']}", className="kpi-trend"),
                ],
            )
            for kpi in KPI_DEFS
        ],
    )
