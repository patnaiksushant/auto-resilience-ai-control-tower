from dash import html,dcc,dash_table
import plotly.express as px
from app.components.ui import header
from app.services import data_loader as dl
from app.services.analytics import risk_scores

def layout():
    r=risk_scores(dl.suppliers(),dl.purchase_orders()); comp=r.groupby('component',as_index=False).agg(avg_risk=('risk_score','mean'),high_risk=('risk_band',lambda s:(s=='High').sum()),exposure=('po_value','sum')).round(1)
    fig1=px.bar(comp.sort_values('avg_risk',ascending=False),x='component',y='avg_risk',title='Component Risk')
    fig2=px.treemap(r,path=['region','country','component'],values='po_value',color='risk_score',title='Risk Heatmap')
    cols=['supplier_id','supplier_name','region','country','component','supplier_rating','capacity_score','lead_time_days','avg_delay_days','late_rate','risk_score','risk_band']
    return html.Div([header('Supply Risk Intelligence','Detect supplier, country and component risk.'),html.Div(className='two-col',children=[dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)]),html.Div(className='panel',children=[dash_table.DataTable(columns=[{'name':c,'id':c} for c in cols],data=r[cols].sort_values('risk_score',ascending=False).to_dict('records'),page_size=12,filter_action='native',sort_action='native',style_table={'overflowX':'auto'})])])
