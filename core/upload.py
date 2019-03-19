import boto3
from botocore.client import Config
import os

ACCESS_KEY_ID = 'AKIAIPEPT7GFYD5VOZRQ'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'wanderift'

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
i=0
bucket = s3.Bucket(BUCKET_NAME)
dir = "E:\downloaded\magz"
for file in os.listdir(dir):
    with open(os.path.join(dir,file), 'rb') as data:

        bucket.Object('magz/'+file).put(Body=data, ACL='public-read')
        i=+1
        print(file)
        print('success')
        print('success')