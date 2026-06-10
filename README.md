# AutoResilience Full Kaggle Dash

Enterprise-style Python Dash prototype for **AI for Resilient Automotive Supply Chains & Smart Manufacturing**.

It is built to use the seven Kaggle datasets listed below and also includes a synthetic fallback generator so the app runs immediately when Kaggle files are not downloaded yet.

## Kaggle Data Sources and How They Are Used

| Dataset | Intended Use in Solution | Standardized Output Tables |
|---|---|---|
| Supply Chain Management for Car | Automotive-specific supplier, car/component and procurement context | suppliers, purchase_orders, inventory |
| General Supply Chain Dataset | Sales/order/logistics style demand and supply-chain analytics | purchase_orders, inventory, demand_history |
| Logistics and Supply Chain Dataset | Shipment, route, carrier and delivery performance | shipments, late_delivery_features |
| Smart Logistics Supply Chain Dataset | Smart logistics events, delivery risk, route risk and real-time logistics patterns | shipments, logistics_events |
| Smart Manufacturing Maintenance Dataset | Predictive maintenance, machine health and downtime analysis | production, maintenance_events |
| Smart Manufacturing IoT-Cloud Monitoring Dataset | IoT sensor stream for anomaly detection and downtime risk | iot_sensor_stream |
| Predicting Manufacturing Defects Dataset | Defect prediction and quality analytics | quality, defect_features |

Place downloaded Kaggle CSVs in `app/data/raw/`. The adapter scans all CSVs and creates a canonical data model in `app/data/processed/`. Because Kaggle schemas vary by version, the adapter uses flexible column matching and falls back to synthetic automotive data when a table cannot be inferred.

## Business Capabilities

- Detect supplier and country risk
- Predict late deliveries
- Forecast demand and inventory exposure
- Recommend alternate suppliers
- Simulate country/component disruption scenarios
- Monitor Cp/Cpk and manufacturing defects
- Track OEE, downtime, energy and machine health
- Generate IoT synthetic real-time streams
- Enable AI-assisted action recommendations

## Project Structure

```text
autoresilience_full_kaggle_dash/
├── app/
│   ├── main.py
│   ├── app_factory.py
│   ├── callbacks/
│   │   ├── register_callbacks.py
│   │   ├── scenario_callbacks.py
│   │   ├── ml_callbacks.py
│   │   └── iot_callbacks.py
│   ├── components/
│   ├── config/
│   ├── pages/
│   ├── services/
│   ├── data/raw/
│   └── data/processed/
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   └── ml_methods.md
├── requirements.txt
└── run.py
```

## Quick Start

```bash
cd autoresilience_full_kaggle_dash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate      # Windows
pip install -r requirements.txt
python run.py --generate-sample-data
python run.py
```

Open `http://127.0.0.1:8050`.

## Prepare Kaggle Data

```bash
# Put Kaggle CSV files under app/data/raw/
python run.py --prepare-kaggle-data
python run.py
```

## IoT Real-Time Synthetic Stream

```bash
python run.py --generate-iot-stream --machines 30 --days 5 --freq-minutes 1
```

The generated stream is written to:

```text
app/data/processed/iot_sensor_stream.csv
```

## Advanced ML / AI Methods Included

| Use Case | Algorithms / Methods |
|---|---|
| Supplier risk scoring | Weighted score + Random Forest + Gradient Boosting-ready feature frame |
| Late delivery prediction | Random Forest Classifier, Gradient Boosting Classifier, Logistic Regression |
| Demand forecasting | Exponential smoothing fallback + Random Forest / Gradient Boosting lag-feature forecast |
| Supplier anomaly detection | Isolation Forest |
| Alternate supplier recommendation | Multi-criteria scoring with risk, rating, capacity, lead time and ESG |
| Disruption simulation | What-if exposure model by country/component |
| Manufacturing quality | Cp, Cpk, SPC status, defect severity ranking |
| IoT anomaly detection | Rule-based labels + Isolation Forest-ready sensor features |
| AI-assisted action recommendation | Rule-based action engine designed to be replaced by GenAI/RAG |

## Pages

1. Executive Control Tower
2. Supply Risk Intelligence
3. Late Delivery ML
4. Inventory Forecasting
5. Smart Manufacturing Quality
6. IoT Real-Time Monitor
7. Scenario Simulator
8. AI Action Center
9. Data Dictionary
