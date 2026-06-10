from dash import Input,Output,html
import plotly.express as px
from app.components.ui import card
from app.services import data_loader as dl
from app.services.analytics import risk_scores, recommend

def register_scenario_callbacks(app):
    @app.callback(Output('scenario-kpis','children'),Output('scenario-chart','figure'),Output('scenario-text','children'),Output('scenario-table','columns'),Output('scenario-table','data'),Input('sim-country','value'),Input('sim-component','value'))
    def update(country,component):
        r=risk_scores(dl.suppliers(),dl.purchase_orders()); inv=dl.inventory(); impacted=r.copy()
        if country!='All': impacted=impacted[impacted.country==country]
        if component!='All': impacted=impacted[impacted.component==component]
        comps=impacted.component.unique(); inv2=inv[inv.component.isin(comps)].copy(); inv_val=float((inv2.stock_on_hand*inv2.unit_cost).sum()) if len(inv2) else 0
        kpis=[card('Impacted Suppliers',impacted.supplier_id.nunique(),'Supplier count','red'),card('Impacted Components',len(comps),'Component families','yellow'),card('Inventory at Risk',f'${inv_val:,.0f}','Stock exposure','yellow'),card('Avg Risk',round(impacted.risk_score.mean() if len(impacted) else 0,1),'Risk score','red')]
        alt=recommend(r, component if component!='All' else r.component.iloc[0], exclude_country=country if country!='All' else None)
        fig=px.bar(alt.sort_values('recommendation_score'),x='recommendation_score',y='supplier_name',orientation='h',title='Alternate Supplier Ranking') if len(alt) else px.bar(title='No alternate supplier found')
        cols=['supplier_id','supplier_name','country','component','supplier_rating','capacity_score','lead_time_days','risk_score','recommendation_score'] if 'recommendation_score' in alt.columns else list(alt.columns)
        text=html.Ul([html.Li(f'Scenario: {country} / {component}'),html.Li('Prioritize suppliers with lower risk, higher capacity and shorter lead time.'),html.Li('Generate procurement workflow or ERP reorder after planner approval.')])
        return kpis,fig,text,[{'name':c,'id':c} for c in cols],alt[cols].to_dict('records')
