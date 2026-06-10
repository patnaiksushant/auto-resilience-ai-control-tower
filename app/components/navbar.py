from dash import html, dcc

def sidebar():
    links=[('Executive','/'),('Supply Risk','/supply-risk'),('Late Delivery ML','/late-delivery-ml'),('Inventory Forecast','/inventory'),('Smart Manufacturing','/manufacturing'),('IoT Monitor','/iot-monitor'),('Scenario Simulator','/scenario'),('AI Actions','/actions'),('Data Dictionary','/dictionary')]
    return html.Aside(className='sidebar', children=[html.Div('AutoResilience', className='brand'), html.Div('AI Control Tower', className='subtitle'), html.Nav([dcc.Link(x, href=u, className='nav-link') for x,u in links]), html.Div('Sense → Predict → Optimize → Act', className='footer')])
