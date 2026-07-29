import os
import certifi

os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

import dash
import dash_bootstrap_components as dbc

from layout.main_layout import build_main_layout
import callbacks

BOOTSTRAP_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800&"
    "family=Manrope:wght@400;600;700&"
    "family=Poppins:wght@500;600;700&display=swap"
)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, BOOTSTRAP_ICONS, GOOGLE_FONTS],
    suppress_callback_exceptions=True,
    title="Weather Intelligence Dashboard",
    update_title=None,
)
server = app.server

app.layout = build_main_layout()

callbacks.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
