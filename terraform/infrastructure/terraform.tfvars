project_name = "ml-pipeline-terraform-aws"
region = "us-west-2"

training_instance_type = "ml.m5.medium"
inference_instance_type = "ml.c5.medium"
volume_size_sagemaker = 5

handler_path = "../../src/lambda_function"
handler = "config_lambda.lambda_handler"