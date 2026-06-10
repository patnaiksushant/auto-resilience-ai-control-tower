import dash
import dash_bootstrap_components as dbc
from app.config.settings import APP_TITLE

def create_app():
    return dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP], title=APP_TITLE)
