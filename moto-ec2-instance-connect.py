# create ec2 instance 
# assuming I interpreted the coursework docs correctly, we need not implement the cost optimization 
# so this is just a regular EC2 instance rather than a spot instance (which tends to be cheaper)

# not sure if I'll need an elastic IP 
# I found it really helped during the Devops coursework though 
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html


import boto3
import base64
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

s3_client = boto3.client("s3", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
s3_client.create_bucket(Bucket="ec2bucket")
print("\nOBJECTS: \n", s3_client.list_objects(Bucket="ec2bucket"))

with open('upload-images.py', 'rb') as file:
    # Is it common to have a singleton module? 
    # wait, am I just using route here so I don't YET need to worry about assigning roles/groups security policies yet? 
    # https://hackernoon.com/resolving-typeerror-a-bytes-like-object-is-required-not-str-in-python
    client = boto3.client(
        'ec2', region_name='us-east-1', endpoint_url="http://127.0.0.1:5000"
    )
    
    # client.create_instances(ImageId='ami-08e4e35cccc6189f4', MinCount=1, MaxCount=1)

    """
    So if I remember correctly, this UserData script is executed 
    when the virtual machine is running, but, given that the instance 
    needs the images before the script is executed, 
    I'd either have to do something along the lines of 
    - put the images elsewhere e.g. a Github repo & perhaps turn that into a CDN 
        - when the script executes, it'll download the images from the Github repo 
        then upload them to the S3 bucket 
    - have the script wait via time.sleep, or repeatedly check if the images exist 
        - before trying to upload them to S3 
        - that way I/the system has time to send the images to the EC2 instance via SSH or so
    - simply just SSH into the instance after its running and scp the images to the EC2 instance 
        - then execute the script 
        - pretty sure this can be done via the SSM service's API's run_command function 

    Also I don't think Moto would actually run the script provided as UserData nor would it even emulate 
    a virtual machine (e.g. as a container)
    """
                            
    # run_instances vs launch_instances vs create_instances? 
    client.run_instances(ImageId='ami-08e4e35cccc6189f4', MinCount=1, MaxCount=1,
                        # originally I intended on trying to automate the execution of the python script 
                        # where 1 way would be injecting the bucket name, and env variables into the script 
                        # using the replace function, but ultimately figured I didn't have enough time 
                        # since I lost alot of time due my account being bugged & not letting me 
                        # ssh into ec2 instance, the deactivation & reactivation of the AWS account fixed this 
                        # one issue is the ec2 instance not being able to access S3 
                        # not sure if this is VPC related, but I could just give the ec2 instance its own env variable 
                        # and auth via the env file, but then I'm not sure if the instance will execute the python script 
                        # as python 2 or python 3, this script is python 3 , so I'd probably want 
                        # the EC2 instance to run a bash script, and have the bash script run python 3 
                        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html#:~:text=This%20value%20will%20be%20base64%20encoded%20automatically.%20Do%20not%20base64%20encode%20this%20value%20prior%20to%20performing%20the%20operation.
                        # Boto will automatically encode the UserData value in base64
                        UserData=file.read(), # see the multi line comment above this invocation 
                        # so I beliave that Vocareum provide pre-created keypairs for us 
                        # so for now I am just going to assume that Moto will not care about the KeyName 
                        # otherwise I'll need to use the create_keypair method 
                        # https://docs.getmoto.org/en/latest/docs/services/ec2.html#:~:text=%5BX%5D-,create_key_pair,-%5BX%5D%20create_launch_template
                        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_key_pair.html
                        KeyName='vockey'
                    )

    print(client.describe_instances())

    # todo: use SSM.run_command to SSH into the instance, transfer the images, execute the script 
    # note: Moto & Boto support EC2InstanceConnect which is essentially SSH, but I doubt Moto 
    # will actually emulate this functionality (Localstack's paid version does) 
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html
    # todo: do we explicitly need to use SSH or can we use SSM's run_command? 
    # If we explicitly need SSH, then honestly I'm not entirely sure how flexible Instance Connect is, 
    # but there is the SSH client library Paramiko which could do so in a programmatic way 
    # alternatively just use the os.system method to have Python run the CLI commands 
    # https://stackoverflow.com/questions/3730964/python-script-execute-commands-in-terminal#:~:text=A%20simple%20way%20is%20using%20the%20os%20module%3A

    
    # todo: use Paramiko to scp the images to the EC2 instance
    instance_connect_client = boto3.client("ec2-instance-connect", region_name='us-east-1', endpoint_url="http://127.0.0.1:5000")
    instance_connect_response = instance_connect_client.send_ssh_public_key(
        # The zone where the instance was launched
        AvailabilityZone='us-east-1',
        # The instance ID to publish the key to.
        InstanceId=client.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"],
        # This should be the user you wish to be when ssh-ing to the instance (eg, ec2-user@[instance IP])
        InstanceOSUser='ec2-user',
        # This should be in standard OpenSSH format (ssh-rsa [key body])
        # I am assuming Moto will not care if its the actual public key or not 
        SSHPublicKey='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3FlHqj2eqCdrGHuA6dRjfZXQ4HX5lXEIRHaNbxEwE5Te7xNF7StwhrDtiV7IdT5fDqbRyGw/szPj3xGkNTVoElCZ2dDFb2qYZ1WLIpZwj/UhO9l2mgfjR56UojjQut5Jvn2KZ1OcyrNO0J83kCaJCV7JoVbXY79FBMUccYNY45zmv9+1FMCfY6i2jdIhwR6+yLk8oubL8lIPyq7X+6b9S0yKCkB7Peml1DvghlybpAIUrC9vofHt6XP4V1i0bImw1IlljQS+DUmULRFSccATDscCX9ajnj7Crhm0HAZC0tBPXpFdHkPwL3yzYo546SCS9LKEwz62ymxxbL9k7h09t',
    )
    print("\ninstance_connect_client: \n", instance_connect_response)
    """
    so now that I am hypothetically connected, does this mean I can start running 
    SSH commands between my PC & the EC2 instance? 
    Or does this mean that I am within the EC2 instance & no longer have access to the original PC? 

    So if we are within the EC2 instance 
    Then we'd do 
    https://stackoverflow.com/questions/11304895/how-do-i-copy-a-folder-or-file-from-remote-to-local-using-scp#:~:text=The%20OP%27s%20question%20was%20whether%20it%20is%20possible%20to%20copy%20file%20from%20remote%20to%20local%20host%20while%20ssh%27d%20to%20remote%20host.%20I%27m%20not%20sure%20why%20no%20single%20answer%20has%20correctly%20addressed%20his/her%20question
    scp -r DEFAULTGATEWAY@windows:/path/to/foo /home/user/Desktop/ 
    ^ I don't think this is correct 
    If I was running Linux on my actual PC then it'd be (assuming I'm inside the EC2 instance)
    scp -r DEFAULTGATEWAY@ubuntu:/path/to/foo /home/user/Desktop/ 
    Actually I am overthinking this, I believe that if 2 machines have been connected via 
    SSH recently, then SCP can be used from actual PC to Ec2 instance without needing to re-auth ? 
    Given that virtualbox seems broken, I think I'd need to boot up a real EC2 instance 
    to help me figure this out      
    """ 


    # utilize the SSM service's send_command function to execute commands 
    # https://stackoverflow.com/questions/42645196/how-to-ssh-and-run-commands-in-ec2-using-boto3
    ssm_client = boto3.client("ssm", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
    ssm_client.send_command(
            DocumentName="AWS-RunShellScript", # One of AWS' preconfigured documents
            Parameters={'commands': [
                # hypothetically I could pass the S3 bucket name as a CLI arg to the python script 
                "python upload-images.py"
            ]},
            InstanceIds=[client.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"]],
        )

print("\nOBJECTS: \n", s3_client.list_objects(Bucket="ec2bucket"))

# maybe: attempt to connect to Ec2 instance though this may require Docker or may not be possible/implemented

