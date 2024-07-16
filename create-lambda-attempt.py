# todo : adjust & complete the surrounding code 
response1 = lambda1.add_permission(FunctionName='put*your*lambda*arn*here',
                               StatementId='response2-id-2',
                               Action='lambda:InvokeFunction',
                               Principal='s3.amazonaws.com',
                               SourceArn='put*your*s3*bucket*arn*here'
                              )
response2 = lambda1.get_policy(FunctionName='put*your*lambda*arn*here')