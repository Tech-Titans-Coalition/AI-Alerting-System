### Variations of algorithm

This algorithm was created for a specific use case in this initial situation, in regards to the training of the meteorite.json training. However, this algorithm can be used to input any format of dataset, you will need to change some variables and logic. 
For instance, you can see that in the CSV version I have used class as my entry and pivot analysis, this needs to change based on your dataset. As well as in the JSON config I have preprocessed the Y table to allow for my X table to absorb a predetermined set
of data. This is especially useful for large datasets with multiple features. However, I have included suitable code for assessing large datasets as you are aware. You as the user may be well aware of this but as a note I needed to include this for clarity. 
What I am presenting to you is a structure that is easily customizable based on your needs so feel free to do what you wish when deviating from this.

-Example:

![Screenshot 2024-05-03 132545](https://github.com/Daazd/Machine-Learning-Pipeline-SageMaker/assets/148648249/5198ab53-782e-461c-a9a0-b75c8a491349)

### Citation for documentation when effectively implementing GridSearchCV for use with RandomForestClassifier

https://www.kaggle.com/code/sociopath00/random-forest-using-gridsearchcv

### Citation for NumPy

https://numpy.org/doc/stable/user/whatisnumpy.html

- Explanation of Practices:
  - In essence what I tried to do is use the most efficient scanning practices to decifer the RandomForestClassifier, as it is a decision tree model that parses over a large amount of data. With numpy we can iterate over these large sets of data effectively and implement efficient         computation using principles of Linear Algebra, which would ultimately be more effective than python lists.
  - With GridSearchCV we can also use the best decisions coming out of RandomForestClassifier using a scoring method, which you can see with the declaration clf = grid_search.best perameter.
  - Label Encoder was also utilized due to the fact in datasets categorical columns can often vary. By doing this we can convert categorical columns into numerical ones so that they can be utilized by training algorithms, which only take in numerical data.
