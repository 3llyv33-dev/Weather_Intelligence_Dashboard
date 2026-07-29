# Weather Intelligence Dashboard

> Real-time weather analytics dashboard with interactive data visualizations, AI-powered insights, and aviation weather support. Built with **Dash** and **Plotly**.

[Report Issue](https://github.com/3llyv33-dev/Weather_Intelligence_Dashboard/issues)


## Overview

A feature-rich weather intelligence platform that displays current conditions, 7-day forecasts, historical trends, air quality metrics, and aviation weather — all through a modern glassmorphism UI. Designed as a data visualization showcase built on the **Dash** + **Plotly** stack.

The dashboard self-accumulates weather history locally, supports mock data mode for offline demos, and generates natural-language insights and recommendations from computed analytics.

## Features

* **Current Weather** — Temperature, humidity, wind, pressure, visibility, feels-like, sunrise/sunset
* **7-Day Forecast** — Daily high/low temperatures, rain probability, and condition icons
* **Interactive Charts** — Temperature trends, rainfall bars, and weather condition distribution
* **Weather Score** — Composite score (0–100) based on temperature, humidity, wind, pressure, visibility, and rain conditions
* **Comfort Index** — Heat-risk assessment from temperature and humidity
* **Air Quality Index** — US EPA-standard AQI conversion from PM2.5 with pollutant breakdown (PM2.5, PM10, O₃, NO₂, CO)
* **Aviation Weather** — Flight condition rating, crosswind estimate, cloud cover, runway status, and weather risk
* **City Comparison** — Side-by-side temperature trend comparison (up to 3 cities)
* **Natural-Language Insights** — Auto-generated weather insights, recommendations, and alerts
* **Dark Mode** — Full light/dark theme toggle
* **Unit Toggle** — °C / °F instant switching
* **Auto-Refresh** — Periodic data refresh with live "last updated" ticker
* **Export** — Print-to-PDF via browser print stylesheet
* **Interactive Globe** — Orthographic map with city markers and animated city transitions
* **Forecast Drill-Down** — Click any forecast day for a detailed modal view
* **Trend Click Analysis** — Click any temperature trend point for inline detail and matching insight
* **Recently Viewed** — Last 5 cities tracked via browser localStorage
* **Mock Data Mode** — Fully functional without an API key using seeded, realistic mock data

## Tech Stack

| Category     | Technology                         |
| ------------ | ---------------------------------- |
| Frontend     | Dash, Dash Bootstrap Components    |
| Charts       | Plotly, Pandas                     |
| Backend      | Python 3                           |
| Data API     | OpenWeatherMap (REST)              |
| Styling      | Custom CSS (Atmos UI)              |
| Caching      | In-memory TTL cache (10 min)       |
| Persistence  | Local JSON files, browser localStorage |

## Architecture

```
┌─────────────┐
│   Browser   │
│  (Dash UI)  │
└──────┬──────┘
       │  Dash callbacks
       ▼
┌──────────────────────┐
│   callbacks.py       │  ◄── central data-fetch on city change / refresh
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  data/aggregator.py             │  ◄── single entry point + TTL cache
│  get_dashboard_data(city, days) │
└─┬──┬──┬──┬──┬───────────────────┘
  │  │  │  │  │
  ▼  ▼  ▼  ▼  ▼
┌──┐┌──┐┌──┐┌──┐┌──────────┐
│Wx││Hx││An││In││ history/ │
│  ││  ││  ││  ││ *.json   │
│Ap││St││ly││si│└──────────┘
│i ││or││ti││gh│
│  ││e ││cs││ts│
│  ││  ││  ││  │
└──┘└──┘└──┘└──┘
```

### Data Flow

Every dashboard panel is populated from a single structured payload returned by `aggregator.get_dashboard_data(city)`:

```python
{
  "current": {...},
  "forecast": [...],
  "trend_series": [...],
  "statistics": {...},
  "insights": {...},
  "aviation": {...},
  "air_quality": {...},
}
```

The frontend never performs calculations — it only renders what the data layer provides.

## Project Structure

```
weather-dashboard/
├── app.py                      # Entry point, Dash app initialization
├── config.py                   # Atmos UI tokens, popular cities, constants
├── callbacks.py                # All Dash callback wiring
├── requirements.txt
├── .env                        # API key and configuration (excluded from git)
├── .gitignore
├── data/
│   ├── weather_api.py          # OpenWeatherMap HTTP calls + mock generator
│   ├── history_store.py        # Self-accumulating local JSON history
│   ├── analytics.py            # Statistics, comfort index, weather score,
│   │                           # AQI conversion, aviation status
│   ├── insights.py             # Natural-language insights, recommendations, alerts
│   ├── condition_icons.py      # Weather condition → icon/color mapping
│   └── aggregator.py           # Single data entry point with caching
├── layout/
│   ├── header.py               # Top navigation bar
│   ├── sidebar.py              # Navigation + location lists + unit toggle
│   ├── hero.py                 # Current weather hero section
│   ├── kpi_cards.py            # KPI metric cards row
│   ├── charts.py               # Temperature, rainfall, condition chart panels
│   ├── forecast.py             # 7-day forecast + drill-down modal
│   ├── insights_panel.py       # Insights, recommendations, comparison, AQI
│   ├── side_panels.py          # Alerts and aviation panels
│   ├── chart_builders.py       # Plotly figure builders
│   ├── components.py           # Shared UI helper components
│   └── main_layout.py          # Full layout assembly
├── assets/
│   └── style.css               # Atmos UI theme (light + dark modes)
└── data/history/               # Per-city JSON history files (auto-generated)
```

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/3llyv33-dev/Weather_Intelligence_Dashboard.git
cd weather-dashboard

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env         # then edit .env with your API key (optional)
```

### Run

```bash
python app.py
```

Open **http://127.0.0.1:8050** in your browser.

## Configuration

Environment variables are loaded from `.env`:

| Variable                | Description                              | Required |
| ----------------------- | ---------------------------------------- | -------- |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap API key                   | No *     |
| `CACHE_TTL_SECONDS`      | In-memory cache duration (default: 600)  | No       |

_* Mock data is used automatically when no API key is provided._

### Mock Mode

If `OPENWEATHERMAP_API_KEY` is empty, the dashboard runs in **mock mode** using built-in seeded data generators. Every panel populates with realistic, city-varying numbers — no internet connection required.

Get a free API key at [openweathermap.org/api](https://openweathermap.org/api). The Current Weather, 5-Day Forecast, Air Pollution, and Geocoding endpoints are all included in the free tier.

## Interactive Features

| Feature                     | Description                                                   |
| --------------------------- | ------------------------------------------------------------- |
| City Search / Dropdown      | Select any city via search input or dropdown                  |
| Popular Locations           | Sidebar list of pre-configured cities with live temperatures  |
| °C / °F Toggle              | Instant unit switching (no data refetch)                      |
| Dark Mode Toggle            | Full light/dark theme switching                               |
| Time Range Selector         | Switch trend view between Today, 3, 7, and 30 days            |
| Forecast Drill-Down         | Click any forecast day for a detailed modal                   |
| Trend Click Analysis        | Click a temperature trend point for inline detail + insights  |
| City Comparison             | Multi-select checklist (up to 3 cities) with overlay chart    |
| Auto-Refresh                | Background data refresh with live "Last Updated" ticker       |
| Collapsible Sidebar         | Expand/collapse sidebar navigation                            |
| Export                      | Print-to-PDF via browser print stylesheet                     |
| Interactive Globe           | Orthographic map with animated city transitions               |
| "Current Location" Button   | Resets to default city (placeholder for browser geolocation)  |

## Engineering Decisions

- **No historical weather API** — OpenWeatherMap's free tier lacks historical data. `history_store.py` self-accumulates a rolling daily snapshot per city and backfills missing days with seeded, plausible values so trend charts are never empty.
- **No database** — Popular locations are a static config list. Recently viewed cities live in browser `localStorage` via `dcc.Store`. API responses are cached in-memory with a configurable TTL.
- **EPA-standard AQI** — PM2.5 concentration from the Air Pollution API is converted to the US AQI scale using the official EPA breakpoint table.
- **Aviation estimates** — Crosswind is a simplified estimate (generic 45° angle assumption). Runway condition is inferred from current weather conditions. Both are flagged in the UI.
- **Export** — Triggers `window.print()` via a Dash clientside callback — zero server round-trip.

## Known Limitations

- Trend/history data before the first live snapshot is seeded, not real
- "Current Location" resets to the default city rather than using browser geolocation
- Crosswind is estimated, not measured (no runway-heading data source)
- Rounded bar corners are not a native Plotly feature — the rainfall chart uses standard bar tops

## Roadmap

- [x] Initial release (v1.1.0)
- [x] Current weather display
- [x] 7-day forecast
- [x] Temperature trend charts
- [x] Air quality index (US AQI)
- [x] Aviation weather panel
- [x] City comparison
- [x] Dark mode
- [ ] Browser geolocation support
- [ ] Production deployment documentation
- [ ] Expanded test coverage

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test your changes
5. Commit (`git commit -m 'Add my feature'`)
6. Push (`git push origin feature/my-feature`)
7. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

_Weather Intelligence Dashboard v1.1.0 — Built by [Elvictory Victor Kazinja](https://github.com/ellyvee) — Data provided by OpenWeatherMap_
