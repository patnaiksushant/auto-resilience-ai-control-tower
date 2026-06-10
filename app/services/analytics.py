import numpy as np, pandas as pd

def risk_scores(sup, po):
    x=po.copy(); x['delay_days']=(x.actual_date-x.promised_date).dt.days.clip(lower=0); perf=x.groupby('supplier_id').agg(avg_delay_days=('delay_days','mean'), late_rate=('delay_days',lambda s:(s>0).mean()), po_value=('po_value','sum'), po_count=('po_id','nunique')).reset_index(); df=sup.merge(perf,on='supplier_id',how='left').fillna(0)
    df['risk_score']=(.22*df.country_risk_score+.20*df.geopolitical_dependency_score+.18*(df.avg_delay_days*10).clip(0,100)+.15*(df.late_rate*100)+.10*(100-df.supplier_rating)+.10*(100-df.capacity_score)+.05*(100-df.esg_score)).round(1)
    df['risk_band']=pd.cut(df.risk_score,[-1,35,65,101],labels=['Low','Medium','High']).astype(str)
    return df

def inventory_health(inv):
    df=inv.copy(); df['coverage_months']=(df.stock_on_hand/df.monthly_demand).replace([np.inf,-np.inf],0).round(2); df['inventory_value']=(df.stock_on_hand*df.unit_cost).round(2); df['stockout_risk']=np.where(df.coverage_months<1,'High',np.where(df.coverage_months<2,'Medium','Low')); df['reorder_recommendation']=np.where(df.stock_on_hand<df.reorder_point,'Reorder','No Action'); return df

def oee(prod):
    df=prod.copy(); df['availability']=1-(df.downtime_minutes/df.planned_minutes).clip(0,1); df['performance']=(df.actual_output/df.target_output).clip(0,1.2); df['quality_rate']=1-(df.scrap_units/df.actual_output).clip(0,1); df['oee']=(df.availability*df.performance*df.quality_rate*100).round(1); df['energy_per_unit']=(df.energy_kwh/df.actual_output).replace([np.inf,-np.inf],np.nan).round(3); return df

def capability(q):
    df=q.copy(); sig=df.process_std.replace(0,np.nan); df['cp']=((df.usl-df.lsl)/(6*sig)).round(2); df['cpu']=(df.usl-df.process_mean)/(3*sig); df['cpl']=(df.process_mean-df.lsl)/(3*sig); df['cpk']=df[['cpu','cpl']].min(axis=1).round(2); df['process_status']=np.where(df.cpk<1,'Critical',np.where(df.cpk<1.33,'Watch','Capable')); return df

def recommend(risk, component, exclude_country=None):
    c=risk[risk.component==component].copy()
    if exclude_country: c=c[c.country!=exclude_country]
    if c.empty: return c
    c['lead_time_score']=100-c.lead_time_days.rank(pct=True)*100; c['recommendation_score']=(.35*(100-c.risk_score)+.2*c.supplier_rating+.2*c.capacity_score+.15*c.lead_time_score+.1*c.esg_score).round(1)
    return c.sort_values('recommendation_score', ascending=False).head(10)
