from moto import mock_aws
import boto3
import json

@mock_aws
def create_lambda_execution_role():
    iam = boto3.client("iam", region_name="eu-west-1")
    
    # Combine the trust relationship and the permissions policy into a single document
    combined_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": "arn:aws:s3:::images/*"
            }
        ]
    }
    
    role = iam.create_role(
        RoleName="lambda-role",
        AssumeRolePolicyDocument=json.dumps(combined_policy),
        Path="/my-path/"
    )["Role"]["Arn"]
    return role

@mock_aws
def create_process_image_lambda(role_arn): 
    response = boto3.client("lambda", region_name="us-east-1").create_function(
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()},
        Description='Process image objects from Amazon S3.',
        FunctionName='process-image',
        Handler='process_image.handler',
        Publish=True,
        Runtime='python3.x',
        Role=role_arn
    )
    print(response)

import time
if __name__ == "__main__":
    role_arn = create_lambda_execution_role()
    print("Waiting for role to propagate...")
    time.sleep(100)  # Adjust sleep duration as needed
    create_process_image_lambda(role_arn)
