from dash import html

def header(title, subtitle=''):
    return html.Div(className='header', children=[html.H1(title), html.P(subtitle)])

def card(title, value, subtitle='', tone='blue'):
    return html.Div(className=f'card {tone}', children=[html.Div(title, className='card-title'), html.Div(str(value), className='card-value'), html.Div(subtitle, className='card-subtitle')])
