import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import COLORS, FONT_FAMILY, WEATHER_SCORE_TIERS


def _base_layout(fig, height=260):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=COLORS["text_secondary"], size=12),
        showlegend=False,
        hoverlabel=dict(bgcolor=COLORS["primary"], font_color="white", font_family=FONT_FAMILY),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False)
    return fig


def _build_ring_gauge(fill_pct: float, color: str, center_html: str, height: int = 170) -> go.Figure:
    fill_pct = max(0.0, min(1.0, fill_pct))
    fig = go.Figure(go.Pie(
        values=[fill_pct, 1 - fill_pct] if fill_pct < 1 else [1, 0.0001],
        hole=0.74,
        marker=dict(colors=[color, COLORS["border"]], line=dict(width=0)),
        textinfo="none",
        hoverinfo="skip",
        direction="clockwise",
        rotation=0,
        sort=False,
    ))
    fig.add_annotation(
        text=center_html, x=0.5, y=0.5, showarrow=False,
        font=dict(family=FONT_FAMILY, color=COLORS["text_primary"]),
        align="center",
    )
    fig.update_layout(
        height=height,
        margin=dict(l=6, r=6, t=6, b=6),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig


def build_gauge_figure(value: int, status: str) -> go.Figure:
    color = next((c for threshold, _, c in WEATHER_SCORE_TIERS if value >= threshold), COLORS["danger"])
    center = (
        f"<b style='font-size:32px'>{value}</b>"
        f"<br><span style='font-size:12px;color:{COLORS['text_secondary']}'>/100</span>"
    )
    return _build_ring_gauge(value / 100, color, center, height=170)


def build_temperature_trend_figure(trend_series: list, unit: str) -> go.Figure:
    df = pd.DataFrame(trend_series)
    df["display_temp"] = df["temperature"] if unit != "F" else df["temperature"] * 9 / 5 + 32
    fig = px.line(df, x="label", y="display_temp", markers=True)
    fig.update_traces(
        line=dict(color=COLORS["accent"], width=3, shape="spline"),
        marker=dict(size=7, color=COLORS["secondary"]),
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.12)",
        hovertemplate="%{x}<br>%{y:.1f}\u00b0" + unit + "<extra></extra>",
    )
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    return _base_layout(fig)


def build_rainfall_figure(trend_series: list) -> go.Figure:
    df = pd.DataFrame(trend_series)
    fig = px.bar(df, x="label", y="rainfall_mm")
    fig.update_traces(
        marker=dict(color=COLORS["accent"]),
        marker_line_width=0,
        hovertemplate="%{x}<br>%{y:.1f} mm<extra></extra>",
    )
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    return _base_layout(fig)


_CONDITION_COLOR_MAP = {
    "sunny": COLORS["warning"],
    "clear": COLORS["warning"],
    "cloudy": COLORS["accent"],
    "clouds": COLORS["accent"],
    "mostly cloudy": COLORS["secondary"],
    "overcast": COLORS["text_secondary"],
    "rainy": COLORS["secondary"],
    "rain": COLORS["secondary"],
    "drizzle": COLORS["secondary"],
    "thunderstorm": COLORS["info"],
    "fog": COLORS["text_secondary"],
    "mist": COLORS["text_secondary"],
    "haze": COLORS["text_secondary"],
    "smoke": COLORS["text_secondary"],
    "dust": COLORS["text_secondary"],
    "sand": COLORS["text_secondary"],
    "ash": COLORS["text_secondary"],
    "squall": COLORS["info"],
    "tornado": COLORS["danger"],
    "wind": COLORS["text_secondary"],
    "snow": COLORS["accent"],
    "sleet": COLORS["secondary"],
}


def build_condition_distribution_figure(distribution: dict, days: int) -> go.Figure:
    if not distribution:
        distribution = {"unknown": 100}
    labels = list(distribution.keys())
    values = list(distribution.values())
    colors = [_CONDITION_COLOR_MAP.get(label, COLORS["text_secondary"]) for label in labels]

    fig = go.Figure(go.Pie(
        labels=[label.title() for label in labels],
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{value}%<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b style='font-size:26px'>{days}</b><br><span style='font-size:11px'>Days</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=COLORS["text_primary"], family=FONT_FAMILY),
    )
    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="v", x=1.05, y=0.5, font=dict(size=11, family=FONT_FAMILY)),
    )
    return fig


def build_comparison_figure(comparison_data: dict) -> go.Figure:
    fig = go.Figure()
    if not comparison_data:
        fig.add_annotation(
            text="Select cities above to compare temperature trends",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=COLORS["text_secondary"], family=FONT_FAMILY),
        )
    else:
        palette = [COLORS["accent"], COLORS["warning"], COLORS["success"]]
        for i, (city, payload) in enumerate(comparison_data.items()):
            df = pd.DataFrame(payload["trend_series"])
            if df.empty:
                continue
            fig.add_trace(go.Scatter(
                x=df["label"], y=df["temperature"], mode="lines+markers", name=city,
                line=dict(color=palette[i % len(palette)], width=2.5),
                marker=dict(size=6),
            ))
    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.18, font=dict(size=11, family=FONT_FAMILY)),
        font=dict(family=FONT_FAMILY, color=COLORS["text_secondary"], size=12),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"], title="\u00b0C")
    return fig


def build_air_quality_gauge(aqi: int, status: str) -> go.Figure:
    if aqi <= 50:
        color = COLORS["success"]
    elif aqi <= 100:
        color = COLORS["warning"]
    elif aqi <= 150:
        color = "#F97316"
    else:
        color = COLORS["danger"]
    fill_pct = max(0.0, min(1.0, 1 - (aqi / 150)))
    center = (
        f"<b style='font-size:26px'>{aqi}</b>"
        f"<br><span style='font-size:10.5px;color:{COLORS['text_secondary']}'>AQI</span>"
    )
    return _build_ring_gauge(fill_pct, color, center, height=150)


def build_globe_figure(rotation_lon: float, rotation_lat: float,
                       scale: float, cities: list,
                       active_city: str = None) -> go.Figure:
    fig = go.Figure()

    lons = [c["lon"] for c in cities]
    lats = [c["lat"] for c in cities]
    names = [c["name"] for c in cities]

    city_color = "rgba(56, 189, 248, 0.7)"
    active_color = COLORS["warning"]

    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats,
        mode="markers",
        marker=dict(size=8, color=city_color,
                    line=dict(width=1, color="white")),
        text=names, hoverinfo="text",
        showlegend=False,
    ))

    if active_city:
        match = next((c for c in cities if c["name"] == active_city), None)
        if match:
            alat, alon = match["lat"], match["lon"]
            # Outer glow ring
            fig.add_trace(go.Scattergeo(
                lon=[alon], lat=[alat],
                mode="markers",
                marker=dict(size=60, color=active_color,
                            opacity=0.08, symbol="circle",
                            line=dict(width=0)),
                showlegend=False, hoverinfo="skip",
            ))
            # Mid glow ring
            fig.add_trace(go.Scattergeo(
                lon=[alon], lat=[alat],
                mode="markers",
                marker=dict(size=36, color=active_color,
                            opacity=0.18, symbol="circle",
                            line=dict(width=0)),
                showlegend=False, hoverinfo="skip",
            ))
            # Inner glow
            fig.add_trace(go.Scattergeo(
                lon=[alon], lat=[alat],
                mode="markers",
                marker=dict(size=20, color=active_color,
                            opacity=0.4, symbol="circle",
                            line=dict(width=0)),
                showlegend=False, hoverinfo="skip",
            ))
            # Core dot
            fig.add_trace(go.Scattergeo(
                lon=[alon], lat=[alat],
                mode="markers",
                marker=dict(size=10, color="#ffffff",
                            line=dict(width=2, color=active_color)),
                showlegend=False, hoverinfo="skip",
            ))
            # City name label next to the active dot
            fig.add_trace(go.Scattergeo(
                lon=[alon + 2.5], lat=[alat + 1.5],
                mode="text",
                text=[active_city],
                textfont=dict(size=12, color="#ffffff",
                              family=FONT_FAMILY),
                showlegend=False, hoverinfo="skip",
            ))

    fig.update_layout(
        geo=dict(
            projection=dict(
                type="orthographic",
                rotation=dict(lon=rotation_lon, lat=rotation_lat, roll=0),
                scale=scale,
            ),
            showland=True, landcolor=COLORS["secondary"],
            showocean=True, oceancolor=COLORS["primary"],
            showcountries=False,
            coastlinecolor=COLORS["accent"], coastlinewidth=0.6,
            showframe=False,
            showlakes=False,
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


