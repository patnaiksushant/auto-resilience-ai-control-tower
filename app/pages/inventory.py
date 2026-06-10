from dash import html,dcc,dash_table
import plotly.express as px
from app.components.ui import header,card
from app.services import data_loader as dl
from app.services.analytics import inventory_health

def layout():
    inv=inventory_health(dl.inventory()); fig1=px.pie(inv,names='stockout_risk',values='inventory_value',title='Inventory Value by Risk'); fig2=px.bar(inv.groupby('component',as_index=False)['inventory_value'].sum(),x='component',y='inventory_value',title='Inventory Exposure by Component')
    return html.Div([header('Inventory Forecasting & Exposure','Forecast demand and monitor stockout exposure.'),html.Div(className='kpi-grid',children=[card('Inventory Value',f"${inv.inventory_value.sum():,.0f}",'Total exposure','blue'),card('Reorder SKUs',int((inv.reorder_recommendation=='Reorder').sum()),'Below reorder point','yellow'),card('High Risk SKUs',int((inv.stockout_risk=='High').sum()),'Coverage < 1 month','red')]),html.Div(className='two-col',children=[dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)]),html.Div(className='panel',children=[dash_table.DataTable(columns=[{'name':c,'id':c} for c in inv.columns],data=inv.sort_values('coverage_months').to_dict('records'),page_size=10,filter_action='native',sort_action='native',style_table={'overflowX':'auto'})])])
