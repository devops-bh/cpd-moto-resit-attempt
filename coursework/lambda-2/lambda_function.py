# save_details_lambda 
# reads from SQS queue and saves information to DynamoDB table 
import boto3
import json
sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")

# todo: create an SQS (later this will be moved to control_aws_infra.py) + add a message to the queue 
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html#creating-a-queue
create_sqs_queue_response = sqs_client.create_queue(QueueName="rekognition-queue")
# print(create_sqs_queue_response)
queue_url = create_sqs_queue_response["QueueUrl"]
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
print(recieved_message_sqs_queue_response["Messages"][0]["Body"])
exit()
"""
So when resources communicate via AWS event notifications (triggers), the event object will be empty/None, 
but when event source mappings are used, then the event will be injected into the lambda (as Records)? 
"""
def lambda_handler(event, context):
    # lambda & SQS communicate via event source mappings 
    """
    So this won't actually cause the lambda to execute, to have the lambda execute I need to create an 
    event source mapping via the lambda client 
    """
    sqs_recieved_message_response = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = sqs_recieved_message_response['Messages'][0]
    receipt_handle = message['ReceiptHandle']


# https://repost.aws/knowledge-center/lambda-function-idempotent
