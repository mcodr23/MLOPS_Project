import boto3
import os
import sys
import pandas as pd
from io import BytesIO

def setup_s3_drift_basics():
    bucket_name = 'my-first-mlops-data'
    s3 = boto3.client('s3')
    
    # Path to local train.csv
    local_baseline = os.path.join('prediction_model', 'datasets', 'train.csv')
    s3_baseline_key = 'datadrift/baseline.csv'
    
    if not os.path.exists(local_baseline):
        print(f"Error: Local baseline file {local_baseline} not found.")
        return False
    
    try:
        # 1. Upload Baseline
        print(f"Uploading {local_baseline} to s3://{bucket_name}/{s3_baseline_key}...")
        s3.upload_file(local_baseline, bucket_name, s3_baseline_key)
        print("Baseline upload successful.")
        
        # 2. Ensure we have at least one data folder for today
        # We don't necessarily need to do this here, the PS1 script can trigger the API.
        return True
    except Exception as e:
        print(f"S3 Setup Error: {e}")
        return False

if __name__ == "__main__":
    if setup_s3_drift_basics():
        sys.exit(0)
    else:
        sys.exit(1)
