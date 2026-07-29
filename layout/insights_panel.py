from dash import html, dcc
import dash_bootstrap_components as dbc


def build_insights_section():
    return html.Div(
        className="insights-row",
        children=[
            html.Div(
                className="panel-card",
                children=[
                    html.Div("WEATHER INSIGHTS", className="section-title"),
                    html.Div(id="insights-list", className="insight-list"),
                ],
            ),
            html.Div(
                className="panel-card",
                children=[
                    html.Div("RECOMMENDATIONS", className="section-title"),
                    html.Div(id="recommendations-list", className="insight-list"),
                ],
            ),
            html.Div(
                id="section-comparison",
                className="panel-card panel-card-wide",
                children=[
                    html.Div(
                        className="section-header",
                        children=[
                            html.Span("CITY COMPARISON", className="section-title"),
                            html.Span("Compare up to 3 cities", className="chart-subtitle"),
                        ],
                    ),
                    dbc.Checklist(
                        id="comparison-city-checklist",
                        className="comparison-checklist",
                        inputClassName="comparison-check-input",
                        labelClassName="comparison-check-label",
                        labelCheckedClassName="checked",
                        options=[],
                        value=[],
                        inline=True,
                    ),
                    dcc.Graph(id="city-comparison-chart", config={"displayModeBar": False}),
                ],
            ),
            html.Div(
                id="section-air-quality",
                className="panel-card",
                children=[
                    html.Div(
                        className="section-header",
                        children=[
                            html.Span("AIR QUALITY INDEX", className="section-title"),
                            html.Span(id="aq-status-badge", className="aq-status-badge"),
                        ],
                    ),
                    html.Div(
                        className="aq-body",
                        children=[
                            dcc.Graph(id="air-quality-gauge", config={"displayModeBar": False}, className="aq-gauge"),
                            html.Div(id="air-quality-metrics", className="aq-metric-list"),
                        ],
                    ),
                ],
            ),
        ],
    )
