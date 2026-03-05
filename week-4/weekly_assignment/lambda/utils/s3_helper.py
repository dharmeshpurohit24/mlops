import boto3

s3_client = boto3.client('s3')

def download_zip(bucket, key, local_path):
    s3_client.download_file(bucket, key, local_path)

def upload_csv(bucket, key, local_path):
    s3_client.upload_file(local_path, bucket, key)
