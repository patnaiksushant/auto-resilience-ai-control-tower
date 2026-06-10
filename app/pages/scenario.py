from dash import html,dcc,dash_table
from app.components.ui import header
from app.services import data_loader as dl
from app.services.analytics import risk_scores

def layout():
    r=risk_scores(dl.suppliers(),dl.purchase_orders()); countries=['All']+sorted(r.country.unique()); comps=['All']+sorted(r.component.unique())
    return html.Div([header('Scenario Simulator','Simulate country/component disruption and find alternate suppliers.'),html.Div(className='filter-row',children=[html.Div([html.Label('Country'),dcc.Dropdown(countries,'All',id='sim-country')]),html.Div([html.Label('Component'),dcc.Dropdown(comps,comps[1],id='sim-component')])]),html.Div(id='scenario-kpis',className='kpi-grid'),html.Div(className='two-col',children=[dcc.Graph(id='scenario-chart'),html.Div(id='scenario-text',className='panel')]),html.Div(className='panel',children=[dash_table.DataTable(id='scenario-table',page_size=10,sort_action='native',style_table={'overflowX':'auto'})])])
