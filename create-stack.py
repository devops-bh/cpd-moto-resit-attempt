import boto3
import yaml
import json

client = boto3.client('cloudformation', endpoint_url="http://127.0.0.1:5000")
# by disabling the rollback, does this mean I don't need the rollback config param? 

template_file_path = 'queue-stack.yml'

with open(template_file_path, 'r') as file:
    template_body = yaml.safe_load(file)

stack_name = 'YourStackName'

response = client.create_stack(
    StackName=stack_name,
    TemplateBody=json.dumps(template_body),
    Parameters=[
        {
            'ParameterKey': 'KeyName',
            'ParameterValue': 'YourKeyName'
        }
        # Add more parameters as needed
    ],
    Capabilities=[
        'CAPABILITY_IAM'
    ],
    Tags=[
        {
            'Key': 'Project',
            'Value': 'ExampleProject'
        }
    ]
)


