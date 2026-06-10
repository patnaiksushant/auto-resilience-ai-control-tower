from dash import html, dcc, Input, Output
from app.app_factory import create_app
from app.components.navbar import sidebar
from app.pages import executive, supply_risk, late_delivery_ml, inventory, manufacturing, iot_monitor, scenario, actions, dictionary
from app.callbacks.register_callbacks import register_callbacks

app = create_app()
server = app.server
app.layout = html.Div([dcc.Location(id='url'), html.Div(className='shell', children=[sidebar(), html.Main(id='page-content', className='content')])])

@app.callback(Output('page-content','children'), Input('url','pathname'))
def route(path):
    if path == '/supply-risk': return supply_risk.layout()
    if path == '/late-delivery-ml': return late_delivery_ml.layout()
    if path == '/inventory': return inventory.layout()
    if path == '/manufacturing': return manufacturing.layout()
    if path == '/iot-monitor': return iot_monitor.layout()
    if path == '/scenario': return scenario.layout()
    if path == '/actions': return actions.layout()
    if path == '/dictionary': return dictionary.layout()
    return executive.layout()

register_callbacks(app)
