# create dynamodb 
import boto3
dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
dynamodb_create_table_response = dynamodb_client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'labels',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'text',
            'AttributeType': 'S',
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'labels',
            'KeyType': 'HASH',
        }, 
        {
            'AttributeName': 'text',
            'KeyType': 'RANGE',
        }, 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5,
    },
    TableName='detections',
)


print(dynamodb_create_table_response)

# ____ 

import boto3
import json
import requests
# https://stackoverflow.com/a/71446846
from decimal import Decimal
#requests.post("http://127.0.0.1:5000/moto-api/reset")
# git commit + push didnt seem to work, this change is just to force & redo the failed push  
def lambda_handler(event, context):
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    recieved_message_sqs_queue_response = sqs_client.receive_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue")
    """print("\nrecieved_message_sqs_queue_response\n")
    print(recieved_message_sqs_queue_response)
    print("\n")
    """
    # extract from sqs 
    messages = recieved_message_sqs_queue_response["Messages"]
    for message in messages:
        print("\nMessage: ")
        print(f"\n{message}\n")
        body = json.loads(message["Body"])
        print(type(body)) # <class 'dict'>
        # insert into DynamoDB 
        # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#:~:text=in%20DynamoDB.-,Map,-A%20map%20type
        """        response = dynamodb_client.put_item(
                    Item={
                        'detection': {
                            # originally I tried to store the dictionary as a dynamodb map 
                            # but that seemed more complex and/or time consuming than desired 
                            # https://stackoverflow.com/questions/57494372/storing-list-of-dict-in-a-dynamodb-table#:~:text=I%20recommend%20you%20JSON%20encode%20you%20list%20and%20just%20store%20it%20in%20DynamoDB%20as%20a%20string%20value.
                            # but turns out this json string is too large 
                            # PutItem operation: One or more parameter values were invalid: Size of hashkey has exceeded the maximum size limit of2048 bytes
                            'S': json.dumps(body)
                        }
                        # addmitedly could also add time.now as a timestamp 
                    },
                    TableName='detections',
                )
                print(response)
        """
    """database = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:5000")
        table = database.Table("detections")
        table.put_item(Item = {
            "detection": { "S": "test" }
        })"""

    """    dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:5000")
        table = dynamodb.Table("detections")
        item_json = {
            "detection": "John Doe"
        }#.encode('utf-8')
        response = table.put_item(Item=item_json)
    print(response)
    """    
    print(type(body["labels"]), type(body["text"]), type(json.dumps(body["text"])))
    response = dynamodb_client.put_item(
            Item={
                'labels': {
                    # originally I tried to store the dictionary as a dynamodb map 
                    # but that seemed more complex and/or time consuming than desired 
                    # https://stackoverflow.com/questions/57494372/storing-list-of-dict-in-a-dynamodb-table#:~:text=I%20recommend%20you%20JSON%20encode%20you%20list%20and%20just%20store%20it%20in%20DynamoDB%20as%20a%20string%20value.
                    # but turns out this json string is too large 
                    # PutItem operation: One or more parameter values were invalid: Size of hashkey has exceeded the maximum size limit of2048 bytes
                    #'L': json.dumps(body["labels"])
                    #'L': body["labels"]
                    'S': json.dumps(body["labels"])
                },
                'text': {
                    # originally I tried to store the dictionary as a dynamodb map 
                    # but that seemed more complex and/or time consuming than desired 
                    # https://stackoverflow.com/questions/57494372/storing-list-of-dict-in-a-dynamodb-table#:~:text=I%20recommend%20you%20JSON%20encode%20you%20list%20and%20just%20store%20it%20in%20DynamoDB%20as%20a%20string%20value.
                    # but turns out this json string is too large 
                    # PutItem operation: One or more parameter values were invalid: Size of hashkey has exceeded the maximum size limit of2048 bytes
                    #'L': json.dumps(body["text"])
                    #'L': body["text"]
                    'S': json.dumps(body["text"])
                },
                # addmitedly could also add time.now as a timestamp 
            },
            TableName='detections',
        )
    print(response)
    
    # delete message from queue 
    try: 
        pass
    except:
        # so here you'd likely have another SQS queue act as a dead letter queue 
        pass
    # insert into dynamodb (dont bother about batch updates?) ~ though I suppose if there was time I should've

def dict_to_item(raw):
    if type(raw) is dict:
        resp = {}
        for k,v in raw.iteritems():
            if type(v) is str:
                resp[k] = {
                    'S': v
                }
            elif type(v) is int:
                resp[k] = {
                    'I': str(v)
                }
            elif type(v) is dict:
                resp[k] = {
                    'M': dict_to_item(v)
                }
            elif type(v) is list:
                resp[k] = []
                for i in v:
                    resp[k].append(dict_to_item(i))
                    
        return resp
    elif type(raw) is str:
        return {
            'S': raw
        }
    elif type(raw) is int:
        return {
            'I': str(raw)
        }

lambda_handler(None, None) 

# check dynamodb is updated 

"""
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
"""