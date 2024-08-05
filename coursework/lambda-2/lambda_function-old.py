"""
I thought it'd be as relatively simple as creating the resources (as mocks) 
Defining the lambda 
Having the lambda interact with the previously created resources 
BUT 
For whatever reason (both when using Moto server & when using the decorator without the server)
Lambda doesn't seem to be able to read the messages from the SQS queue, 
Which has me suspecting that lambda does not actually see the SQS queue 
Bare in mind I am executing the lambda as a regular python function 
I vaguely remember discovering that when using the decorators, resources within different functions 
could not "see" each other, but found that (well, at least it seemed like) this was not the case 
when using the Moto server (as AWS state is maintained in memory the duration the server is running)
But cpd-resit\coursework\lambda-2\moto-server-aws-state-awareness-across-functions.py
Appears to give me the behavior I wanted, so I am not sure why this script failed 
"""
# save_details_lambda 
# reads from SQS queue and saves information to DynamoDB table 
import boto3
import json
import requests
from moto import mock_aws

#requests.post("http://127.0.0.1:5000/moto-api/reset")

# todo: create an SQS (later this will be moved to control_aws_infra.py) + add a message to the queue 
"""
So when resources communicate via AWS event notifications (triggers), the event object will be empty/None, 
but when event source mappings are used, then the event will be injected into the lambda (as Records)? 
"""
sqs_client = boto3.client("sqs", region_name="us-east-1")#, endpoint_url="http://127.0.0.1:5000")
def lambda_handler(event, context):
    # lambda & SQS communicate via event source mappings 
    """
    So this won't actually cause the lambda to execute, to have the lambda execute I need to create an 
    event source mapping via the lambda client 
    """
    """send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue", MessageBody=json.dumps({
        "task_status": "in progress"
    }))
    print(send_message_to_sqs_queue_response)"""
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue")
    #print(recieved_message_sqs_queue_response["Messages"][0]["Body"])
    print(recieved_message_sqs_queue_response)
    try:
        print(recieved_message_sqs_queue_response["Messages"][0]["Body"])
    except:
        print("Unable to obtain message")


@mock_aws
def mock():
    #sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", )#rl="http://127.0.0.1:5000")

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html#creating-a-queue
    create_sqs_queue_response = sqs_client.create_queue(QueueName="rekognition-queue")
    # print(create_sqs_queue_response)
    queue_url = create_sqs_queue_response["QueueUrl"]
    print(queue_url)
    send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps({
        "task_status": "in progress"
    }))
    print(send_message_to_sqs_queue_response)

    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl=queue_url)
    """
    Ok, so when it comes to running this code inside the lambda, the lambda won't actually run 
    Unless an event source mapping is configured 
    And I believe the event source mapping will contain the information that is within the SQS message? 
    If so, then I believe lambda will be able to get the message body in 2 ways 
    1. via the event object which is implicitly passed to the lambda (via event source mapping) 
    2. the sqs_client.receive_message function 
    """
    print(recieved_message_sqs_queue_response)
    #print(recieved_message_sqs_queue_response["Messages"][0]["Body"])

    response = dynamodb_client.create_table(
        # todo: do I need to provide definitions in advance or can I provide an empty definition?
        AttributeDefinitions=[
            {
                'AttributeName': 'rekognition',
                'AttributeType': 'S',
            }
        ],
        # todo: do I need to provide a schema in advance or can I provide an empty schema?
        KeySchema=[
            {
                'AttributeName': 'rekognition',
                'KeyType': 'HASH',
            }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName='rekognition_table',
    )

    
    lambda_handler(None, None)

    # execute lambda 
    # print dynamodb items 

mock()

# https://repost.aws/knowledge-center/lambda-function-idempotent
