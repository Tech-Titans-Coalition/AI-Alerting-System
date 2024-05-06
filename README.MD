# Tutorial

This is a multi-format algorithm designed to leverage the SageMaker service provided by AWS. Through Terraform we can implement an ECR repository, multiple S3 buckets, create a State Machine utilizing Step Functions, and Lambda Function Configuration. 

### Pre-Requisites

-Terraform Installed

-AWS account

-Python V3.7 or higher

-Docker Desktop

-WSL or Linux OS

### Deploy AWS Infrastructure with Terraform

You are able to clone this repository or create your own Terraform configuration. For the sake of clarity, we will assume you are cloning the repository for the rest of the demo. The configuration for this demo is located in this directory:

```shell script
/terraform
```

First time initialization:

- Open the file "terraform/infrastructure/terraform.tfvars" and adjust the variable "project_name" 
to the name of your project, as well as the variable "region" if you want to deploy in another region.
Further, you can change additional variables such as instance types for training and inference.

After you have configured the file to your specific needs, follow the steps outlined below to deploy with Terraform

```shell script
export AWS_PROFILE=<your_aws_cli_profile_name>

cd terraform/infrastructure

terraform init

terraform plan

terraform apply
```
Once the Terraform has successfully applied check the output to see if the ECR repository was successfully constructed. The Terraform code provided includes an output of the repository URL that it was created at.
Once that is done check ECR on AWS for successful construction.
Once this is done we can build and construct the Docker image and push it to ECR for mounting.

### Push your Docker Image to ECR

For the ML pipeline and Sagemaker to properly train the datasets we are feeding and provision an endpoint for inference, you need to provide a Docker image and store it in ECR.

```shell script
cd src/container

export AWS_PROFILE=<your_aws_cli_profile_name> #If already done at the step above and profile still active, skip this step

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <account_number>.dkr.ecr.eu-west-1.amazonaws.com

docker build -t ml-training . #This is the name of your Docker Image you will be using feel free to edit this to whatever you like.

docker tag ml-training:latest <account_number>.dkr.ecr.eu-west-1.amazonaws.com/<ecr_repository_name>:latest

docker push <account_number>.dkr.ecr.eu-west-1.amazonaws.com/<ecr_repository_name>
```

### Run the ML pipeline

In order to train and run the ML pipeline, go to Step Functions and start the execution.
You will be able prompted to provide a selection for which data you would like to train based on a JSON input.
I have included the scripts for my algorithm in the NOTE_TO_USER file.
Once the training is complete you will see all green and at this point you can head over to the SageMaker console, then in the inference section click on endpoints.
If the State Machine executed correctly you should see an endpoint with the InService tag.

### Invoke your endpoint
For the next step you have freedom of choice with how you would like to invoke your endpoint you can place it in a python file or use a Jupyter Notebook provided by SageMaker.
Here is a simple script for invoking the CSV model:
```python
import boto3
from io import StringIO
import pandas as pd

client = boto3.client('sagemaker-runtime')

endpoint_name = 'Your endpoint name' # Your endpoint name.
content_type = "text/csv"   # The MIME type of the input data in the request body.

payload = pd.DataFrame([[1.5,0.2,4.4,2.6]])
csv_file = StringIO()
payload.to_csv(csv_file, sep=",", header=False, index=False)
payload_as_csv = csv_file.getvalue()

response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    ContentType=content_type,
    Body=payload_as_csv
    )

label = response['Body'].read().decode('utf-8')
print(label)
```

### Cleanup 

SageMaker is extremely resource heavy so it incurs quite a cost. Due to this fact it is necessary to utilize Terraform destroy to disable the infrastructure. 
Another note to make is that Terraform is only deploying our infrastructure so you will need to manually go through Sagemaker and delete your endpoints. Make sure that the data is removed from your buckets and they are both empty befor incurring Terraform destroy.
I have provided detailed steps to fully shut down the pipeline below:
- Delete the dataset in the S3 training bucket and all models you trained via the ML pipeline in the S3 bucket for the
 models in the AWS Console or via the AWS CLI
 
- Destroy the infrastructure created via Terraform
```shell script
cd terraform/infrastructure

terraform destroy
```
- Delete SageMaker Endpoints, you can do this through the AWS Console or through AWS CLI.

### Thank you for checking out my repo and code!
