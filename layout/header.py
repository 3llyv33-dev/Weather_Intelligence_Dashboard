from dash import html, dcc

from config import POPULAR_LOCATIONS, DEFAULT_CITY


def build_header():
    return html.Div(
        className="atmos-header",
        children=[
            html.Div(
                className="header-left",
                children=[
                    html.Button(
                        html.I(className="bi bi-list"),
                        id="sidebar-toggle",
                        className="icon-btn sidebar-toggle-btn",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="logo-block",
                        children=[
                            html.I(className="bi bi-cloud-sun-fill logo-icon"),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Span("WEATHER ", className="logo-title"),
                                            html.Span("INTELLIGENCE", className="logo-title accent"),
                                        ]
                                    ),
                                    html.Div("DASHBOARD", className="logo-subtitle"),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="header-center",
                children=[
                    html.Div(
                        className="search-box",
                        children=[
                            html.I(className="bi bi-search"),
                            dcc.Input(
                                id="city-search-input",
                                type="text",
                                placeholder="Search for a city...",
                                debounce=True,
                                className="search-input",
                            ),
                        ],
                    ),
                    html.Div(
                        className="city-dropdown-wrap",
                        children=[
                            html.I(className="bi bi-geo-alt-fill"),
                            dcc.Dropdown(
                                id="city-select-dropdown",
                                options=[
                                    {"label": f"{c['name']}, {c['country']}", "value": c["name"]}
                                    for c in POPULAR_LOCATIONS
                                ],
                                value=DEFAULT_CITY,
                                clearable=False,
                                searchable=False,
                                className="city-dropdown",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="header-right",
                children=[
                    html.Button(
                        [html.I(className="bi bi-geo-alt"), " Current Location"],
                        id="btn-current-location",
                        className="header-btn",
                        n_clicks=0,
                    ),
                    html.Button(
                        html.I(className="bi bi-arrow-clockwise"),
                        id="btn-refresh",
                        className="icon-btn",
                        n_clicks=0,
                        title="Refresh",
                    ),
                    html.Button(
                        html.I(className="bi bi-download"),
                        id="btn-export",
                        className="icon-btn",
                        n_clicks=0,
                        title="Export (print / save as PDF)",
                    ),
                    html.Button(
                        html.I(className="bi bi-moon-stars"),
                        id="btn-theme-toggle",
                        className="icon-btn",
                        n_clicks=0,
                        title="Toggle dark mode",
                    ),
                    html.Div(id="header-clock", className="header-clock"),
                    html.Div("AD", className="user-avatar"),
                ],
            ),
            dcc.Interval(id="clock-interval", interval=1000, n_intervals=0),
        ],
    )
