from dash import html
from app.components.ui import header
from app.services import data_loader as dl
from app.services.analytics import risk_scores, inventory_health, oee, capability

def layout():
    r=risk_scores(dl.suppliers(),dl.purchase_orders()); inv=inventory_health(dl.inventory()); p=oee(dl.production()); q=capability(dl.quality())
    acts=[]
    if (r.risk_band=='High').sum()>10: acts.append('Run mitigation workshop for top high-risk suppliers and dual-source critical components.')
    if (inv.stockout_risk=='High').sum()>5: acts.append('Trigger assisted ERP reorder for SKUs with less than one month of coverage.')
    if p.oee.mean()<80: acts.append('Investigate downtime drivers on lowest OEE lines and schedule maintenance review.')
    if (q.process_status=='Critical').sum()>20: acts.append('Open quality containment actions for Cpk-critical lines and defect families.')
    acts.append('Use GenAI/RAG extension to summarize risk drivers, SOPs, meeting actions and supplier mitigation notes.')
    return html.Div([header('AI-Assisted Action Center','Decision recommendations generated from risk, inventory, quality and IoT signals.'),html.Div(className='panel',children=[html.H3('Recommended Actions'),html.Ul([html.Li(a) for a in acts])])])
