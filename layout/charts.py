from dash import html, dcc
import dash_bootstrap_components as dbc

from config import TIME_RANGES


def build_charts_section():
    return html.Div(
        id="section-analytics",
        className="charts-row",
        children=[
            html.Div(
                className="chart-card chart-card-wide",
                children=[
                    html.Div(
                        className="chart-card-header",
                        children=[
                            html.Span("TEMPERATURE TREND", className="chart-title"),
                            dbc.RadioItems(
                                id="time-range-toggle",
                                className="time-range-toggle btn-group",
                                inputClassName="btn-check",
                                labelClassName="time-range-label",
                                labelCheckedClassName="active",
                                options=[{"label": r["label"], "value": r["value"]} for r in TIME_RANGES],
                                value="7",
                            ),
                        ],
                    ),
                    dcc.Graph(id="temperature-trend-chart", config={"displayModeBar": False}),
                    html.Div(id="trend-chart-click-info", className="chart-click-info"),
                ],
            ),
            html.Div(
                className="chart-card",
                children=[
                    html.Div(
                        className="chart-card-header",
                        children=[
                            html.Span("RAINFALL (mm)", className="chart-title"),
                            html.Span(id="rainfall-subtitle", className="chart-subtitle"),
                        ],
                    ),
                    dcc.Graph(id="rainfall-chart", config={"displayModeBar": False}),
                ],
            ),
            html.Div(
                className="chart-card",
                children=[
                    html.Div(
                        className="chart-card-header",
                        children=[
                            html.Span("WEATHER CONDITION DISTRIBUTION", className="chart-title"),
                            html.Span(id="condition-subtitle", className="chart-subtitle"),
                        ],
                    ),
                    dcc.Graph(id="condition-distribution-chart", config={"displayModeBar": False}),
                ],
            ),
        ],
    )
