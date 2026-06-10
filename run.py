import argparse
from app.services.synthetic_data import generate_all_sample_data
from app.services.kaggle_adapter import prepare_kaggle_data
from app.services.iot_simulator import generate_iot_stream

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-sample-data', action='store_true')
    parser.add_argument('--prepare-kaggle-data', action='store_true')
    parser.add_argument('--generate-iot-stream', action='store_true')
    parser.add_argument('--machines', type=int, default=25)
    parser.add_argument('--days', type=int, default=5)
    parser.add_argument('--freq-minutes', type=int, default=1)
    args = parser.parse_args()
    if args.generate_sample_data:
        generate_all_sample_data()
        print('Generated sample data.')
    elif args.prepare_kaggle_data:
        prepare_kaggle_data()
        print('Prepared Kaggle data into canonical tables.')
    elif args.generate_iot_stream:
        generate_iot_stream(machines=args.machines, days=args.days, freq_minutes=args.freq_minutes)
        print('Generated IoT stream.')
    else:
        from app.main import app
        app.run_server(debug=True, port=8050)
if __name__ == '__main__': main()
