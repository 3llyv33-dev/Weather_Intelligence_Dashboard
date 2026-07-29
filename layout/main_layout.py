from dash import html, dcc
import dash_bootstrap_components as dbc

from config import DEFAULT_CITY, AUTO_REFRESH_MS
from layout.header import build_header
from layout.sidebar import build_sidebar
from layout.hero import build_hero
from layout.kpi_cards import build_kpi_cards
from layout.charts import build_charts_section
from layout.forecast import build_forecast_section
from layout.insights_panel import build_insights_section
from layout.side_panels import build_side_panels


def build_main_layout():
    return html.Div(
        id="app-root",
        className="atmos-app theme-light",
        children=[
            dcc.Store(id="active-city-store", data=DEFAULT_CITY),
            dcc.Store(id="theme-store", data="light"),
            dcc.Store(id="dashboard-data-store"),
            dcc.Store(id="last-fetch-time-store"),
            dcc.Store(id="fetch-error-store"),
            dcc.Store(id="nav-active-store"),
            dcc.Store(id="globe-state-store"),

            dcc.Location(id="url", refresh=False),

            dcc.Interval(id="load-interval", interval=500, max_intervals=1),
            dcc.Interval(id="ticker-interval", interval=1000, n_intervals=0),
            dcc.Interval(id="auto-refresh-interval", interval=AUTO_REFRESH_MS, n_intervals=0),

            build_header(),
            dbc.Alert(id="error-banner", color="danger", is_open=False, dismissable=True, className="error-banner"),

            html.Div(
                className="app-body",
                children=[
                    build_sidebar(),
                    html.Div(
                        className="main-content",
                        children=[
                            html.Div(
                                className="top-grid",
                                children=[
                                    html.Div(
                                        className="top-grid-main",
                                        children=[build_hero(), build_kpi_cards()],
                                    ),
                                    html.Div(className="top-grid-rail", children=[build_side_panels()]),
                                ],
                            ),
                            build_charts_section(),
                            build_forecast_section(),
                            build_insights_section(),
                            html.Footer(
                                id="section-settings",
                                className="atmos-footer",
                                children=[
                                    html.Div(id="last-updated-label", className="footer-updated"),
                                    html.Div("Data provided by OpenWeatherMap", className="footer-source"),
                                    html.Div("Weather Intelligence Dashboard v1.1.0", className="footer-version"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
