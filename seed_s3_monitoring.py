import boto3
import os
import pandas as pd
from io import BytesIO
from datetime import datetime

# AWS Region (Sydney)
region = 'ap-southeast-2'
bucket_name = 'my-first-mlops-data'

def seed_data():
    print(f"--- Seeding S3 Monitoring Resources ({region}) ---")
    s3 = boto3.client('s3', region_name=region)
    
    # 1. Upload Baseline (train.csv)
    local_train = os.path.join('prediction_model', 'datasets', 'train.csv')
    if os.path.exists(local_train):
        print("Uploading baseline.csv...")
        s3.upload_file(local_train, bucket_name, 'datadrift/baseline.csv')
        print("✅ Baseline uploaded.")
    else:
        print("❌ local train.csv not found.")

    # 2. Generate Today's Data via API
    import requests
    local_test = os.path.join('prediction_model', 'datasets', 'test.csv')
    if os.path.exists(local_test):
        print("Triggering batch prediction to generate today's monitoring data...")
        url = 'http://localhost:8005/batch_prediction'
        try:
            with open(local_test, 'rb') as f:
                res = requests.post(url, files={'file': f})
                if res.status_code == 200:
                    print("✅ Batch prediction successful. S3 folder updated.")
                else:
                    print(f"❌ Batch prediction failed and returned: {res.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    seed_data()
