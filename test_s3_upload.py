import boto3
import sys

def test_upload():
    access_key = input("Enter Access Key: ")
    secret_key = input("Enter Secret Key: ")
    region = 'ap-southeast-2'
    bucket = 'my-first-mlops-data'
    
    try:
        s3 = boto3.client('s3', 
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region)
        
        print("Checking bucket...")
        s3.head_bucket(Bucket=bucket)
        print(f"✅ Bucket '{bucket}' found.")
        
        print("Uploading test file...")
        s3.put_object(Bucket=bucket, Key='test_connection.txt', Body='Connection Successful')
        print("✅ Test upload successful.")
        
        print("Listing datadrift/ folder...")
        response = s3.list_objects_v2(Bucket=bucket, Prefix='datadrift/')
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print(" ❌ datadrift/ folder is empty.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload()
