# mock aws services 

from control_aws_infra import *
import boto3
from moto import mock_aws
import requests 

#requests.post("http://127.0.0.1:5000/moto-api/reset")

s3_client = boto3.client("s3", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
# I suppose there is a way to accomplish this using the client API but the code is more verbose 
# & iirc if/when I tried to do so I wasn't able to get it working 
s3_resource = boto3.resource('s3', endpoint_url="http://127.0.0.1:5000")
sns_client = boto3.client("sns", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")

# todo: https://docs.getmoto.org/en/latest/docs/configuration/state_transition/index.html

@mock_aws
def test_sns_topic():
    SNSTopicController = SNSTopic(sns_client)
    SNSTopicController.create()
    SNSTopicController.validate()
    return SNSTopicController

@mock_aws
def test_s3(sns_topic_arn):
    S3BucketController = S3Bucket(s3_client, s3_resource)
    S3BucketController.create(sns_topic_arn)
    S3BucketController.validate()

sns_topic_arn = test_sns_topic()
test_s3("arn:aws:sns:us-east-1:123456789012:mockedsnstopic")