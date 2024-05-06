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

After you have configured the file to your specific needs, follow the steps outlined below to deploy with Terraform.do a scan on the image to make sure all dependencies are installed correctly and you have no critical errorsIf your scan comes back with errors then the errors are most likely with how you constructed your environment in the Docker File/requirements.txt. Make sure you are using the latest versions and do not have deprecated resources.

```shell script
export AWS_PROFILE=<your_aws_cli_profile_name>

cd terraform/infrastructure

terraform init

terraform plan

terraform apply
```
Once the Terraform has successfully applied check the output to see if the ECR repository was successfully constructed. The Terraform code provided includes an output of the repository URL that it was created at.
Once that is done check ECR on AWS for successful completion and mounting.
Once this is done we can build and construct the Docker image and push it to ECR.

### Push your Docker Image to ECR

For the ML pipeline and Sagemaker to properly train the datasets we are feeding and provision an endpoint for inference, you need to provide a Docker image and store it in ECR.
This operation functions much in the same way as a github repository used in an automation process to clone the image and use its contents for application.
That being said if you make changes to your code for the algorithm you will need to repeat these steps everytime it is changed, much in the same way you would for Terraform. That probably goes without saying, but it is important to make a note of.
Below I have outlined steps for building, tagging, and pushing to the ECR repository created in the Terraform code.

```shell script
cd src/container

export AWS_PROFILE=<your_aws_cli_profile_name> #If already done at the step above and profile still active, skip this step

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <account_number>.dkr.ecr.eu-west-1.amazonaws.com

docker build -t ml-training . #This is the name of your Docker Image you will be using feel free to edit this to whatever you like.

docker tag ml-training:latest <account_number>.dkr.ecr.eu-west-1.amazonaws.com/<ecr_repository_name>:latest

docker push <account_number>.dkr.ecr.eu-west-1.amazonaws.com/<ecr_repository_name>
```

After you have successfully pushed to ECR do a scan on the image to make sure all dependencies are installed correctly and you have no critical errors.
If your scan comes back with errors then the errors are most likely with how you constructed your environment in the Docker File/requirements.txt. Make sure you are using the latest versions and do not have deprecated resources.

### Run the ML pipeline

In order to train and run the ML pipeline, go to Step Functions and start the execution.
When we applied the Terraform configuration we created a State Machine to run our Step Functions, this is how we will execute the training of the model and the configuration of endpoints. Along with the State Machine we created we also
deployed S3 buckets as retainers for model data as well as an output path for a trained model. This is what you see stated in the algorithm code as output_path, training_path, and model_path. You can check the health and status of the training job
in the SageMaker console. You can also look and see the graph view in the execution console. If you run into errors training check the cloudwatch logs for more clarity on what issue is arising, however the step execution console will give you a detailed 
view of where the error is and where it occured in the pipeline. 
Once this is complete you will see a completed green pipeline and an endpoint that has the InService tag.

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
