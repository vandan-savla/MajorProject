import pandas as pd
import joblib
import time
import csv
import os

class MLModel:
    def __init__(self, model_file):
        self.model = joblib.load(model_file)

    def predict(self, data):
        return self.model.predict(data)

def process_row(row, model):
    # Select the required features from the row
    #rows are repeated
    features = [
        row['bwd_pkt_len_std'],
        row['pkt_len_std'],
        row['bwd_pkt_len_max'],
        row['pkt_size_avg'],
        row['bwd_seg_size_mean'],
        row['pkt_len_max'],
        row['init_fwd_win_bytes'],
        row['pkt_len_mean'],
        row['fwd_header_len'],
        row['bwd_pkt_len_mean'],
        row['pkt_len_var'],
        row['bwd_header_len'],
        row['tot_bwd_pkts'],
        row['fwd_header_len'],
        row['totlen_bwd_pkts'],
        row['fwd_pkt_len_max'],
        row['tot_bwd_pkts'],
        row['init_bwd_win_byts'],
        row['totlen_fwd_pkts'],
        row['tot_fwd_pkts'],
        row['fwd_pkt_len_mean'],
        row['bwd_pkt_len_min'],
        row['totlen_fwd_pkts'],
        row['idle_max'],
        row['pkt_len_min'],
        row['fwd_pkt_len_min'],
        row['fwd_iat_max'],
        row['fwd_seg_size_mean'],
        row['fwd_iat_std'],
        row['flow_iat_max']
    ]

    # Convert features to a list of floats
    features = [float(feature) for feature in features]

    # Make predictions
    predictions = model.predict([features])

    # Return predictions
    return predictions[0]

def main(csv_file, model_file):
    model = MLModel(model_file)
    last_read_size = 0

    while True:
        try:
            # Check if the CSV file has been modified
            file_size = os.path.getsize(csv_file)
            if file_size > last_read_size:
                # Read the new data from the CSV file
                with open(csv_file, 'r') as f:
                    f.seek(last_read_size)
                    csv_reader = csv.DictReader(f)
                    for row in csv_reader:
                        # Process each new row and make predictions
                        prediction = process_row(row, model)
                        print(f"Prediction: {prediction}")

                # Update the last read size
                last_read_size = file_size

            # Add a delay before checking for new data again
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopping real-time prediction...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle the error or continue processing

if __name__ == "__main__":
    csv_file = './output_flows/eth0.csv'  # Replace 'data.csv' with your CSV file path
    model_file = 'model.pkl'  # Replace 'model.pkl' with your model file path

    main(csv_file, model_file)

