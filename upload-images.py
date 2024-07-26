import boto3
from datetime import datetime
from pathlib import Path
s3_client = boto3.client("s3", region_name="us-east-1", endpoint_url="http://127.0.0.1:5000")
s3_client.upload_file("image1.jpg", "ec2bucket", "images/image1.jpg")
f = open(str(Path.home())+"/ec2.txt", "w")
f.write(str(datetime.today().strftime('%Y-%m-%d'))+"\n"+datetime.now().strftime("%H:%M:%S"))
f.close()