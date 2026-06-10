import pandas as pd
from app.config.settings import PROCESSED_DIR
from app.services.synthetic_data import generate_all_sample_data
REQ=['suppliers.csv','purchase_orders.csv','inventory.csv','shipments.csv','demand_history.csv','production.csv','quality.csv','iot_sensor_stream.csv']
def ensure():
    if any(not (PROCESSED_DIR/f).exists() for f in REQ): generate_all_sample_data()
def load(name, parse_dates=None): ensure(); return pd.read_csv(PROCESSED_DIR/name, parse_dates=parse_dates)
def suppliers(): return load('suppliers.csv')
def purchase_orders(): return load('purchase_orders.csv', ['po_date','promised_date','actual_date'])
def inventory(): return load('inventory.csv')
def shipments(): return load('shipments.csv', ['ship_date','delivery_date'])
def demand(): return load('demand_history.csv', ['month'])
def production(): return load('production.csv', ['date'])
def quality(): return load('quality.csv', ['date'])
def iot(): return load('iot_sensor_stream.csv', ['timestamp'])
