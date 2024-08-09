import boto3
import json
sns_client = boto3.client("sns", region_name="us-east-1", endpoint_url="http://localhost:5000")
lambda_client = boto3.client("lambda", region_name="us-east-1", endpoint_url="http://localhost:5000")
iam_client = boto3.client("iam", region_name="us-east-1", endpoint_url="http://localhost:5000")
role_creation_response = iam_client.create_role(
            RoleName='lambda-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )
print(role_creation_response)
lambda_function_creation_response = lambda_client.create_function(
        Code={'ZipFile': open('../coursework/lambda-1.zip', 'rb').read()},
        Description='Process image objects from Amazon S3.',
        FunctionName='process-image',
        #Handler='processimagefile.handler',
        Handler='lambda_function.lambda_handler',
        Publish=True,
        Runtime='python3.10',
        Role=role_creation_response["Role"]["Arn"]
    )
response = sns_client.create_topic(Name="s3-image-received")
response = sns_client.publish(
    TopicArn='arn:aws:sns:us-east-1:123456789012:s3-image-received',
    Message=json.dumps({
        "image_path": "image1.jpg", 
        "bucket_name": "bucketname" 
    }),
    Subject='s3-image-received',
)

sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://localhost:5000")
sqs_client.create_queue(QueueName="rekognition-queue")

# ___ 

"""
Extract image file name (or path) & S3 bucket name from SNS notification
Call the AWS Rekognition detect_labels function 
Store the labels and their confidence score in a dictionary 
Call the AWS Rekognition detect_text function 
Store the labels and their confidence score in a dictionary 
Send the above data to an SQS queue 
"""

import boto3

def lambda_handler(event, context):
    # print(event)
    # should it be 1 image at a time or should they batched?... 
    message = event['Records'][0]['Sns']['Message']
    print("\n MESSAGE: \n")
    print(message)
    print("\n")
    rekognition_client = boto3.client("rekognition", region_name="us-east-1", endpoint_url="http://localhost:5000")
    sns_client = boto3.client("sns", region_name="us-east-1", endpoint_url="http://localhost:5000")
    sqs_client = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://localhost:5000")

    # extract from SNS notification 
    # TODO: should the lambda be subscribing to the function here, or does the message come within the injected event object? 
    # or can I use sns_backend.topics[sns_topic_arn].sent_notifications
    # I think sent_notifications is probably only for dev/debugging 
    # I believe we implicitly get the message via the injected event object 
    """response = sns_client.subscribe(
        TopicArn="arn:aws:sns:us-east-1:123456789012:s3-image-received",
        Protocol='lambda',
        Endpoint="arn:aws:lambda:us-east-1:123456789012:function:lambda_function_1",
        ReturnSubscriptionArn=True
    )
    print("\nSubscription Resp:\n", response)
    """


    detect_text_response = rekognition_client.detect_text(Image={
        'S3Object': {
            'Bucket': message["bucket"], #'Bucket': "bucketname",
            # just gonna merge the image path, filename & extension into 1 since its convenient 
            'Name': message["image"], #'Name': 'image.jpg',
        }
    })
    print("\ndetect_text_response\n")
    print(detect_text_response)
    print("\n")
    detect_labels_response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': message["bucket"], #'Bucket': "bucketname",
                # just gonna merge the image path, filename & extension into 1 since its convenient 
                'Name': message["image"], #'Name': 'image.jpg',
            },
        },
    )
    print(detect_labels_response)
    # send to SQS queue 
    send_message_to_sqs_queue_response = sqs_client.send_message(QueueUrl="http://127.0.0.1:5000/123456789012/rekognition-queue", MessageBody=json.dumps({
        "imagename": message["image"],
        "labels": detect_labels_response["Labels"],
        # Not sure if it matters yet, but I'd assume that you'd want the parent for each instance, oh well 
        "text": detect_text_response["TextDetections"]
    }))
    print(send_message_to_sqs_queue_response)

sns_event = {
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "2019-01-02T12:45:07.000Z",
        "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==",
        "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": {
            "bucket": "bucketname",
            "image": "image1.jpg", 
        },
        "MessageAttributes": {
          "Test": {
            "Type": "String",
            "Value": "TestString"
          },
          "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
          }
        },
        "Type": "Notification",
        "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-1:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
        "TopicArn":"arn:aws:sns:us-east-1:123456789012:sns-lambda",
        "Subject": "TestInvoke"
      }
    }
  ]
}

lambda_handler(sns_event, None)