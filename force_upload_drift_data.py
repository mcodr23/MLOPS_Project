import boto3
import os
import pandas as pd
from datetime import datetime

# Initialize the S3 client
print("Initializing S3 connection in ap-southeast-2...")
s3 = boto3.client('s3', region_name='ap-southeast-2')
bucket_name = 'my-first-mlops-data'

def push_drift_data():
    local_test_file = os.path.join('prediction_model', 'datasets', 'test.csv')
    
    if not os.path.exists(local_test_file):
        print(f"Error: {local_test_file} not found.")
        return
        
    print(f"Reading {local_test_file}...")
    df = pd.read_csv(local_test_file)
    
    # 1. Provide fake predictions so the Data Quality tab doesn't crash expecting a 'Prediction' column
    print("Generating simulated predictions...")
    import random
    df['Prediction'] = [random.choice(['Y', 'N']) for _ in range(len(df))]
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S").replace(":", "_")
    
    # S3 path matches exactly what the Drift Monitoring app expects: datadrift/YYYY-MM-DD/file.csv
    s3_key = f"datadrift/{current_date}/test_predictions_{current_datetime}.csv"
    
    print(f"Uploading to s3://{bucket_name}/{s3_key}")
    
    csv_buffer = df.to_csv(index=False).encode('utf-8')
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer)
        print("\nSUCCESS! Today's batch prediction data is now on S3.")
        print("You can now refresh your Streamlit dashboard at http://localhost:8501")
    except Exception as e:
        print(f"\nUPLOAD FAILED: {e}")
        print("Please ensure you have set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY before running this script.")

if __name__ == "__main__":
    push_drift_data()
