from dash import html
import dash_bootstrap_components as dbc


def build_forecast_section():
    return html.Div(
        id="section-forecast",
        className="forecast-card",
        children=[
            html.Div(
                className="section-header",
                children=[html.Span("7-DAY FORECAST", className="section-title")],
            ),
            html.Div(id="forecast-cards-row", className="forecast-cards-row"),
            dbc.Modal(
                id="forecast-detail-modal",
                is_open=False,
                centered=True,
                className="forecast-modal",
                children=[
                    dbc.ModalHeader(dbc.ModalTitle(id="forecast-modal-title")),
                    dbc.ModalBody(id="forecast-modal-body"),
                ],
            ),
        ],
    )
