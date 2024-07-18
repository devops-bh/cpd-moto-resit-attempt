from moto import mock_aws
import boto3

@mock_aws
def main():
    print(boto3.client("sns", region_name="us-east-1").create_topic(Name="nameless2"))
    print(boto3.client("sns", region_name="us-east-1").create_topic(Name="nameless2"))
    print(boto3.client("sns", region_name="us-east-1").create_topic(Name="nameless2"))
    print(boto3.client("sns", region_name="us-east-1").create_topic(Name="nameless2"))


main()