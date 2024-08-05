import boto3
import json
import requests
requests.post("http://127.0.0.1:5000/moto-api/reset")
# git commit + push didnt seem to work, this change is just to force & redo the failed push  
def lambda_handler(event, context):
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue")
    print("\nrecieved_message_sqs_queue_response\n")
    print(recieved_message_sqs_queue_response)
    print("\nrecieved_message_sqs_queue_response[\"Messages\"]\n")
    print(recieved_message_sqs_queue_response["Messages"])
    # todo: update Dynamodb table 
    dynamodb_put_item_response = dynamodb_client.put_item(
        Item={
            'rekognition': {
                'S': 'todo',
            }
        },
        ReturnConsumedCapacity='TOTAL',
        TableName='rekognition_table',
    )
    print("\ndynamodb_put_item_response\n")
    print(dynamodb_put_item_response)
    print("\n")


def create_queue_and_send_message_to_queue():
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    create_sqs_queue_response = sqs_client.create_queue(QueueName="rekognition-queue")
    # print(create_sqs_queue_response)
    queue_url = create_sqs_queue_response["QueueUrl"]
    print(queue_url)
    send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps({
        "task_status": "in progress"
    }))
    # create dynamodb table 
    dynamo_db_table_creation_response = dynamodb_client.create_table(
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
    dynamodb_list_tables_response = dynamodb_client.list_tables()
    print(dynamodb_list_tables_response)
    # execute lambda 
    lambda_handler(None, None)
    # print dynamodb items (dunno how to do this using the client API, use the resource API or consider using "scan" or transact_get_items)
    # or query - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/query.html#:~:text=Client.exceptions.InternalServerError-,Examples,-This%20example%20queries
    dynamodb_get_item_response = dynamodb_client.get_item(
        Key={
            'rekognition': {
                'S': 'todo',
            }},
        TableName='rekognition_table',
    )
    print("\ndynamodb_get_item_response\n")
    print(dynamodb_get_item_response)
    print("\n")



create_queue_and_send_message_to_queue()
#print("\n...\n")
#lambda_handler(None, None)