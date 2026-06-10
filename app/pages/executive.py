from dash import html,dcc
import plotly.express as px
from app.components.ui import header,card
from app.services import data_loader as dl
from app.services.analytics import risk_scores, inventory_health, oee, capability

def layout():
    risk=risk_scores(dl.suppliers(),dl.purchase_orders()); inv=inventory_health(dl.inventory()); prod=oee(dl.production()); q=capability(dl.quality())
    country=risk.groupby(['region','country'],as_index=False).agg(avg_risk=('risk_score','mean'), exposure=('po_value','sum')).round(1)
    fig1=px.bar(country.sort_values('avg_risk',ascending=False).head(12),x='country',y='avg_risk',color='region',title='Country Risk Exposure')
    fig2=px.line(prod.groupby('date',as_index=False)['oee'].mean(),x='date',y='oee',title='OEE Trend')
    return html.Div([header('Executive Control Tower','End-to-end AI control tower for supplier risk, inventory, quality and IoT health.'),html.Div(className='kpi-grid',children=[card('Avg Supplier Risk',round(risk.risk_score.mean(),1),'Composite risk','yellow'),card('High-Risk Suppliers',int((risk.risk_band=='High').sum()),'Mitigation needed','red'),card('High Stockout SKUs',int((inv.stockout_risk=='High').sum()),'Coverage < 1 month','red'),card('Avg OEE',f"{prod.oee.mean():.1f}%",'Manufacturing effectiveness','green'),card('Critical Cpk',int((q.process_status=='Critical').sum()),'Quality risk','yellow')]),html.Div(className='two-col',children=[dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)])])
