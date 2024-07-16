"""
https://stackoverflow.com/questions/44982302/how-to-add-the-trigger-s3-bucket-to-lambda-function-dynamicallypython-boto3-api
https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketNotificationConfiguration.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html

"""
import boto3
# create bucket 

import json
import boto3
#from moto import mock_lambda, mock_iam
from moto import mock_aws

"""
@mock_lambda
@mock_iam
"""
"""
@mock_aws
def create_lambda():
    #lambda_cli = boto3.client('lambda', endpoint_url='http://localhost:5000')
    lambda_cli = boto3.client('lambda')
    iam_cli = boto3.client('iam')
    

    role_arn = iam_cli.create_role(
            RoleName='lambda-role',
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
            )
        )['Role']['Arn']
    print(role_arn)

    lambda_cli.create_function(
        FunctionName='process-image',
        Runtime='python3.7',
        Role=role_arn,
        Handler='process_image.handler', 
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()}
    )['FunctionArn']

    # should I create the bucket before the lambda so I have the bucket arn? 
    response = lambda_cli.add_permission(
        FunctionName="process-image",
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn="arn:aws:s3:::images",
        SourceAccount='66666666666'
    )

@mock_aws
def create_bucket():
    s3conn = boto3.client("s3", region_name="us-east-1")
    s3conn.create_bucket(Bucket="images")
    # configure a lambda trigger in the form of an S3 event notification
    lambdaArn = "123456789012:role/lambda-role" # suppose I could share the arn as env var 
    # wasn't sure whetther to keep this code here (since its a direct config to S3)
    # or put it in the create-lambda.py after the lambda has been created 
    # does the lambda need to be created before this is called? 
    # because the bucket needs to exist before the lambda is called 
    s3conn.put_bucket_notification_configuration(
        Bucket='images',
        NotificationConfiguration= {'LambdaFunctionConfigurations':[{'LambdaFunctionArn': lambdaArn, 'Events': ['s3:ObjectCreated:*']}]})

create_bucket()
create_lambda()
"""

@mock_aws
def create_lambda_and_s3_bucket():
    s3conn = boto3.client("s3", region_name="us-east-1")
    s3conn.create_bucket(Bucket="images")
    # configure a lambda trigger in the form of an S3 event notification
    lambdaArn = "123456789012:role/lambda-role" # suppose I could share the arn as env var 
    # wasn't sure whetther to keep this code here (since its a direct config to S3)
    # or put it in the create-lambda.py after the lambda has been created 
    # does the lambda need to be created before this is called? 
    # because the bucket needs to exist before the lambda is called 
    s3conn.put_bucket_notification_configuration(
        Bucket='images',
        NotificationConfiguration= {'LambdaFunctionConfigurations':[{'LambdaFunctionArn': lambdaArn, 'Events': ['s3:ObjectCreated:*']}]})

    #lambda_cli = boto3.client('lambda', endpoint_url='http://localhost:5000')
    lambda_cli = boto3.client('lambda')
    iam_cli = boto3.client('iam')
    
    role_arn = iam_cli.create_role(
            RoleName='lambda-role',
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
            )
        )['Role']['Arn']
    print(role_arn)


    lambda_cli.create_function(
        FunctionName='process-image',
        Runtime='python3.7',
        Role=role_arn,
        Handler='process_image.handler', 
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()}
    )['FunctionArn']


    # should I create the bucket before the lambda so I have the bucket arn? 
    response = lambda_cli.add_permission(
        FunctionName="process-image",
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn="arn:aws:s3:::images",
        SourceAccount='66666666666'
    )

create_lambda_and_s3_bucket()