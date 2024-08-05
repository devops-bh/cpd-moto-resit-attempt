import boto3
import json
import requests
requests.post("http://127.0.0.1:5000/moto-api/reset")
def create_queue_and_send_message_to_queue():
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    create_sqs_queue_response = sqs_client.create_queue(QueueName="rekognition-queue")
    # print(create_sqs_queue_response)
    queue_url = create_sqs_queue_response["QueueUrl"]
    print(queue_url)
    send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps({
        "task_status": "in progress"
    }))

def read_received_messages_from_queue():
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue")
    print("\nrecieved_message_sqs_queue_response\n")
    print(recieved_message_sqs_queue_response)
    print("\nrecieved_message_sqs_queue_response[\"Messages\"]\n")
    print(recieved_message_sqs_queue_response["Messages"])
    

create_queue_and_send_message_to_queue()
print("\n...\n")
read_received_messages_from_queue()