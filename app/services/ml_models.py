import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error, r2_score
from app.services.analytics import risk_scores

def late_delivery_model(sup, po, algo='Random Forest'):
    r=risk_scores(sup,po); x=po.copy(); x['delay_days']=(x.actual_date-x.promised_date).dt.days.clip(lower=0); x['late_flag']=(x.delay_days>0).astype(int); df=x.merge(r[['supplier_id','supplier_rating','capacity_score','lead_time_days','country_risk_score','geopolitical_dependency_score','esg_score','risk_score']],on='supplier_id')
    feats=['quantity','unit_cost','supplier_rating','capacity_score','lead_time_days','country_risk_score','geopolitical_dependency_score','esg_score','risk_score']; X=df[feats].fillna(0); y=df.late_flag
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y if y.nunique()>1 else None)
    model={'Gradient Boosting':GradientBoostingClassifier(random_state=42),'Logistic Regression':LogisticRegression(max_iter=1000),'Random Forest':RandomForestClassifier(n_estimators=160,random_state=42)}.get(algo,RandomForestClassifier(n_estimators=160,random_state=42))
    model.fit(Xtr,ytr); pred=model.predict(Xte); prob=model.predict_proba(Xte)[:,1] if hasattr(model,'predict_proba') else pred
    metrics={'Accuracy':round(accuracy_score(yte,pred),3),'ROC_AUC':round(roc_auc_score(yte,prob),3) if yte.nunique()>1 else None}
    scored=df.copy(); scored['late_probability']=model.predict_proba(X)[:,1] if hasattr(model,'predict_proba') else model.predict(X)
    return metrics, scored.sort_values('late_probability', ascending=False).head(25), feats

def demand_forecast_ml(demand, algo='Random Forest'):
    df=demand.sort_values(['sku','month']).copy(); df['t']=df.groupby('sku').cumcount(); df['lag1']=df.groupby('sku').demand.shift(1); df['lag3']=df.groupby('sku').demand.shift(3); df['roll3']=df.groupby('sku').demand.shift(1).rolling(3).mean().reset_index(level=0,drop=True); train=df.dropna().copy()
    feats=['t','lag1','lag3','roll3']; X=train[feats]; y=train.demand
    model=GradientBoostingRegressor(random_state=42) if algo=='Gradient Boosting' else RandomForestRegressor(n_estimators=160, random_state=42)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42); model.fit(Xtr,ytr); p=model.predict(Xte); metrics={'MAE':round(mean_absolute_error(yte,p),1),'R2':round(r2_score(yte,p),3)}
    latest=train.groupby('sku').tail(1).copy(); latest['forecast_demand']=model.predict(latest[feats]).round(0); return metrics, latest[['sku','component','plant','forecast_demand']].head(50)

def supplier_anomaly(risk):
    feats=['risk_score','supplier_rating','capacity_score','lead_time_days','country_risk_score','geopolitical_dependency_score','avg_delay_days','late_rate']; X=risk[feats].fillna(0); m=IsolationForest(contamination=.08, random_state=42).fit(X); out=risk.copy(); out['anomaly_flag']=(m.predict(X)==-1).astype(int); out['anomaly_score']=m.decision_function(X).round(3); return out.sort_values(['anomaly_flag','risk_score'], ascending=[False,False]).head(30)
