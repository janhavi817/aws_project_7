import boto3

s3 = boto3.client('s3')

bucket_name = 'janhavi-nodejs-cicd-2026'

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    }
)