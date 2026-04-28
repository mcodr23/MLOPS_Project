import boto3

def check_s3():
    try:
        s3 = boto3.client('s3', region_name='ap-southeast-2')
        response = s3.list_objects_v2(Bucket='my-first-mlops-data', Prefix='datadrift/')
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"Found: {obj['Key']}")
        else:
            print("Bucket/Prefix is empty.")
    except Exception as e:
        print(f"Error accessing S3: {e}")

if __name__ == "__main__":
    check_s3()
