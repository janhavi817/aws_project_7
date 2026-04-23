import boto3
import json

iam = boto3.client('iam')

assume_role_policy = json.dumps({
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "Service": "codebuild.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }]
})

role = iam.create_role(
    RoleName='CodeBuildServiceRole',
    AssumeRolePolicyDocument=assume_role_policy
)

iam.attach_role_policy(
    RoleName='CodeBuildServiceRole',
    PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
)

print("Role ARN:", role['Role']['Arn'])

