from dash import html, dcc


def build_hero():
    return html.Div(
        id="section-dashboard",
        className="hero-section",
        children=[
            dcc.Graph(
                id="hero-globe",
                config={"displayModeBar": False},
                className="hero-globe",
            ),
            html.Div(
                className="hero-main",
                children=[
                    html.Div(id="hero-greeting", className="hero-greeting"),
                    html.H2(id="hero-city", className="hero-city"),
                    html.Div(id="hero-country", className="hero-country"),
                    html.Div(
                        className="hero-temp-row",
                        children=[
                            html.Div(id="hero-temperature", className="hero-temperature"),
                            html.Div(
                                className="hero-condition-block",
                                children=[
                                    html.Div(id="hero-condition-icon", className="hero-condition-icon"),
                                    html.Div(id="hero-condition-label", className="hero-condition-label"),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="hero-meta-row",
                        children=[
                            html.Div(
                                [html.I(className="bi bi-thermometer-half"), html.Span(id="hero-feels-like")],
                                className="hero-meta-item",
                            ),
                            html.Div(id="hero-comfort-pill", className="comfort-pill"),
                            html.Div(
                                [html.I(className="bi bi-sunrise-fill"), html.Span(id="hero-sunrise")],
                                className="hero-meta-item",
                            ),
                            html.Div(
                                [html.I(className="bi bi-sunset-fill"), html.Span(id="hero-sunset")],
                                className="hero-meta-item",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="hero-score",
                children=[
                    html.Div(
                        className="score-card",
                        children=[
                            html.Div("Weather Score", className="hero-score-label"),
                            dcc.Graph(id="weather-score-gauge", config={"displayModeBar": False}, className="score-gauge"),
                            html.Div(id="weather-score-status", className="score-status"),
                        ],
                    ),
                ],
            ),
        ],
    )
