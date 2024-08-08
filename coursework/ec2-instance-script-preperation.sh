"""
Since the coursework documents do not specify that we are to use SSH, and because I had experienced difficulty 
SSHing into an EC2 instance in the past (which seemed like it was due to a bugged AWS account as opposed 
to a technical misunderstanding), I decided to use Wget within a bash script which will (via HTTP) 
download the images and the python script from a server (exposed via Ngrok) onto the EC2 instance. 
The script will then run the upload-images-to-s3.py script. 

This shell script will be executed either via at launch the EC2 UserData parameter 
Or via the SSM.send_command functionality 
"""

SERVER_URL = # this'll be an .env variable which contains the Ngrok URL 
