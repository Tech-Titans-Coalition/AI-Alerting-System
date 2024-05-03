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

### Variations of algorithm and a note to user.
This algorithm was created for a specific use case, in the training of the meteorite.json training. However, this algorithm can be used to input any format of dataset, you will need to change some variables and logic. 
For instance, you can see that in the CSV version I have used class as my entry and pivot analysis, this needs to change based on your dataset. As well as in the JSON config I have preprocessed the Y table to allow for my X table to absorb a predetermined set
of data. This is especially useful for large datasets with multiple features. However, I have included suitable code for assessing large datasets as you are aware. You as the user may be well aware of this but as a note I needed to include this for clarity. 
What I am presenting to you is a structure that is easily customizable based on your needs so feel free to do what you wish when deviating from this.

-Example:
![Screenshot 2024-05-03 132401](https://github.com/Daazd/Machine-Learning-Pipeline-SageMaker/assets/148648249/6f7c691a-65ae-4ee9-9621-c171225067ab)

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
view of where the error is. 
Once this is complete you will see a completed green pipeline and an endpoint that has the InService tag.


