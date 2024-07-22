import boto3
import yaml
import json
import os
#from dotenv import load_dotenv
#load_dotenv()

# For the Queue 
# Specify the location of your CloudFormation template file
template_file_location = 'queue-template.yaml'

# Specify the name of the stack you want to create
stack_name = 'cloud_formation_face_analysis_queue_stack'

# Read the YAML file and convert it to JSON
with open(template_file_location, 'r') as content_file:
    content = yaml.load(content_file, Loader=yaml.FullLoader)
content = json.dumps(content)

# Create a CloudFormation client
"""cloud_formation_client = boto3.client('cloudformation',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # todo: use env vars
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], # todo: use env vars
    aws_session_token=os.environ['AWS_SESSION_TOKEN'] # todo: use env vars 
)
"""
cloud_formation_client = boto3.client('cloudformation', endpoint_url="http://127.0.0.1:5000")

# Create the stack
print(f"Creating {stack_name}")
response = cloud_formation_client.create_stack(
    StackName=stack_name,
    TemplateBody=content)

