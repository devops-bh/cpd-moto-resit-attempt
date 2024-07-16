import boto3
import json
from moto import mock_aws

@mock_aws
def create_lambda_and_s3_bucket_upload_to_s3_to_trigger_lambda():
    s3conn = boto3.client("s3", region_name="us-east-1")
    s3conn.create_bucket(Bucket="images")

    # Create Lambda function
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

    # Extract the Lambda function ARN from the response
    lambda_arn = lambda_response['FunctionArn']

    # Configure S3 bucket notification
    s3conn.put_bucket_notification_configuration(
        Bucket='images',
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [{'LambdaFunctionArn': lambda_arn, 'Events': ['s3:ObjectCreated:*']}]
        })

    # Add permission to allow S3 to invoke the Lambda function
    lambda_cli.add_permission(
        FunctionName="process-image",
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f"arn:aws:s3:::images",
        SourceAccount='66666666666'  # Replace with your AWS Account ID
    )

    trigger_lambda_by_uploading_to_s3()

create_lambda_and_s3_bucket_upload_to_s3_to_trigger_lambda()

@mock_aws
def trigger_lambda_by_uploading_to_s3():
    conn = boto3.client("s3", region_name="us-east-1")
    #conn = boto3.resource("s3", region_name="us-east-1")
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    #conn.put_object(Bucket="mybucket", "image1.jpg", Body=self.value)
    conn.upload_file("image1.jpg", "images", "image1.jpg")
    print("file uploaded (mocked)")

#trigger_lambda_by_uploading_to_s3()