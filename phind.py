import boto3
import json
from moto import mock_aws

@mock_aws
def trigger_lambda_by_uploading_to_s3():
    conn = boto3.client("s3", region_name="us-east-1")
    conn.upload_file(Filename='image1.jpg', Bucket='images', Key='image1.jpg')
    print("file uploaded (mocked)")

@mock_aws
def create_lambda_and_s3_bucket_upload_to_s3_to_trigger_lambda():
    s3conn = boto3.client("s3", region_name="us-east-1")
    s3conn.create_bucket(Bucket="images")

    lambda_cli = boto3.client('lambda')
    iam_cli = boto3.client('iam')

    role_arn = iam_cli.create_role(
        RoleName='lambda-role',
        AssumeRolePolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        })
    )['Role']['Arn']

    lambda_response = lambda_cli.create_function(
        FunctionName='process-image',
        Runtime='python3.7',
        Role=role_arn,
        Handler='process_image.handler',
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()}
    )

    lambda_arn = lambda_response['FunctionArn']

    s3conn.put_bucket_notification_configuration(
        Bucket='images',
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [{'LambdaFunctionArn': lambda_arn, 'Events': ['s3:ObjectCreated:*']}]
        })

    lambda_cli.add_permission(
        FunctionName="process-image",
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f"arn:aws:s3:::images",
        SourceAccount='66666666666'
    )

    trigger_lambda_by_uploading_to_s3()

create_lambda_and_s3_bucket_upload_to_s3_to_trigger_lambda()
