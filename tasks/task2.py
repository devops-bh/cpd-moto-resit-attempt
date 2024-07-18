# task1 but configure bucket to notify SNS 
# create an S3 bucket (have SNS react to file being uploaded )

# honestly I kind of like Localstack's Botostack way but its not too much of an API difference 
# though Localstack's is more procedural which is what I think I want to go for
from moto import mock_aws
import boto3

s3_client = boto3.client("s3", region_name="us-east-1")
sns_client = boto3.client("sns", region_name="us-east-1")
def create_bucket(bucket_name):
    # I don't think it matters if we use client or resource
    s3_client.create_bucket(Bucket=bucket_name)
  
def create_sns_topic(topic_name):
    response = sns_client.create_topic(Name=topic_name)
    # I think the ARN will be arn:aws:sns:us-east-1:123456789012:topic_name
    # I think 123456789012 must be a constant for an SNS topic? 
    # still not entirely sure as what an Amazon Resource Name comprises 
    # ok so 123456789012 appears to be the default Moto account-id - https://stackoverflow.com/questions/59348407/how-to-mock-motos-accountid
    return response


def validate_buckets_creation(bucket_name):
    # alternative implementation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_bucket.html
    for bucket in s3_client.list_buckets()["Buckets"]:
        if bucket["Name"] == bucket_name:
            print(f"Bucket {bucket_name} was created")
            return
    print("Bucket {bucket_name} was not created successfully")


def configure_bucket_event_notification_for_sns_topic(bucket_name, sns_topic_arn):    
    # https://stackoverflow.com/questions/49961491/using-boto3-to-send-s3-put-requests-to-sns/52670469#52670469
    # boto3.resource is a higher level API than boto3.client 
    s3_resource = boto3.resource('s3')
    bucket_notification = s3_resource.BucketNotification(bucket_name)
    s3_notification_config = {
        'TopicConfigurations': [
            {
                'TopicArn': sns_topic_arn,
                'Events': [
                    's3:ObjectCreated:*',
                ],
            },
        ],
    }
    response = bucket_notification.put(NotificationConfiguration=s3_notification_config)
    """
    So, if my understanding is correct, and my code implementation is correct, 
    this will automatically have SNS publish to the topic of "new-image" each time 
    a file (image) is uploaded to the S3 bucket? 
    I was a little confused if we also need the policy & set_topic_attributes part of the code, 
    - https://stackoverflow.com/questions/49961491/using-boto3-to-send-s3-put-requests-to-sns/52670469#52670469:~:text=SNS.Client.set_topic_attributes-,sns_topic_policy,-%3D%20%7B%0A%20%20%20%20%22Version%22%3A%20%222012%2D10
    but assuming my interpretation of this code's output is correct, then that is not needed 
    """

# optional teardown/cleanup method 
def teardown():
    pass

def upload_file_to_validate_bucket_event_notification(bucket_name, sns_topic_arn):
    # print SNS published messages - https://docs.getmoto.org/en/latest/docs/services/sns.html#:~:text=If%20you%20need%20to%20verify%20that%20a%20message%20was%20published%20successfully
    from moto.core import DEFAULT_ACCOUNT_ID
    from moto.sns import sns_backends
    sns_backend = sns_backends[DEFAULT_ACCOUNT_ID]["us-east-1"]  # Use the appropriate account/region
    all_sent_notifications = sns_backend.topics[sns_topic_arn].sent_notifications
    print("SENT NOTIFICATIONS BEFORE FILE UPLOAD: ")
    print(all_sent_notifications)
    s3_client.upload_file("image1.jpg", bucket_name, bucket_name+"/"+"image1.jpg")
    print("SENT NOTIFICATIONS AFTER FILE UPLOAD: ")
    all_sent_notifications = sns_backend.topics[sns_topic_arn].sent_notifications
    print(all_sent_notifications)

@mock_aws
def create_and_configure_resources():
    bucket_name = "images"
    sns_topic_name = "new-image"
    sns_topic_arn = create_sns_topic(sns_topic_name)["TopicArn"]
    create_bucket(bucket_name)
    # contemplated doing this inside the create_bucket function 
    # I suppose maybe use the builder pattern for this? 
    validate_buckets_creation(bucket_name)
    configure_bucket_event_notification_for_sns_topic(bucket_name, sns_topic_arn)
    upload_file_to_validate_bucket_event_notification(bucket_name, sns_topic_arn)


create_and_configure_resources()