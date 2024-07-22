import boto3

s3_client = boto3.client("s3", endpoint_url="http://127.0.0.1:5000", region_name="us-east-1")
s3_client.create_bucket(Bucket="bucket_name")
