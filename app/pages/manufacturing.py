from dash import html,dcc,dash_table
import plotly.express as px
from app.components.ui import header,card
from app.services import data_loader as dl
from app.services.analytics import oee, capability

def layout():
    p=oee(dl.production()); q=capability(dl.quality()); fig1=px.line(p.groupby(['date','line'],as_index=False)['oee'].mean(),x='date',y='oee',color='line',title='OEE by Line'); fig2=px.box(q,x='line',y='cpk',color='process_status',title='Cpk Distribution'); fig3=px.bar(q.groupby('defect_type',as_index=False)['defect_rate'].mean().sort_values('defect_rate',ascending=False),x='defect_type',y='defect_rate',title='Defect Rate')
    return html.Div([header('Smart Manufacturing Quality','Track OEE, downtime, energy, Cp/Cpk and defects.'),html.Div(className='kpi-grid',children=[card('Avg OEE',f"{p.oee.mean():.1f}%",'Effectiveness','green'),card('Avg Energy/Unit',round(p.energy_per_unit.mean(),3),'kWh/unit','blue'),card('Critical Cpk',int((q.process_status=='Critical').sum()),'Cpk<1','red'),card('Avg Defect Rate',f"{q.defect_rate.mean()*100:.2f}%",'Quality loss','yellow')]),html.Div(className='two-col',children=[dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)]),dcc.Graph(figure=fig3),html.Div(className='panel',children=[dash_table.DataTable(columns=[{'name':c,'id':c} for c in ['date','line','part_id','defect_type','defect_rate','cp','cpk','process_status']],data=q.sort_values('cpk').head(100).to_dict('records'),page_size=10,style_table={'overflowX':'auto'})])])
