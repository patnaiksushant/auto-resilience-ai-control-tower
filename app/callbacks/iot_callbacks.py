from dash import Input,Output
import plotly.express as px
from app.components.ui import card
from app.services import data_loader as dl

def register_iot_callbacks(app):
    @app.callback(Output('iot-kpis','children'),Output('iot-sensor-chart','figure'),Output('iot-health-chart','figure'),Output('iot-failure-chart','figure'),Input('iot-interval','n_intervals'),Input('iot-machine','value'))
    def update(n,machine):
        df=dl.iot().sort_values('timestamp'); x=df[df.machine_id==machine].reset_index(drop=True); end=min(max(30,(n+1)*4),len(x)); live=x.iloc[max(0,end-150):end]; latest=live.iloc[-1]
        k=[card('Status',latest.machine_status,'Current','blue'),card('Health',latest.health_score,'0-100','green' if latest.health_score>65 else 'red'),card('Anomaly',latest.anomaly_flag,'Sensor flag','red' if latest.anomaly_flag else 'green'),card('Downtime Risk',latest.downtime_risk,'Risk flag','red' if latest.downtime_risk else 'green'),card('RUL Hours',latest.predicted_rul_hours,'Remaining useful life','yellow')]
        long=live.melt(id_vars=['timestamp'],value_vars=['temperature_c','vibration_mm_s','humidity_pct','pressure_bar','energy_kwh'],var_name='sensor',value_name='value')
        return k,px.line(long,x='timestamp',y='value',color='sensor',title=f'Live Sensor Trend: {machine}'),px.line(live,x='timestamp',y='health_score',title='Health Score'),px.histogram(live,x='failure_mode',color='machine_status',title='Failure Mode Distribution')
