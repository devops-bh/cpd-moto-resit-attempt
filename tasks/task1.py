# create an S3 bucket (have SNS react to file being uploaded )

# honestly I kind of like Localstack's Botostack way but its not too much of an API difference 
# though Localstack's is more procedural which is what I think I want to go for
from moto import mock_aws
import boto3

s3_client = boto3.client("s3", region_name="us-east-1")
def create_bucket(bucket_name):
    # I don't think it matters if we use client or resource
    s3_client.create_bucket(Bucket=bucket_name)

def validate_buckets_creation(bucket_name):
    for bucket in s3_client.list_buckets()["Buckets"]:
        if bucket["Name"] == "bucket_name":
            print(f"Bucket {bucket_name} was created")
            return
    print("Bucket {bucket_name} was not created successfully")


# optional teardown/cleanup method 
def teardown():
    pass

@mock_aws
def create_and_configure_resources():
    bucket_name = "images"
    create_bucket(bucket_name)
    validate_buckets_creation(bucket_name)


create_and_configure_resources()