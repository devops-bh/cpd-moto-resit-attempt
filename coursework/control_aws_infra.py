import boto3
import yaml
import json
# these constants are just temp for dev 
LOGGING = True 
BUCKETNAME = "mockedbucket"
SNS_TOPIC = "mockedsnstopic" # arn:aws:sns:us-east-1:123456789012:mockedsnstopic
TEMPLATEFILELOCATION = 'queue-template.yaml'
STACKNAME = 'cloud_formation_face_analysis_queue_stack'

class StaticOrchestrator:
    logging = LOGGING
    def reset(self):
        pass
    def getServices(self):
        pass
    # [todo] what happens if I forget to pass the error when calling the function? 
    def logError(self, error):
        # write to file or kafka topic 
        if None == error:
            print("Something went wrong")
            return
        print("\nError: \n", error)
    def log(self, message=None):
        # write to file or kafka topic 
        if True == self.logging:
            print("\nLogger:\n", message)

# https://stackoverflow.com/questions/30556857/creating-a-static-class-with-no-instances 
# Python does not support the concept of static classes? 
Orchestrator = StaticOrchestrator()

class CloudformationStack:
    """
    Instead of sending 1 client, multipe clients are sent: the SQS client, DynamoDB client and Cloudformation client 
    So hypothetically I could use the strategy pattern to get the required client?
    """
    clients = None
    def __init__(self, clients):
        self.clients = clients

    def __load_yml_file_as_json(self, yml_file_location):
        try:
            with open(yml_file_location, 'r') as content_file:
                content = yaml.load(content_file, Loader=yaml.FullLoader)
            Orchestrator.log(f"attempted to load YML and convert to JSON") 
            return json.dumps(content)
        except Exception as exception:
            Orchestrator.logError(f"failed to load YML and convert to JSON\n{exception}")
    def create(self):
        # sqs + dynamo
        try:
            stack_as_json = self.__load_yml_file_as_json(TEMPLATEFILELOCATION)
            response = self.clients["cloud_formation_client"].create_stack(
                StackName=STACKNAME,
                TemplateBody=stack_as_json)
            Orchestrator.log(f"stack creation attempt\n {response}")
        except Exception as exception:
            Orchestrator.logError(f"failed to create stack\n{exception}")
    def validate(self):
        # todo: error checking & programmetically check the desired stacks exist similar to the S3 bucket code
        Orchestrator.log(f"Stacks: \n{self.clients['cloud_formation_client'].list_stacks()}") # TODO: GET THE ACTUAL STACK 
        # check SQS queue exists 
        listed_queues_response = self.clients["sqs_client"].list_queues()
        Orchestrator.log(f"Queues: \n{listed_queues_response}")
        # check DynamoDB table exists 
        listed_tables_response = self.clients["dynamodb_client"].list_tables()
        Orchestrator.log(f"tables: \n{listed_tables_response}")
    def destroy(self):
        pass


# task1 
class EC2Instances:
    client = None
    def __init__(self, client):
        self.client = client

    # will SSH into the instance & provide the image & script 
    """
    so if I was doing an OOP based implementation 
    then I'd have the base interface which defines the create, validate, destroy methods 
    then I'd maybe use the decorator design pattern to attach these additional methods? 
    """
    def _prepare_instance_with_files(self): pass
    def _execute_upload_images_to_s3_script(self): pass
    def create(self):
        pass
    def validate(self):
        pass
    def destroy(self):
        pass

# task3
class SNSTopic:
    client = None
    response = None
    def __init__(self, client):
        self.client = client

    def create(self):
        try: 
            self.response = self.client.create_topic(Name=SNS_TOPIC)
            Orchestrator.log(f"sns topic creation attempt\n {self.response}")
        except Exception as exception:
            Orchestrator.logError(exception)
    def validate(self):
        pass
    def destroy(self):
        pass
    def getArn(self):
        if None == self.response:
            Orchestrator.logError("Response is None")
            return
        return self.response["TopicArn"]


# task2
class S3Bucket:
    client = None
    s3_bucket_resource = None
    def __init__(self, client, resource):
        self.client = client
        self.s3_bucket_resource = resource
    def _configure_bucket_notification(self, sns_topic_arn):
        try:
            bucket_notification = self.s3_bucket_resource.BucketNotification(BUCKETNAME)
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
            Orchestrator.log(f"bucket notification configuration attempt\n {response}")
        except Exception as exception:
            Orchestrator.logError(exception)

    def create(self, sns_topic_arn):
        try:
            self.client.create_bucket(Bucket=BUCKETNAME)
            self._configure_bucket_notification(sns_topic_arn)
            Orchestrator.log("Bucket with event notification configured was created")
        except Exception as exception:
            Orchestrator.logError(exception)
    def validate(self):
        try: 
            # pretty sure I could just do 
            # self.client.list_buckets()["Buckets"][BUCKETNAME]
            for bucket in self.client.list_buckets()["Buckets"]:
                if BUCKETNAME == bucket["Name"]:
                    Orchestrator.log(f"Bucket {BUCKETNAME} was created")
                    return
        except Exception as exception:
            Orchestrator.logError(exception)
    def destroy(self):
        # with Moto services are auto destroyed when the server is restarted 
        pass


class Lambda:
    lambda_name = ""
    def __init__(self, lambda_name):
        self.lambda_name = lambda_name
        pass
    def _create_rekognition_lambda(self): 
        pass
    def _create_save_details_lambda(self): 
        pass
    
    def create(self):
        # also a strategy pattern I guess 
        if self.lambda_name == "rekognition_lambda":
            self._create_rekognition_lambda()
        elif self.lambda_name == "save_details_lambda":
            self._create_save_details_lambda()
        else: 
            Orchestrator.logError("Please provide the name of the lambda (rekognition_lambda, save_details_lambda)")
    def validate(self): pass
    # more so execute mock lambda 
    # I guess (perhaps if was being more functional) I could pass the lambda function to invoke 
    # e.g. execute_lambda_mock(lambda_handler)
    def execute_lambda_mock(self): 
        # ...
        pass
    def validate_lambda_execution_mock(self): pass
    def invoke_lambda(self): pass
    def validate_lambda_invocation(self): pass
