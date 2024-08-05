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
requests.post("http://127.0.0.1:5000/moto-api/reset")

#sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
def lambda_handler(event, context):
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue")
    print(recieved_message_sqs_queue_response["Messages"][0]["Body"])

def mock():
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    create_sqs_queue_response = sqs_client.create_queue(QueueName="rekognition-queue")
    queue_url = create_sqs_queue_response["QueueUrl"]
    print("QUEUE_URL: ", queue_url)
    send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps({
        "task_status": "in progress"
    }))
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl=queue_url)
    print(recieved_message_sqs_queue_response)

mock()
lambda_handler(None, None)

