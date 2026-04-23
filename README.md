# AWS CI/CD Pipeline for Node.js Application

This project sets up a complete Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Node.js application using AWS native tools.

## Architecture Let's Build
1. **Source**: GitHub repository containing our Node.js app code.
2. **Build**: AWS CodeBuild will test and package our code.
3. **Deploy**: AWS CodeDeploy will deploy the code safely to our EC2 instances.
4. **Orchestration**: AWS CodePipeline manages the flow and triggers on every git push.

## Included Files

### Node.js App
- `package.json` & `index.js`: The Express backend simply returning a response on port 3000.
- `appspec.yml`: Tells CodeDeploy what steps to take during the deployment.
- `scripts/install_dependencies.sh`: Automatically runs `npm install` and sets up PM2.
- `scripts/start_server.sh`: Starts the Node app in the background via PM2.
- `scripts/stop_server.sh`: Shuts down the previous version of the app to free up port 3000.

### AWS Setup Scripts (Python Boto3)
- `iam_roles.py`: Sets up service roles.
- `s3_bucket.py`: Creates the S3 artifact store.
- `create_build.py`: Provisions the CodeBuild project.
- `create_codedeploy.py`: Provisions CodeDeploy resources to push to EC2.
- `create_pipeline.py`: Orchestrates everything.

## How to execute

1. Setup an EC2 instance running Amazon Linux 2 with the AWS CodeDeploy Agent installed and a Role containing `AmazonS3ReadOnlyAccess`.
2. Push this folder to your GitHub repo (`janhavi817/aws_project_7`).
3. Run the python scripts (make sure `GITHUB_TOKEN` is set in your environment):
   - `python iam_roles.py`
   - `python s3_bucket.py`
   - `python create_build.py`
   - `python create_codedeploy.py`
   - `python create_pipeline.py`

Once configured, any push to `main` branch will automatically be tested, packaged, and deployed directly to the EC2 instances!
