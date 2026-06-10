import numpy as np, pandas as pd
from app.config.settings import PROCESSED_DIR
np.random.seed(42)
REGIONS={'Asia':['China','India','Japan','Vietnam','Thailand','South Korea'],'Europe':['Germany','Poland','Czech Republic','France','Italy'],'North America':['USA','Mexico','Canada']}
COMPONENTS=['Semiconductor','Battery Cell','Steel','Aluminum','Sensor','Wiring Harness','Brake Assembly','Motor Controller','Tire','Infotainment Unit']
PLANTS=['Pune','Chennai','Gurugram','Sanand','Bengaluru EV Plant']

def suppliers(n=100):
    rows=[]
    for i in range(1,n+1):
        region=np.random.choice(list(REGIONS)); country=np.random.choice(REGIONS[region]); comp=np.random.choice(COMPONENTS)
        rows.append(dict(supplier_id=f'S{i:04d}', supplier_name=f'Supplier {i:04d}', region=region, country=country, component=comp, supplier_rating=np.random.randint(50,99), capacity_score=np.random.randint(35,100), lead_time_days=np.random.randint(5,85), country_risk_score=np.random.randint(10,90), geopolitical_dependency_score=np.random.randint(10,95), esg_score=np.random.randint(45,98), payment_terms_days=np.random.choice([30,45,60,90])))
    return pd.DataFrame(rows)

def purchase_orders(sup,n=2200):
    dates=pd.date_range('2025-01-01', periods=365, freq='D'); rows=[]
    for i in range(1,n+1):
        s=sup.sample(1).iloc[0]; po=pd.Timestamp(np.random.choice(dates)); promised=po+pd.Timedelta(days=int(s.lead_time_days)); delay=max(0,int(np.random.normal(s.country_risk_score/18+s.geopolitical_dependency_score/35,4)))
        actual=promised+pd.Timedelta(days=delay); qty=np.random.randint(50,9000); cost=round(np.random.uniform(5,600),2)
        rows.append(dict(po_id=f'PO{i:06d}', supplier_id=s.supplier_id, component=s.component, po_date=po.date(), promised_date=promised.date(), actual_date=actual.date(), quantity=qty, unit_cost=cost, po_value=round(qty*cost,2)))
    return pd.DataFrame(rows)

def inventory():
    rows=[]
    for ci,c in enumerate(COMPONENTS,1):
        for si in range(1,9):
            demand=np.random.randint(700,8000)
            rows.append(dict(sku=f'SKU-{ci:02d}-{si:02d}', component=c, plant=np.random.choice(PLANTS), stock_on_hand=np.random.randint(100,20000), safety_stock=np.random.randint(300,4000), reorder_point=np.random.randint(700,6000), monthly_demand=demand, unit_cost=round(np.random.uniform(8,500),2)))
    return pd.DataFrame(rows)

def shipments(sup,n=1000):
    dates=pd.date_range('2025-01-01', periods=365, freq='D'); carriers=['DHL','Maersk','FedEx','BlueDart','Local Freight','DB Schenker']; rows=[]
    for i in range(1,n+1):
        s=sup.sample(1).iloc[0]; ship=pd.Timestamp(np.random.choice(dates)); transit=np.random.randint(2,30)
        rows.append(dict(shipment_id=f'SHIP{i:06d}', supplier_id=s.supplier_id, origin_country=s.country, destination_plant=np.random.choice(PLANTS), carrier=np.random.choice(carriers), ship_date=ship.date(), delivery_date=(ship+pd.Timedelta(days=int(transit))).date(), transit_days=transit, freight_cost=round(np.random.uniform(500,30000),2)))
    return pd.DataFrame(rows)

def demand_history(inv, months=24):
    rows=[]; dates=pd.date_range('2024-01-01', periods=months, freq='MS')
    for _,r in inv.iterrows():
        base=r.monthly_demand
        for i,d in enumerate(dates):
            val=max(1, base*(1+0.08*np.sin(i/12*6.28))+np.random.normal(0,base*0.08))
            rows.append(dict(month=d.date(), sku=r.sku, component=r.component, plant=r.plant, demand=round(val)))
    return pd.DataFrame(rows)

def production(days=240):
    rows=[]
    for d in pd.date_range('2025-01-01', periods=days):
        for line in ['Line A','Line B','Line C','EV Line','Battery Line']:
            target=np.random.randint(750,1600); actual=int(target*np.random.uniform(.70,1.08)); down=np.random.randint(5,160); scrap=np.random.randint(2,max(8,int(actual*.07)))
            rows.append(dict(date=d.date(), line=line, plant=np.random.choice(PLANTS), planned_minutes=480, downtime_minutes=down, target_output=target, actual_output=actual, scrap_units=scrap, energy_kwh=round(actual*np.random.uniform(.10,.45),2)))
    return pd.DataFrame(rows)

def quality(days=240):
    defects=['Surface Scratch','Dimension Variation','Welding Defect','Sensor Failure','Paint Defect','Assembly Gap']; rows=[]
    for d in pd.date_range('2025-01-01', periods=days):
        for line in ['Line A','Line B','Line C','EV Line','Battery Line']:
            mean=np.random.normal(50,.9); std=np.random.uniform(.15,.9)
            rows.append(dict(date=d.date(), line=line, part_id=f'PART-{np.random.randint(100,999)}', defect_type=np.random.choice(defects), defect_rate=round(np.random.uniform(.003,.10),4), lsl=48.5, usl=51.5, process_mean=round(mean,3), process_std=round(std,3)))
    return pd.DataFrame(rows)

def generate_all_sample_data():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    sup=suppliers(); inv=inventory()
    sup.to_csv(PROCESSED_DIR/'suppliers.csv', index=False); purchase_orders(sup).to_csv(PROCESSED_DIR/'purchase_orders.csv', index=False); inv.to_csv(PROCESSED_DIR/'inventory.csv', index=False); shipments(sup).to_csv(PROCESSED_DIR/'shipments.csv', index=False); demand_history(inv).to_csv(PROCESSED_DIR/'demand_history.csv', index=False); production().to_csv(PROCESSED_DIR/'production.csv', index=False); quality().to_csv(PROCESSED_DIR/'quality.csv', index=False)
    from app.services.iot_simulator import generate_iot_stream
    generate_iot_stream(machines=25, days=3, freq_minutes=5)
