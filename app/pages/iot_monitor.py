from dash import html,dcc
from app.components.ui import header
from app.services import data_loader as dl

def layout():
    df=dl.iot(); machines=sorted(df.machine_id.unique())
    return html.Div([header('IoT Real-Time Monitor','Synthetic IoT stream for anomaly detection, downtime risk and predictive maintenance.'),dcc.Interval(id='iot-interval',interval=1200,n_intervals=0),html.Div(className='filter-row',children=[html.Div([html.Label('Machine'),dcc.Dropdown(machines,machines[0],id='iot-machine')])]),html.Div(id='iot-kpis',className='kpi-grid'),html.Div(className='two-col',children=[dcc.Graph(id='iot-sensor-chart'),dcc.Graph(id='iot-health-chart')]),dcc.Graph(id='iot-failure-chart')])
