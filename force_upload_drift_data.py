import boto3
import os
import pandas as pd
from io import BytesIO
from datetime import datetime

def force_seed():
    print("--- Force Seeding Today's Monitoring Data ---")
    region = 'ap-southeast-2'
    bucket_name = 'my-first-mlops-data'
    
    # Use environment variables (which you provided in the launcher)
    s3 = boto3.client('s3', region_name=region)
    
    # 1. Prepare today's folder path
    current_date = datetime.now().strftime("%Y-%m-%d")
    s3_folder = f"datadrift/{current_date}/"
    s3_key = f"{s3_folder}manual_demo_data.csv"
    
    # 2. Use test.csv as the 'recent' data
    local_test = os.path.join('prediction_model', 'datasets', 'test.csv')
    if os.path.exists(local_test):
        df = pd.read_csv(local_test)
        # Add a fake prediction column to satisfy the dashboard
        df['Prediction'] = 'Y' 
        
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        
        print(f"Uploading to {s3_key}...")
        try:
            s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
            print(f"✅ Successfully created today's folder: {s3_folder}")
        except Exception as e:
            print(f"❌ Failed to upload: {e}")
    else:
        print("❌ local test.csv not found.")

if __name__ == "__main__":
    force_seed()
