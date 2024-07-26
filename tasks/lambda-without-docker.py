"""
	- create a lambda using Boto 
		- creating an IAM policy & role 
		- convert a directory containing a lambda function to a zip file 
		- create the lambda 
		- print lambdas 
	- attempt executing using Moto & !user_docker
	- note the error 
	- install & start Moto server 
	- attempt executing using Moto & !user_docker
	- note the error 

	"""

import boto3
from moto import mock_aws
#ZIPNAME = "code\\process-image-lambda.zip"
ZIPNAME = "process-image-lambda.zip"


def aws_file():
    with open(ZIPNAME, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content



lambda_client = boto3.client('lambda', region_name="us-east-1") # may need endpoint for moto server 
def lambda_creator():
    # todo:
    # define policy 
    # create policy 
    # create role 
    # attach policy to role 
    iam_client = boto3.client("iam", region_name="us-east-1") # may need endpoint for moto server 
    response = iam_client.create_role(
        AssumeRolePolicyDocument='<Stringified-JSON>',
        Path='/',
        RoleName='Test-Role',
    )

    print(response)

    response = lambda_client.create_function(
        Code={
            'ZipFile': aws_file()
        },
        Description='Hello World Test.',
        FunctionName='process-images',
        Handler='lambda_function.lambda_handler',
        Publish=True,
        # do I need to create a policy & a role (& attach them) before hand? 
        # from what I can infer, yes - https://stackoverflow.com/questions/36419442/the-role-defined-for-the-function-cannot-be-assumed-by-lambda
        Role='arn:aws:iam::123456789012:role/lambda-role',
        Runtime='python3.10',
    )
    return response

def validate_lambda_creation():
    response = lambda_client.get_function(
        FunctionName='process-images',
        Qualifier='1',
    )
    print("\n\nVALIDATE LAMBDA CREATION: ")
    print(response)

def invoke_lambda():
    response = lambda_client.invoke(
        FunctionName='process-images',
        Payload='{}', # is this optional? 
        Qualifier='1', # not sure what this is 
    )
    print("\n\nINVOKE LAMBDA: ")
    print(response)


@mock_aws
def execute():
    lambda_creator()
    validate_lambda_creation()
    invoke_lambda()

execute()