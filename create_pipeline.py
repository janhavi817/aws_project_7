import boto3
import os

# Get GitHub token (make sure you set it in terminal)
github_token = os.getenv("GITHUB_TOKEN")

codepipeline = boto3.client('codepipeline', region_name='ap-south-1')

pipeline = {
    'pipeline': {
        'name': 'NodeJSPipeline',
        
        'roleArn': 'arn:aws:iam::693878106320:role/final_aws_project_7',
        
        'artifactStore': {
            'type': 'S3',
            'location': 'janhavi-nodejs-cicd-2026'
        },
        
        'stages': [
            {
                'name': 'Source',
                'actions': [{
                    'name': 'Source',
                    'actionTypeId': {
                        'category': 'Source',
                        'owner': 'ThirdParty',
                        'provider': 'GitHub',
                        'version': '1'
                    },
                    'outputArtifacts': [{'name': 'SourceOutput'}],
                    'configuration': {
                        'Owner': 'janhavi817',
                        'Repo': 'aws_project_7',
                        'Branch': 'main',
                        'OAuthToken': github_token
                    },
                    'runOrder': 1
                }]
            },
            {
                'name': 'Build',
                'actions': [{
                    'name': 'Build',
                    'actionTypeId': {
                        'category': 'Build',
                        'owner': 'AWS',
                        'provider': 'CodeBuild',
                        'version': '1'
                    },
                    'inputArtifacts': [{'name': 'SourceOutput'}],
                    'outputArtifacts': [{'name': 'BuildOutput'}],
                    'configuration': {
                        'ProjectName': 'NodeJSBuildProject'
                    },
                    'runOrder': 1
                }]
            },
            {
                'name': 'Deploy',
                'actions': [{
                    'name': 'DeployToEC2',
                    'actionTypeId': {
                        'category': 'Deploy',
                        'owner': 'AWS',
                        'provider': 'CodeDeploy',
                        'version': '1'
                    },
                    'inputArtifacts': [{'name': 'BuildOutput'}],
                    'configuration': {
                        'ApplicationName': 'NodeJS-WebApp',
                        'DeploymentGroupName': 'NodeJSApp-ProdGroup'
                    },
                    'runOrder': 1
                }]
            }
        ],
        'version': 1
    }
}

try:
    response = codepipeline.create_pipeline(pipeline=pipeline['pipeline'])
    print("✅ Pipeline created successfully")
except codepipeline.exceptions.PipelineNameInUseException:
    response = codepipeline.update_pipeline(pipeline=pipeline['pipeline'])
    print("✅ Pipeline updated successfully")