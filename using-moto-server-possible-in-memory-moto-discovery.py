# OLD - DO NOT USE  
"""
import boto3
from moto.server import ThreadedMotoServer
server = ThreadedMotoServer()
server.start()
#client = boto3.client("service", endpoint_url="http://localhost:5000")
server_client = boto3.client("s3", endpoint_url="http://127.0.0.1:5000")
server_client.create_bucket(Bucket="test-moto-server")
#in_mem_client = boto3.client("s3")
#buckets = in_mem_client.list_buckets()["Buckets"]
print(server_client.list_buckets()["Buckets"])
server.stop()
"""

import boto3
from moto.server import ThreadedMotoServer
from moto import mock_aws
server = ThreadedMotoServer()
server.start()
#client = boto3.client("service", endpoint_url="http://localhost:5000")
#server_client = boto3.client("s3", endpoint_url="http://127.0.0.1:5000")
server_client = boto3.client("s3")
iam_client = boto3.client('iam', endpoint_url="http://127.0.0.1:5000")
lambda_client = boto3.client('lambda', endpoint_url="http://127.0.0.1:5000")
#@mock_aws
#def create_bucket():
@mock_aws
def create_bucket():
    server_client.create_bucket(Bucket="test-moto-server")
    print(server_client.list_buckets())
create_bucket()
"""#in_mem_client = boto3.client("s3")
#buckets = in_mem_client.list_buckets()["Buckets"]
# Initialize the Boto3 client for IAM

# Load the trust policy document from a file
with open('TrustPolicy.json', 'r') as file:
    trust_policy_document = file.read()

# Create the role with the specified trust policy
response = iam_client.create_role(
    RoleName='LambdaS3AccessRole',
    AssumeRolePolicyDocument=trust_policy_document
)

print(response)

# Load the policy document from a file
with open('IAMPolicy.json', 'r') as file:
    policy_document = file.read()

# Add the policy to the role
response = iam_client.put_role_policy(
    RoleName='LambdaS3AccessRole',
    PolicyName='S3AccessPolicy',
    PolicyDocument=policy_document
)

print(response)

# Initialize the Boto3 client for Lambda

response = lambda_client.create_function(
    FunctionName='YourLambdaFunctionName',
    Runtime='python3.10',
    Role='arn:aws:iam::123456789012:role/LambdaS3AccessRole',
    Handler='lambda_function.lambda_handler',
    Code={'ZipFile': open('tasks\process-image-lambda.zip', 'rb').read()},
    Description='A sample Lambda function',
    Timeout=15,
    MemorySize=128,
    Publish=True,
)

print(response)


# invokve lambda function which uploads to S3 bucket 
# this code errors as it is still trying to use Docker to run the lambda 
@mock_aws(config={"lambda": {"use_docker": False}})
def invoke_lambda():
    response = lambda_client.invoke(
        FunctionName='YourLambdaFunctionName',
        Payload='{}', # is this optional? 
        Qualifier='1', # not sure what this is 
    )
    print("INVOKED LAMBDA RESPONSE: ")
    print(response)
invoke_lambda()
"""
print("Buckets: ")
# HERE THE BUCKETS WILL BE EMPTY, I believe this is because we are using the in-memory version of Moot 
# at first I assumed in-memory meant the resources are mocked the entire script's execution time 
# but perhaps its actually that each resource is mocked for the duration of the decorated function is was created in?
@mock_aws
def list_bucket():
    print(server_client.list_buckets())
list_bucket()
#print(server_client.list_buckets())
# output bucket contents 
#create_bucket()
server.stop()

