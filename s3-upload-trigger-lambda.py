# Image file upload to S3 and Lambda trigger from SNS
"""
https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications.html
https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html
https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
https://aws.amazon.com/blogs/architecture/understanding-the-different-ways-to-invoke-lambda-functions/
https://medium.com/awesome-cloud/aws-different-ways-to-trigger-aws-lambda-functions-understand-lambda-invocations-integration-other-services-7d8110028141
https://dashbird.io/blog/what-are-aws-lambda-triggers/
"""

"""
# use Boto3 to create a lambda with a trigger 
There are 2 ways to accomplish this, 
By adding the trigger (notification) to the AWS Lambda 
By configuring the S3 bucket to trigger the AWS Lambda ~ demonstrated via https://stackoverflow.com/a/56473008
We are going to do the first option as it is more concise code wise  
^ ignore this, the first option (triggers) are only applicable to some services, 
where the triggering service (e.g. S3) stores the trigger information, not the lambda 
The other option is "event source mapping" in which lambda stores the information 
see these links regarding the differences 
- https://github.com/aws/serverless-application-model/issues/31#issuecomment-264332672
- https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
- https://docs.aws.amazon.com/cli/latest/reference/lambda/create-event-source-mapping.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html

Though I doubt the lecturer mentions the difference between event source mapping and triggers (I'm pretty sure
he only talks about triggers), his hints & resource document links to 
https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html
"In Lambda, a common use case is to invoke your function based on an event that occurs elsewhere in your
application. Some services can invoke a Lambda function with each new event. This is called a trigger"
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html
So I believe AWS uses the terms "event notification" & "trigger" simultaneously 
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html



"""



class LambdaWrapper:
    def __init__(self, lambda_client, iam_resource):
        self.lambda_client = lambda_client
        self.iam_resource = iam_resource


    def invoke_function(self, function_name, function_params, get_log=False):
        """
        Invokes a Lambda function.

        :param function_name: The name of the function to invoke.
        :param function_params: The parameters of the function as a dict. This dict
                                is serialized to JSON before it is sent to Lambda.
        :param get_log: When true, the last 4 KB of the execution log are included in
                        the response.
        :return: The response from the function invocation.
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=json.dumps(function_params),
                LogType="Tail" if get_log else "None",
            )
            logger.info("Invoked function %s.", function_name)
        except ClientError:
            logger.exception("Couldn't invoke function %s.", function_name)
            raise
        return response


