from moto import mock_aws, mock_iam
from moto.core import set_initial_no_auth_action_count
import boto3
#@set_initial_no_auth_action_count(10000)
#see https://stackoverflow.com/a/74331093
with mock_iam():
    iam = boto3.client("iam", region_name="eu-west-1")
    iam_role = iam.create_role(
        RoleName="lambda-role",
        AssumeRolePolicyDocument="some policy",
        Path="/my-path/",
    )["Role"]["Arn"]

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