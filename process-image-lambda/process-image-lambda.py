import json
import boto3
from moto import mock_aws

f = open(r"C:\Users\sleep\software-dev-2024\cpd-resit\hello.txt", "a")
f.write("Now the file has even more content!")
f.close()

rekognition_client = boto3.client('rekognition')
"""
ok, so if we ran in this in a real AWS lambda, we would literally be paying money to 
not use AWS by using AWS (where if we forgot we had the mock_aws then we may be mistakenly thinking we 
are using AWS)
^ so I may make a script which checks files for "mock_aws" 
"""
@mock_aws
def lambda_handler(context, event):
    rekognition_labels_response = rekognition_client.detect_labels(
        Image={"S3Object": {"Bucket": "rekognition-bucket", "Name": "image1.jpg"}}, 
        MaxLabels=5
    )
    labels_list = [label['Name'] for label in rekognition_labels_response['Labels']]
    labels = ", ".join(labels_list)

    # Initialize the item for DynamoDB
    item = {
        "ImageName": {"S": "image1.jpg"},
        "calmConfidenceScore": {"S": ""},
        "happyConfidenceScore": {"S": ""},
        "angryConfidenceScore": {"S": ""},
        "frustratedConfidenceScore": {"S": ""},
        "labels": {"S": labels}
    }
    # Ok so I assume that since this is a mock it always returns mobile phone? 
    # therefor when unit testing, you have to assume that if the code is successful 
    # it returns mobile phone? and maybe you'd also want to test the returned data's structure (or format) 
    # e.g. what attributes etc it is 
    # and in a real ML setting you (well, AWS given its a non modified Rekognition model) would 
    # already have an idea as to the confidence levels for each label? 
    # is it possible to change the default return via Moto or would I need a custom implementation 
    # if I wanted something more dynamic (even if not ML, or perhaps a local model) rather than a mocked API? 
    print(item, item["labels"])    
    return item

#lambda_handler()