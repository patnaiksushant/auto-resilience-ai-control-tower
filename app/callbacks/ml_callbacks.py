from dash import Input,Output
from app.components.ui import card
from app.services import data_loader as dl
from app.services.ml_models import late_delivery_model

def register_ml_callbacks(app):
    @app.callback(Output('late-ml-metrics','children'),Output('late-ml-table','columns'),Output('late-ml-table','data'),Input('late-algo','value'))
    def update_late(algo):
        metrics, scored, feats = late_delivery_model(dl.suppliers(), dl.purchase_orders(), algo)
        cards=[card(k,v,'Model metric','blue') for k,v in metrics.items()]
        cols=['po_id','supplier_id','component','quantity','unit_cost','delay_days','late_probability']
        return cards,[{'name':c,'id':c} for c in cols],scored[cols].round(3).to_dict('records')
