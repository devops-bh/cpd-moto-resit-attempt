import boto3
from moto import mock_aws
import json

@mock_aws
def create_role_and_policy():
    iam_client = boto3.client('iam')
    
    # Check if the role exists, if not, create it
    try:
        iam_client.get_role(RoleName='lambda-role')
    except iam_client.exceptions.NoSuchEntityException:
        response = iam_client.create_role(
            RoleName='lambda-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )
        print(f"Created role {response['Role']['RoleName']}")

    # Define the policy document for the role
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": "arn:aws:s3:::images/*"
            }
        ]
    }
    
    # Create the policy
    policy_response = iam_client.create_policy(
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(policy_document),
        Description='Allows Lambda to access S3 bucket'
    )
    print("Created policy:", policy_response['Policy']['Arn'])

    # Attach the policy to the role
    attach_response = iam_client.attach_role_policy(
        RoleName='lambda-role',
        PolicyArn=policy_response['Policy']['Arn']
    )
    print("Attached policy to role:", attach_response)

    # Update the role's trust policy to include a Resource element
    put_role_policy_response = iam_client.put_role_policy(
        RoleName='lambda-role',
        PolicyName="LambdaS3AccessPolicy",
        PolicyDocument='''{
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole",
            "Resource": "*"
            }
        ]
        }'''
    )
    print("Updated trust policy for role:", put_role_policy_response)

create_role_and_policy()
import time
# since AWS takes time, in a real environment may need to give it sometime for the resources to actually be created 
# time.sleep(60) 

@mock_aws
def create_process_image_lambda(): 
    """
    # so here we are creating a function from a zipfile & uploading that zip file to S3? 
    # then AWS uses the zipfile from the S3 bucket to spin up & invoke the lambda? 
    # no, this is telling AWS to look in S3 for the zipfile 
    Code={
        'S3Bucket': "images", # 'lambda-functions-bucket',
        'S3Key': 'function.zip',
    },
    """
    response = boto3.client("lambda", region_name="us-east-1").create_function(
        # https://stackoverflow.com/a/47599666
        Code={'ZipFile': open('./process-image-lambda.zip', 'rb').read()},
        Description='Process image objects from Amazon S3.',
        FunctionName='process-image',
        Handler='process_image.handler',
        Publish=True,
        Runtime='python3.x',
        Role='arn:aws:iam::123456789012:role/lambda-role'
    )
    print(response)

create_process_image_lambda()