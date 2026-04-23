import boto3
import time
import json

ec2 = boto3.client('ec2', region_name='ap-south-1')
iam = boto3.client('iam')

def setup_ec2():
    try:
        # 1. Create a Trust Policy for EC2
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # 2. Create IAM Role for EC2
        role_name = 'EC2-CodeDeploy-Role'
        try:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy)
            )
            print("✅ IAM Role created")
        except iam.exceptions.EntityAlreadyExistsException:
            print("IAM Role already exists")
            
        # Attach required policies
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess')
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy')
        
        # 3. Create Instance Profile
        profile_name = 'EC2-CodeDeploy-Instance-Profile'
        try:
            iam.create_instance_profile(InstanceProfileName=profile_name)
            iam.add_role_to_instance_profile(InstanceProfileName=profile_name, RoleName=role_name)
            print("✅ Instance Profile created")
            time.sleep(10) # wait for profile to propagate
        except iam.exceptions.EntityAlreadyExistsException:
            print("Instance Profile already exists")
            
        # 4. Launch EC2 Instance with User Data (Install CodeDeploy & Node)
        user_data_script = """#!/bin/bash
yum update -y
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-ap-south-1.s3.ap-south-1.amazonaws.com/latest/install
chmod +x ./install
./install auto
service codedeploy-agent start
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs
"""

        # Fetch latest Amazon Linux 2 AMI in ap-south-1
        ssm = boto3.client('ssm', region_name='ap-south-1')
        ami_param = ssm.get_parameter(Name='/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2')
        ami_id = ami_param['Parameter']['Value']

        print(f"Launching EC2 instance using AMI: {ami_id}...")
        instances = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            IamInstanceProfile={'Name': profile_name},
            UserData=user_data_script,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'App', 'Value': 'NodeJSApp'}]
            }]
        )
        instance_id = instances['Instances'][0]['InstanceId']
        print(f"✅ EC2 Instance launched successfully: {instance_id}")

    except Exception as e:
        print(f"Error provisioning EC2: {e}")

if __name__ == "__main__":
    setup_ec2()
