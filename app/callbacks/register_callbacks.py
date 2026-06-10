from app.callbacks.scenario_callbacks import register_scenario_callbacks
from app.callbacks.ml_callbacks import register_ml_callbacks
from app.callbacks.iot_callbacks import register_iot_callbacks

def register_callbacks(app):
    register_scenario_callbacks(app)
    register_ml_callbacks(app)
    register_iot_callbacks(app)
