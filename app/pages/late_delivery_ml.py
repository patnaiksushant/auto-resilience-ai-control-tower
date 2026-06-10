from dash import html,dcc,dash_table
from app.components.ui import header

def layout():
    return html.Div([header('Late Delivery Advanced ML','Train ML model to predict supplier late delivery risk.'),html.Div(className='filter-row',children=[html.Div([html.Label('Algorithm'),dcc.Dropdown(['Random Forest','Gradient Boosting','Logistic Regression'],'Random Forest',id='late-algo')])]),html.Div(id='late-ml-metrics',className='kpi-grid'),html.Div(className='panel',children=[html.H3('Top Late Delivery Predictions'),dash_table.DataTable(id='late-ml-table',page_size=12,sort_action='native',style_table={'overflowX':'auto'})])])
