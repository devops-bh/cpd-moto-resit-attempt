import json
import boto3
from moto import mock_aws

rekognition_client = boto3.client('rekognition')
@mock_aws
def lambda_handler():
    requests = []
    # I remember not using the resource api in the coursework 
    conn = boto3.client("s3", region_name="us-east-1")
    #conn = boto3.resource("s3", region_name="us-east-1")
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket="mybucket")
    #conn.put_object(Bucket="mybucket", "image1.jpg", Body=self.value)
    conn.upload_file("image1.jpg", "mybucket", "image1.jpg")
    """
    # NotImplementedError: The detect_faces action has not been implemented
    # ok so https://docs.getmoto.org/en/latest/docs/services/rekognition.html 
    # does not have an "[x]" next to "detect_faces" so the "[x]" means its not implemented (mocked)  
    # I assumed it was the opposite
    rekognition_response = rekognition_client.detect_faces(
        # todo: create + so that I can mock the S3 bucket 
            Image={"S3Object": {"Bucket": "rekognition-bucket", "Name": "image1.jpg"}},
            Attributes=["ALL"])
    """

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

    # double check if these emotions are part of the API 
    """
    for face in rekognition_response['FaceDetails']:
        for emotion in face["Emotions"]:
            emotion_type = emotion["Type"].upper()
            if emotion_type == "CALM":
                item["calmConfidenceScore"]["S"] = str(emotion["Confidence"])
            elif emotion_type == "HAPPY":
                item["happyConfidenceScore"]["S"] = str(emotion["Confidence"])
            elif emotion_type == "ANGRY":
                item["angryConfidenceScore"]["S"] = str(emotion["Confidence"])
            elif emotion_type == "FRUSTRATED":
                item["frustratedConfidenceScore"]["S"] = str(emotion["Confidence"])
    """
    # Add the item to the batch requests
    """    requests.append({
            'PutRequest': {
                'Item': item
            }
        })
    """    
    """
      {'ImageName': {'S': 'image1.jpg'}, 'calmConfidenceScore': {'S': ''}, 'happyConfidenceScore': {'S': ''}, 'angryConfidenceScore': 
    {'S': ''}, 'frustratedConfidenceScore': {'S': ''}, 'labels': {'S': 'Mobile Phone'}} {'S': 'Mobile Phone'}
    """
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

lambda_handler()