import time
from datetime import datetime

from dash import html, Input, Output, State, ctx, ALL, no_update
from dash.exceptions import PreventUpdate

from config import DEFAULT_CITY, POPULAR_LOCATIONS
from data import aggregator, insights, weather_api
from data.condition_icons import icon_for_condition

from layout.chart_builders import (
    build_gauge_figure,
    build_temperature_trend_figure,
    build_rainfall_figure,
    build_condition_distribution_figure,
    build_comparison_figure,
    build_air_quality_gauge,
    build_globe_figure,
)
from layout.components import (
    format_temp,
    build_location_list_item,
    build_alert_card,
    build_aviation_stat,
    build_aq_metric,
    build_forecast_detail_body,
)


def _city_coords_global(city_name):
    for loc in POPULAR_LOCATIONS:
        if loc["name"].lower() == city_name.lower():
            return loc["lat"], loc["lon"]
    try:
        return weather_api.geocode_city(city_name)
    except Exception:
        return -6.0, 35.0


def register_callbacks(app):

    @app.callback(
        Output("dashboard-data-store", "data"),
        Output("active-city-store", "data"),
        Output("last-fetch-time-store", "data"),
        Output("fetch-error-store", "data"),
        Input("city-select-dropdown", "value"),
        Input("city-search-input", "n_submit"),
        Input("btn-refresh", "n_clicks"),
        Input("btn-current-location", "n_clicks"),
        Input("time-range-toggle", "value"),
        Input("auto-refresh-interval", "n_intervals"),
        Input({"type": "location-item", "city": ALL}, "n_clicks"),
        State("city-search-input", "value"),
        State("active-city-store", "data"),
    )
    def refresh_dashboard_data(dropdown_city, _search_submits, _refresh_clicks, _loc_clicks,
                                trend_days, _auto_n, location_item_clicks,
                                search_value, active_city):
        triggered = ctx.triggered_id
        city = active_city or DEFAULT_CITY

        if isinstance(triggered, dict) and triggered.get("type") == "location-item":
            if not any(location_item_clicks):
                raise PreventUpdate
            city = triggered["city"]
        elif triggered == "city-search-input" and search_value and search_value.strip():
            city = search_value.strip()
        elif triggered == "city-select-dropdown" and dropdown_city:
            city = dropdown_city
        elif triggered == "btn-current-location":
            city = DEFAULT_CITY

        trend_days_int = int(trend_days) if trend_days else 7

        try:
            data = aggregator.get_dashboard_data(city, trend_days=trend_days_int)
            return data, data["current"]["city"], time.time(), None
        except Exception as exc:
            return no_update, no_update, no_update, str(exc)

    @app.callback(
        Output("error-banner", "children"),
        Output("error-banner", "is_open"),
        Input("fetch-error-store", "data"),
    )
    def render_error_banner(error_message):
        if not error_message:
            return "", False
        return f"\u26a0 {error_message}", True

    @app.callback(
        Output("hero-greeting", "children"),
        Output("hero-city", "children"),
        Output("hero-country", "children"),
        Output("hero-temperature", "children"),
        Output("hero-condition-icon", "children"),
        Output("hero-condition-label", "children"),
        Output("hero-feels-like", "children"),
        Output("hero-comfort-pill", "children"),
        Output("hero-comfort-pill", "className"),
        Output("hero-sunrise", "children"),
        Output("hero-sunset", "children"),
        Output("weather-score-gauge", "figure"),
        Output("weather-score-status", "children"),
        Output("weather-score-status", "className"),
        Input("dashboard-data-store", "data"),
        Input("unit-store", "data"),
    )
    def render_hero(data, unit):
        if not data:
            raise PreventUpdate
        current = data["current"]
        comfort = data["insights"]["comfort_index"]
        score = data["insights"]["weather_score"]

        icon_class = f"bi {icon_for_condition(current['condition'])}"
        comfort_class = f"comfort-pill comfort-{comfort['status'].lower().replace(' ', '-')}"
        status_slug = score["status"].lower().replace(" ", "-")
        status_class = f"score-status status-{status_slug}"

        return (
            _time_greeting(),
            current["city"],
            current.get("country", "") or "\u2014",
            format_temp(current["temperature"], unit),
            html.I(className=icon_class),
            current["condition"],
            f"Feels like {format_temp(current['feels_like'], unit)}",
            f"Comfort: {comfort['status']}",
            comfort_class,
            f"Sunrise {current['sunrise']}",
            f"Sunset {current['sunset']}",
            build_gauge_figure(score["value"], score["status"]),
            [html.I(className="bi bi-check-circle-fill"), f" {score['status']}"],
            status_class,
        )

    @app.callback(
        Output("kpi-value-temperature", "children"),
        Output("kpi-trend-temperature", "children"),
        Output("kpi-value-humidity", "children"),
        Output("kpi-trend-humidity", "children"),
        Output("kpi-value-wind_speed", "children"),
        Output("kpi-trend-wind_speed", "children"),
        Output("kpi-value-visibility", "children"),
        Output("kpi-trend-visibility", "children"),
        Output("kpi-value-pressure", "children"),
        Output("kpi-trend-pressure", "children"),
        Input("dashboard-data-store", "data"),
        Input("unit-store", "data"),
    )
    def render_kpi_cards(data, unit):
        if not data:
            raise PreventUpdate
        current = data["current"]
        stats = data["statistics"]

        delta = round(current["temperature"] - stats["average_temperature"], 1)
        arrow = "\u2191" if delta > 0 else ("\u2193" if delta < 0 else "\u2192")
        temp_trend = f"{arrow} {abs(delta)}\u00b0 vs weekly avg"

        wind_trend = f"{current['wind_direction']} \u00b7 " + ("Moderate" if current["wind_speed"] < 25 else "Strong")
        visibility_trend = "Excellent" if current["visibility"] >= 8 else ("Good" if current["visibility"] >= 5 else "Reduced")
        pressure_trend = "Falling" if stats["temperature_trend"] == "Decreasing" else "Stable"

        return (
            format_temp(current["temperature"], unit), temp_trend,
            f"{current['humidity']}%", stats["humidity_trend"],
            f"{current['wind_speed']} km/h", wind_trend,
            f"{current['visibility']} km", visibility_trend,
            f"{current['pressure']} hPa", pressure_trend,
        )

    @app.callback(
        Output("temperature-trend-chart", "figure"),
        Output("rainfall-chart", "figure"),
        Output("condition-distribution-chart", "figure"),
        Input("dashboard-data-store", "data"),
        Input("unit-store", "data"),
    )
    def render_charts(data, unit):
        if not data:
            raise PreventUpdate
        trend = data["trend_series"]
        stats = data["statistics"]
        return (
            build_temperature_trend_figure(trend, unit),
            build_rainfall_figure(trend),
            build_condition_distribution_figure(stats["condition_distribution"], days=len(trend)),
        )

    @app.callback(
        Output("trend-chart-click-info", "children"),
        Input("temperature-trend-chart", "clickData"),
        State("dashboard-data-store", "data"),
        prevent_initial_call=True,
    )
    def show_trend_click_detail(click_data, data):
        if not click_data or not data:
            raise PreventUpdate
        label = click_data["points"][0]["x"]
        match = next((d for d in data["trend_series"] if d["label"] == label), None)
        if not match:
            raise PreventUpdate
        text = (
            f" {label}: {match['temperature']}\u00b0C \u00b7 {match['condition']} \u00b7 "
            f"Humidity {match['humidity']}% \u00b7 Wind {match['wind_speed']} km/h"
        )
        related = [m for m in data["insights"]["messages"] if label.lower() in m.lower()]
        return html.Div(
            className="chart-click-callout",
            children=[
                html.Div([html.I(className="bi bi-geo-alt-fill"), html.Span(text)]),
                html.Div(related[0], className="chart-click-related") if related else None,
            ],
        )

    @app.callback(
        Output("forecast-cards-row", "children"),
        Input("dashboard-data-store", "data"),
        Input("unit-store", "data"),
    )
    def render_forecast_cards(data, unit):
        if not data:
            raise PreventUpdate
        cards = []
        for i, day in enumerate(data["forecast"]):
            is_today = day["day"] == "Today"
            cards.append(
                html.Div(
                    id={"type": "forecast-card", "index": i},
                    n_clicks=0,
                    className=f"forecast-card-item{' today' if is_today else ''}",
                    children=[
                        html.Div(day["day"], className="forecast-day"),
                        html.Div(day["date"], className="forecast-date"),
                        html.I(className=f"bi {icon_for_condition(day['condition'])} forecast-icon"),
                        html.Div(
                            [
                                html.Span(format_temp(day["high"], unit), className="forecast-high"),
                                html.Span(format_temp(day["low"], unit), className="forecast-low"),
                            ],
                            className="forecast-temps",
                        ),
                        html.Div(
                            [html.I(className="bi bi-droplet-fill"), f" {day['rain_chance']}%"],
                            className="forecast-rain",
                        ),
                    ],
                )
            )
        return cards

    @app.callback(
        Output("forecast-detail-modal", "is_open"),
        Output("forecast-modal-title", "children"),
        Output("forecast-modal-body", "children"),
        Input({"type": "forecast-card", "index": ALL}, "n_clicks"),
        State("dashboard-data-store", "data"),
        State("unit-store", "data"),
        prevent_initial_call=True,
    )
    def open_forecast_detail(n_clicks_list, data, unit):
        if not data or not any(n_clicks_list):
            raise PreventUpdate
        triggered = ctx.triggered_id
        if not isinstance(triggered, dict):
            raise PreventUpdate
        idx = triggered["index"]
        forecast = data.get("forecast", [])
        if idx >= len(forecast):
            raise PreventUpdate
        day = forecast[idx]
        return True, f"{day['day']}, {day['date']}", build_forecast_detail_body(day, unit)

    @app.callback(
        Output("insights-list", "children"),
        Output("recommendations-list", "children"),
        Input("dashboard-data-store", "data"),
    )
    def render_insights(data):
        if not data:
            raise PreventUpdate
        insight_items = [
            html.Div([html.I(className="bi bi-info-circle-fill"), html.Span(msg)], className="insight-item")
            for msg in data["insights"]["messages"]
        ]
        rec_items = [
            html.Div([html.I(className="bi bi-check-circle-fill"), html.Span(msg)], className="insight-item")
            for msg in data["insights"]["recommendations"]
        ]
        return insight_items, rec_items

    @app.callback(
        Output("alerts-list", "children"),
        Input("dashboard-data-store", "data"),
    )
    def render_alerts(data):
        if not data:
            raise PreventUpdate
        alerts = insights.generate_alerts(data["current"], data["statistics"], data["insights"]["weather_score"])
        return [build_alert_card(a) for a in alerts]

    @app.callback(
        Output("aviation-panel-body", "children"),
        Input("dashboard-data-store", "data"),
    )
    def render_aviation(data):
        if not data:
            raise PreventUpdate
        av = data["aviation"]
        current = data["current"]
        badge_color = {"EXCELLENT": "success", "GOOD": "success", "MODERATE": "warning", "POOR": "danger"}.get(
            av["flight_condition"], "secondary"
        )
        return [
            html.Div(
                [
                    html.Span("Flight Condition", className="aviation-label"),
                    html.Span(av["flight_condition"], className=f"badge-pill badge-{badge_color}"),
                ],
                className="aviation-row-header",
            ),
            html.Div(
                className="aviation-grid",
                children=[
                    build_aviation_stat("Visibility", f"{current['visibility']} km",
                                        "Excellent" if current["visibility"] >= 8 else "Moderate"),
                    build_aviation_stat("Cloud Cover", f"{av['cloud_cover_percent']}%",
                                        "Scattered" if av["cloud_cover_percent"] < 50 else "Broken"),
                    build_aviation_stat("Wind", f"{current['wind_speed']} km/h", current["wind_direction"]),
                    build_aviation_stat("Crosswind (est.)", f"{av['crosswind_kmh']} km/h",
                                        "Moderate" if av["crosswind_kmh"] > 15 else "Light"),
                ],
            ),
            html.Div(
                [
                    html.Span("Runway Conditions", className="aviation-label"),
                    html.Span(
                        f"{av['runway_condition']} \u00b7 {av['runway_quality']}",
                        className=f"badge-pill badge-{'success' if av['runway_condition'] == 'DRY' else 'warning'}",
                    ),
                ],
                className="aviation-row",
            ),
            html.Div(
                [html.I(className="bi bi-shield-check"), html.Span(f" Weather Risk: {av['weather_risk']}")],
                className="aviation-risk",
            ),
        ]

    @app.callback(
        Output("air-quality-gauge", "figure"),
        Output("air-quality-metrics", "children"),
        Output("aq-status-badge", "children"),
        Output("aq-status-badge", "className"),
        Input("dashboard-data-store", "data"),
    )
    def render_air_quality(data):
        if not data:
            raise PreventUpdate
        aq = data["air_quality"]
        aqi = aq["aqi"]
        status = aq["status"]
        fig = build_air_quality_gauge(aqi, status)
        if aqi <= 50:
            badge_class = "aq-status-badge aq-good"
        elif aqi <= 100:
            badge_class = "aq-status-badge aq-moderate"
        elif aqi <= 150:
            badge_class = "aq-status-badge aq-unhealthy-sensitive"
        else:
            badge_class = "aq-status-badge aq-unhealthy"
        metrics = [
            build_aq_metric("PM2.5", aq["pm2_5"]),
            build_aq_metric("PM10", aq["pm10"]),
            build_aq_metric("O\u2083", aq["o3"]),
            build_aq_metric("NO\u2082", aq["no2"]),
            build_aq_metric("CO", aq["co"]),
        ]
        return fig, metrics, status, badge_class

    @app.callback(
        Output("comparison-city-checklist", "options"),
        Output("comparison-city-checklist", "value"),
        Input("load-interval", "n_intervals"),
        Input("active-city-store", "data"),
        Input("comparison-city-checklist", "value"),
        State("recently-viewed-store", "data"),
    )
    def manage_comparison_checklist(_n, active_city, selected_cities, recently_viewed):
        try:
            base = [c["name"] for c in POPULAR_LOCATIONS]
            extra = []
            if active_city and active_city not in base:
                extra.append(active_city)
            if recently_viewed:
                for c in recently_viewed:
                    if isinstance(c, str) and c not in base and c not in extra:
                        extra.append(c)
            all_cities = base + extra
            options = [{"label": c, "value": c} for c in all_cities]

            cities = selected_cities or []
            if len(cities) > 3:
                cities = cities[-3:]
            elif not cities:
                cities = all_cities[:3]

            return options, cities
        except Exception:
            base = [c["name"] for c in POPULAR_LOCATIONS]
            options = [{"label": c, "value": c} for c in base]
            return options, base[:3]

    @app.callback(
        Output("city-comparison-chart", "figure"),
        Input("comparison-city-checklist", "value"),
        Input("time-range-toggle", "value"),
        prevent_initial_call=True,
    )
    def render_comparison(selected_cities, trend_days):
        selected_cities = (selected_cities or [])[:3]
        trend_days_int = int(trend_days) if trend_days else 7
        try:
            comparison_data = aggregator.get_comparison_data(selected_cities, trend_days=trend_days_int)
        except Exception:
            comparison_data = {}
        return build_comparison_figure(comparison_data)

    @app.callback(
        Output("popular-locations-list", "children"),
        Input("active-city-store", "data"),
    )
    def render_popular_locations(active_city):
        return [
            build_location_list_item(loc["name"], active=(loc["name"] == active_city))
            for loc in POPULAR_LOCATIONS
        ]

    @app.callback(
        Output("recently-viewed-store", "data"),
        Input("active-city-store", "data"),
        State("recently-viewed-store", "data"),
        prevent_initial_call=True,
    )
    def track_recently_viewed(active_city, current_list):
        current_list = [c for c in (current_list or []) if c != active_city]
        current_list.insert(0, active_city)
        return current_list[:5]

    @app.callback(
        Output("recently-viewed-list", "children"),
        Input("recently-viewed-store", "data"),
    )
    def render_recently_viewed(cities):
        return [build_location_list_item(c, active=False) for c in (cities or [])]

    @app.callback(
        Output("header-clock", "children"),
        Input("clock-interval", "n_intervals"),
    )
    def update_clock(_n):
        now = datetime.now()
        return [
            html.Div(now.strftime("%H:%M"), className="clock-time"),
            html.Div(now.strftime("%a, %d %b %Y"), className="clock-date"),
        ]

    @app.callback(
        Output("last-updated-label", "children"),
        Input("ticker-interval", "n_intervals"),
        State("last-fetch-time-store", "data"),
    )
    def update_last_updated_label(_n, last_fetch_time):
        if not last_fetch_time:
            return [html.I(className="bi bi-arrow-clockwise"), " Last Updated: \u2014"]
        elapsed = int(time.time() - last_fetch_time)
        text = f"{elapsed} seconds ago" if elapsed < 60 else f"{elapsed // 60} minute(s) ago"
        return [html.I(className="bi bi-arrow-clockwise"), f" Last Updated: {text}"]

    @app.callback(
        Output("hero-globe", "figure"),
        Output("globe-state-store", "data"),
        Input("clock-interval", "n_intervals"),
        Input("dashboard-data-store", "data"),
        State("globe-state-store", "data"),
        prevent_initial_call=False,
    )
    def update_globe(n_intervals, data, state):
        if not state or state.get("init") is None:
            state = {
                "lon": 35.0, "lat": -6.0, "scale": 1.0,
                "target_lon": 35.0, "target_lat": -6.0,
                "init": True,
            }

        active_city = DEFAULT_CITY
        if data:
            active_city = data["current"]["city"]
            triggered = ctx.triggered_id

            if triggered == "dashboard-data-store":
                lat, lon = _city_coords_global(active_city)
                state["target_lon"] = lon
                state["target_lat"] = lat
                state["lon"] = lon
                state["lat"] = lat

        drift = (n_intervals or 0) * 0.68
        state["lon"] = state["target_lon"] + drift

        fig = build_globe_figure(
            state["lon"], state["lat"],
            state["scale"], POPULAR_LOCATIONS, active_city,
        )
        return fig, state

    @app.callback(
        Output("city-select-dropdown", "value"),
        Input("hero-globe", "clickData"),
        prevent_initial_call=True,
    )
    def globe_click_to_city(click_data):
        if not click_data:
            raise PreventUpdate
        city = click_data["points"][0].get("text", "")
        if city and any(c["name"] == city for c in POPULAR_LOCATIONS):
            return city
        raise PreventUpdate

    @app.callback(
        Output("atmos-sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("atmos-sidebar", "className"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(_n, current_class):
        if "collapsed" in (current_class or ""):
            return "atmos-sidebar"
        return "atmos-sidebar collapsed"

    @app.callback(
        Output("theme-store", "data"),
        Input("btn-theme-toggle", "n_clicks"),
        State("theme-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_theme(_n, current_theme):
        return "dark" if current_theme == "light" else "light"

    @app.callback(
        Output("app-root", "className"),
        Input("theme-store", "data"),
    )
    def apply_theme(theme):
        return f"atmos-app theme-{theme or 'light'}"

    @app.callback(
        Output("unit-store", "data"),
        Output("unit-toggle-label", "children"),
        Input("unit-toggle-btn", "n_clicks"),
        State("unit-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_unit(_n, current_unit):
        new_unit = "F" if current_unit == "C" else "C"
        return new_unit, f"Switch to \u00b0{'F' if new_unit == 'C' else 'C'}"

    app.clientside_callback(
        "function(hash){var t=hash?hash.replace('#',''):'section-dashboard';document.querySelectorAll('.sidebar-nav-item').forEach(function(e){e.getAttribute('href')==='#'+t?e.classList.add('active'):e.classList.remove('active')});return window.dash_clientside.no_update}",
        Output("nav-active-store", "data"),
        Input("url", "hash"),
    )

    app.clientside_callback(
        "function(n){if(n){window.print()}return window.dash_clientside.no_update}",
        Output("btn-export", "title"),
        Input("btn-export", "n_clicks"),
        prevent_initial_call=True,
    )


def _time_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    if hour < 18:
        return "Good Afternoon"
    return "Good Evening"
