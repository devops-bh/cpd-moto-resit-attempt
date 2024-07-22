from datetime import datetime
from pathlib import Path
# not sure if need mock_aws
import boto3
from moto import mock_aws
from PIL import Image
import io
# @mock_aws # file still wasn't updated
# @mock_aws(config={"lambda": {"use_docker": False}}) # file still wasn't updated
@mock_aws
def lambda_handler(event, context): 
    """
    I am using Path.home as I was not sure if Moto/Localstack would create the file 
    in a directory of its own choice as opposed to the current directory when Moto/Localstack 
    was ran 
    https://stackoverflow.com/questions/4028904/what-is-a-cross-platform-way-to-get-the-home-directory#:~:text=If%20you%27re%20on%20Python%203.5%2B%20you%20can%20use%20pathlib.Path.home()%3A
    """
    """    
        print(str(Path.home())+"/lambdalastinvocation.txt")
        f = open(str(Path.home())+"/lambdalastinvocation.txt", "w")
        f.write(str(datetime.today().strftime('%Y-%m-%d'))+"\n"+datetime.now().strftime("%H:%M:%S"))
        f.close()
    """
    # todo: upload to s3 bucket test-moto-server
    s3_client = boto3.client("s3", endpoint_url="http://127.0.0.1:5000")
    s3_client.upload_file(r"C:\Users\sleep\software-dev-2024\cpd-resit\tasks\image1.jpg", "test-moto-server", "image1.jpg")
    response = s3_client.get_object(
        Bucket='test-moto-server',
        Key='image1.jpg',
    )
    print(response)
    img_in_response = response["Body"]
    print(img_in_response)
    outfile = io.BytesIO()
    s3_client.download_fileobj("test-moto-server", "image1.jpg", outfile)
    outfile.seek(0)
    Image.open(outfile).save(r"C:\Users\sleep\software-dev-2024\cpd-resit\lambda.jpg") 
