import boto3

codedeploy = boto3.client('codedeploy', region_name='ap-south-1')

# 1. Create a CodeDeploy application
app_name = 'NodeJS-WebApp'
try:
    codedeploy.create_application(
        applicationName=app_name,
        computePlatform='Server'
    )
    print(f"✅ CodeDeploy Application '{app_name}' created.")
except codedeploy.exceptions.ApplicationAlreadyExistsException:
    print(f"CodeDeploy Application '{app_name}' already exists.")

# 2. Create a Deployment Group (targeting EC2 via tags)
# Ensure your EC2 instances have the tag Key=App, Value=NodeJSApp
# and that the Role ARN exists.
try:
    codedeploy.create_deployment_group(
        applicationName=app_name,
        deploymentGroupName='NodeJSApp-ProdGroup',
        serviceRoleArn='arn:aws:iam::693878106320:role/final_aws_project_7',  # Replace with valid CodeDeploy service role
        ec2TagFilters=[
            {
                'Key': 'App',
                'Value': 'NodeJSApp',
                'Type': 'KEY_AND_VALUE'
            }
        ]
    )
    print("✅ CodeDeploy Deployment Group 'NodeJSApp-ProdGroup' created.")
except codedeploy.exceptions.DeploymentGroupAlreadyExistsException:
    print("Deployment Group already exists.")
except Exception as e:
    print(f"Error creating deployment group: {e}")
