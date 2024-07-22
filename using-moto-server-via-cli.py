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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np
import boto3
import io
"""server = ThreadedMotoServer()
server.start()
"""
#client = boto3.client("service", endpoint_url="http://localhost:5000")
@mock_aws(config={"lambda": {"use_docker": False}})
def mock_resources():
    server_client = boto3.client("s3", endpoint_url="http://127.0.0.1:5000")
    iam_client = boto3.client('iam', endpoint_url="http://127.0.0.1:5000")
    lambda_client = boto3.client('lambda', endpoint_url="http://127.0.0.1:5000")
    server_client.create_bucket(Bucket="test-moto-server")
    print(server_client.list_buckets())
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
    """
    Even though the response may look like the lambda ran, I am still not sure that the lambda actually runs 
    I am somewhat positive I have configured Moto to emulate the lambda runtime without using Docker 
    But the lambda doesn't actually do anything, and I have no idea if this is intentional or not 
    """
    # or maybe it was the function which runs that was to have the @mock_aws(docker: false) ? 
    response = lambda_client.invoke(
        FunctionName='YourLambdaFunctionName',
        Payload='{"optionaL": "ihopeso"}', # is this optional? 
        Qualifier='1', # not sure what this is 
    )
    print("INVOKED LAMBDA RESPONSE: ")
    print(response)
    print("Buckets: ")
    # HERE THE BUCKETS WILL BE EMPTY, I believe this is because we are using the in-memory version of Moot 
    # at first I assumed in-memory meant the resources are mocked the entire script's execution time 
    # but perhaps its actually that each resource is mocked for the duration of the decorated function is was created in?
    print(server_client.list_buckets())

    server_client.upload_file(r"C:\Users\sleep\software-dev-2024\cpd-resit\tasks\image1.jpg", "test-moto-server", "image1.jpg")

    # output bucket contents 
    response = server_client.list_objects(Bucket='test-moto-server')
    print("\nLIST OBJECTS: ")
    print(response)
    print("\nLIST OBJECTS V2: ")
    response = server_client.list_objects_v2(Bucket='test-moto-server')
    print(response)
    print("GET IMAGE FROM BUCKET: ")
    response = server_client.get_object(
        Bucket='test-moto-server',
        Key='image1.jpg',
    )
    print(response)
    img_in_response = response["Body"]
    print(img_in_response)
    outfile = io.BytesIO()
    server_client.download_fileobj("test-moto-server", "image1.jpg", outfile)
    outfile.seek(0)
    Image.open(outfile).save("geeks.jpg") 

mock_resources()
#server.stop()

