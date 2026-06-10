import numpy as np, pandas as pd
from app.config.settings import PROCESSED_DIR
np.random.seed(7)
MACHINE_TYPES={'CNC':(58,6,22,5,3.1,.35,2.8,.6),'RobotArm':(52,5,18,4,2.5,.25,2.1,.45),'PressMachine':(65,7,34,7,4.0,.45,3.6,.7),'Compressor':(70,8,38,8,4.5,.55,4.1,.8),'Conveyor':(48,4,15,4,2.2,.2,1.7,.35)}
PLANTS=['Pune','Chennai','Gurugram','Bengaluru EV Plant']; LINES=['Line A','Line B','Line C','EV Line','Battery Line']; FAIL=['None','Overheating','Bearing Wear','Pressure Leak','Electrical Overload','Humidity Exposure']

def shift(h): return 'A' if 6<=h<14 else ('B' if 14<=h<22 else 'C')
def generate_iot_stream(machines=25, days=3, freq_minutes=5):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True); rows=[]; ts=pd.date_range(pd.Timestamp.now().floor('min')-pd.Timedelta(days=days), periods=int(days*24*60/freq_minutes), freq=f'{freq_minutes}min')
    master=[]
    for i in range(1,machines+1): master.append(dict(machine_id=f'MCH-{i:04d}', machine_type=np.random.choice(list(MACHINE_TYPES)), plant=np.random.choice(PLANTS), line=np.random.choice(LINES), age_years=round(np.random.uniform(.5,12),1), criticality=np.random.choice(['Low','Medium','High'],p=[.25,.5,.25])))
    for m in master:
        degr=np.random.uniform(0,8)
        for idx,t in enumerate(ts):
            isrun=np.random.rand() < (.82 if shift(t.hour) in ['A','B'] else .55); load=float(np.clip(np.random.normal(72 if isrun else 20,12),5,100)); p=MACHINE_TYPES[m['machine_type']]
            temp=np.random.normal(p[0],p[1])+12*load/100+degr*idx/len(ts)*.7; vib=np.random.normal(p[2],p[3])+8*load/100+degr*idx/len(ts)*.9; hum=np.random.normal(42,7); pressure=np.random.normal(p[4],p[5])+0.25*load/100; energy=max(.2,np.random.normal(p[6],p[7])+1.2*load/100)
            mode='None'
            if np.random.rand()<.06:
                mode=np.random.choice(FAIL[1:]); sev=np.random.uniform(.5,1.5)
                if mode=='Overheating': temp+=18*sev; energy+=1.2*sev
                elif mode=='Bearing Wear': vib+=24*sev; energy+=.5*sev
                elif mode=='Pressure Leak': pressure-=1.3*sev; vib+=8*sev
                elif mode=='Electrical Overload': energy+=2*sev; temp+=10*sev
                elif mode=='Humidity Exposure': hum+=20*sev; vib+=4*sev
            stress=max(0,(temp-80)/25)*25+max(0,(vib-45)/25)*25+max(0,(hum-65)/25)*10+max(0,(2-pressure)/1.5)*20+max(0,(energy-5)/3)*20+m['age_years']*1.2+(5 if m['criticality']=='High' else 0); stress=float(np.clip(stress,0,100)); health=round(100-stress,1)
            status='Failure' if stress>=75 else ('Warning' if stress>=45 else ('Running' if isrun else 'Idle'))
            rows.append({**m,'timestamp':t,'shift':shift(t.hour),'machine_status':status,'load_pct':round(load,1),'temperature_c':round(float(np.clip(temp,20,130)),2),'vibration_mm_s':round(float(np.clip(vib,1,90)),2),'humidity_pct':round(float(np.clip(hum,10,95)),2),'pressure_bar':round(float(np.clip(pressure,.5,7)),2),'energy_kwh':round(float(np.clip(energy,.2,9)),2),'failure_mode':mode,'anomaly_flag':int(stress>=35),'downtime_risk':int(stress>=55),'maintenance_required':int(stress>=65),'predicted_rul_hours':round(max(5,800-stress*9-m['age_years']*18+np.random.normal(0,25)),1),'health_score':health})
    df=pd.DataFrame(rows); df.to_csv(PROCESSED_DIR/'iot_sensor_stream.csv', index=False); return df
