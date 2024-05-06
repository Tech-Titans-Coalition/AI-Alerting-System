### Variations of algorithm

This algorithm was created for a specific use case in this initial situation, in regards to the training of the meteorite.json training. However, this algorithm can be used to input any format of dataset; you will need to change some variables and logic. 
For instance, you can see that in the CSV version I have used class as my entry and pivot analysis, this needs to change based on your dataset. As well as in the JSON config I have preprocessed the Y table to allow for my X table to absorb a predetermined set
of data. This is especially useful for large datasets with multiple features. However, I have included suitable code for assessing large datasets as you are aware. You as the user may be well aware of this but as a note I needed to include this for clarity. 
What I am presenting to you is a structure that is easily customizable based on your needs so feel free to do what you wish when deviating from this. 

-Example:

![Screenshot 2024-05-03 132545](https://github.com/Daazd/Machine-Learning-Pipeline-SageMaker/assets/148648249/5198ab53-782e-461c-a9a0-b75c8a491349)

### Concerning ECR and Docker Images

ECR functions in the same way as a github repository. ECR will mount the image and utilize what is contained in the image for use by Step Functions. It is important to note that when you make changes to the python code you will need to re upload your Docker file to ECR to utilize the latest changes you have made. Once the image is pushed to the ECR url specified in your terraform code it is best practice to do a scan on the image. If your scan comes back with critical errors then determine the nature of the issues and where they derive. Usually with these sorts of critical errors it has to do with the version of your dependencies make sure that you have the latest versions of your dependencies. The requirements.txt forms your environment so if you wish to add any dependencies or alter them, then start with that file. 

### Concerning Step Functions and SageMaker

When we applied the Terraform configuration we created a State Machine to run our Step Functions, this is how we will execute the training of the model and the configuration of endpoints. Along with the State Machine we created we also
deployed S3 buckets as retainers for model data as well as an output path for a trained model. This is what you see stated in the algorithm code as output_path, training_path, and model_path. You can check the health and status of the training job
in the SageMaker console. You can also look and see the graph view in the execution console. If you run into errors training check the cloudwatch logs for more clarity on what issue is arising, however the step execution console will give you a detailed 
view of where the error is and where it occured in the pipeline. 
You are able to alter the step function code to suit whatever purpose you wish, I have implemented one for multi-format input but you are able to scale it.

### Scripts for JSON input 

```shell script
{
  "datasetType": "iris",
  "training_job_name": "my-training-job" #Feel free to change these as they are just identifiers for jobs for organization 
}

{
  "datasetType": "meteorite",
  "training_job_name": "my-training-job"
}
```

### Citation for documentation concerning effectively implementing GridSearchCV for use with RandomForestClassifier

https://www.kaggle.com/code/sociopath00/random-forest-using-gridsearchcv

### Citation for NumPy

https://numpy.org/doc/stable/user/whatisnumpy.html

### Terraform Documentation

https://developer.hashicorp.com/terraform/docs

### Explanation of Practices:
  - In essence what I tried to do is use the most efficient scanning practices to decifer the RandomForestClassifier, as it is a decision tree model that parses over a large amount of data. With numpy we can iterate over these large sets of data effectively and implement efficient         computation using principles of Linear Algebra, which would ultimately be more effective than python lists.
  - With GridSearchCV we can also use the best decisions coming out of RandomForestClassifier using a scoring method, which you can see with the declaration clf = grid_search.best perameter.
  - Label Encoder was also utilized due to the fact in datasets categorical columns can often vary. By doing this we can convert categorical columns into numerical ones so that they can be utilized by training algorithms, which only take in numerical data.
