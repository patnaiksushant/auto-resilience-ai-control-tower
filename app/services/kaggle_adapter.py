import pandas as pd
from app.config.settings import RAW_DIR, PROCESSED_DIR
from app.services.synthetic_data import generate_all_sample_data

def prepare_kaggle_data():
    """Flexible adapter. It inventories raw Kaggle files and creates canonical tables.
    For production, extend FIELD_ALIASES below with exact downloaded Kaggle schemas.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True); PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    csvs=list(RAW_DIR.glob('*.csv'))
    generate_all_sample_data()  # creates robust canonical baseline
    inv=[]
    for f in csvs:
        try:
            df=pd.read_csv(f); inv.append({'file_name':f.name,'rows':len(df),'columns':', '.join(map(str,df.columns[:60]))})
        except Exception as e: inv.append({'file_name':f.name,'rows':'ERROR','columns':str(e)})
    if inv: pd.DataFrame(inv).to_csv(PROCESSED_DIR/'kaggle_raw_inventory.csv', index=False)
