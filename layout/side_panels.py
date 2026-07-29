from dash import html


def build_side_panels():
    return html.Div(
        className="side-rail",
        children=[
            html.Div(
                id="section-alerts",
                className="panel-card",
                children=[
                    html.Div(
                        className="section-header",
                        children=[
                            html.Span("WEATHER ALERTS", className="section-title"),
                        ],
                    ),
                    html.Div(id="alerts-list", className="alerts-list"),
                ],
            ),
            html.Div(
                id="section-aviation",
                className="panel-card",
                children=[
                    html.Div(
                        className="section-header",
                        children=[
                            html.Span("AVIATION WEATHER", className="section-title"),
                        ],
                    ),
                    html.Div(id="aviation-panel-body"),
                ],
            ),
        ],
    )
