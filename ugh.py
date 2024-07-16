import json
import boto3
#from moto import mock_lambda, mock_iam
from moto import mock_aws

"""
@mock_lambda
@mock_iam
"""
@mock_aws
def test_lambda_failure():
    #lambda_cli = boto3.client('lambda', endpoint_url='http://localhost:5000')
    lambda_cli = boto3.client('lambda')
    iam_cli = boto3.client('iam')

    role_arn = iam_cli.create_role(
            RoleName='foo',
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

    return lambda_cli.create_function(
        FunctionName='process-image',
        Runtime='python3.7',
        Role=role_arn,
        Handler='process_image.handler', 
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()}
    )['FunctionArn']


if __name__ == '__main__':
    test_lambda_failure()