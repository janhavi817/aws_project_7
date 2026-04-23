import boto3

codebuild = boto3.client('codebuild', region_name='ap-south-1')

response = codebuild.create_project(
    name='NodeJSBuildProject',
    
    source={
        'type': 'GITHUB',
        'location': 'https://github.com/janhavi817/aws_project_7'
    },
    
    artifacts={
        'type': 'S3',
        'location': 'janhavi-nodejs-cicd-2026'
    },
    
    environment={
        'type': 'LINUX_CONTAINER',
        'image': 'aws/codebuild/standard:7.0',
        'computeType': 'BUILD_GENERAL1_SMALL'
    },
    
    serviceRole='arn:aws:iam::693878106320:role/CodeBuildServiceRole'
)

print("✅ CodeBuild project created")