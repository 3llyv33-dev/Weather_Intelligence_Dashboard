from dash import html, dcc

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "bi-house-door-fill", "id": "nav-dashboard", "target": "section-dashboard"},
    {"label": "Current Weather", "icon": "bi-cloud-sun-fill", "id": "nav-current", "target": "section-current-weather"},
    {"label": "Forecast", "icon": "bi-calendar3", "id": "nav-forecast", "target": "section-forecast"},
    {"label": "Analytics", "icon": "bi-bar-chart-fill", "id": "nav-analytics", "target": "section-analytics"},
    {"label": "Aviation", "icon": "bi-airplane-fill", "id": "nav-aviation", "target": "section-aviation"},
    {"label": "Alerts", "icon": "bi-exclamation-triangle-fill", "id": "nav-alerts", "target": "section-alerts"},
    {"label": "City Comparison", "icon": "bi-graph-up", "id": "nav-comparison", "target": "section-comparison"},
    {"label": "Air Quality", "icon": "bi-wind", "id": "nav-air-quality", "target": "section-air-quality"},
    {"label": "Settings", "icon": "bi-gear-fill", "id": "nav-settings", "target": "section-settings"},
]


def build_sidebar():
    return html.Div(
        id="atmos-sidebar",
        className="atmos-sidebar",
        children=[
            html.Div(
                className="sidebar-nav",
                children=[
                    html.A(
                        [html.I(className=f"bi {item['icon']}"), html.Span(item["label"], className="nav-label")],
                        className=f"sidebar-nav-item{' active' if item['id'] == 'nav-dashboard' else ''}",
                        id=item["id"],
                        href=f"#{item['target']}",
                    )
                    for item in NAV_ITEMS
                ],
            ),
            html.Div(
                className="sidebar-section",
                children=[
                    html.Div(
                        className="sidebar-section-header",
                        children=[html.Span("POPULAR LOCATIONS")],
                    ),
                    html.Div(id="popular-locations-list", className="location-list"),
                ],
            ),
            html.Div(
                className="sidebar-section",
                children=[
                    html.Div(
                        className="sidebar-section-header",
                        children=[html.Span("RECENTLY VIEWED")],
                    ),
                    html.Div(id="recently-viewed-list", className="location-list"),
                ],
            ),
            html.Div(
                className="sidebar-footer",
                children=[
                    html.Button(
                        [
                            html.I(className="bi bi-thermometer-half"),
                            html.Span("Switch to \u00b0F", id="unit-toggle-label"),
                        ],
                        id="unit-toggle-btn",
                        className="unit-switch-btn",
                        n_clicks=0,
                    ),
                ],
            ),
            dcc.Store(id="unit-store", data="C"),
            dcc.Store(id="recently-viewed-store", storage_type="local", data=[]),
        ],
    )
