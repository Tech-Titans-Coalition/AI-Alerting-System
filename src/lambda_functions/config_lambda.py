import time
import json
import boto3
import pandas as pd
from sklearn.cluster import KMeans, AffinityPropagation
from io import StringIO

athena_client = boto3.client('athena')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Setting up query parameters
    database = 'data_lake_athena_db'
    query = "SELECT * FROM your_table_name" # This is where we customize our queries for the data we want to analyze
    output_location = 's3://our_query_results_bucket/' # This is where we want our query results to be stored
    
    # Running the query
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': output_location,
        }
    )
    
    # Getting the query execution ID
    query_execution_id = response['QueryExecutionId']
    
    # Waiting for the query to finish
    while True:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = query_status['QueryExecution']['Status']['State']
        
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        
        time.sleep(2)
        
    if status == 'SUCCEEDED':
        # Fetch the query results
        result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        
        # Parsing the query results
        columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = [[field.get('VarCharValue') for field in row['Data']] for row in result['ResultSet']['Rows'][1:]]
        
        df = pd.DataFrame(rows, columns=columns)
        
        # Here is where we perfom the clustering analysis
        affinity_prop = AffinityPropagation().fit(df)
        kmeans = KMeans(n_clusters=len(set(affinity_prop.labels_))).fit(df)
        
        df['affinity_cluster'] = affinity_prop.labels_
        df['kmeans_cluster'] = kmeans.labels_
        
        # Saving the results to S3
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3_client.put_object(Bucket='our_cluster_data_bucket', Key='clustered_data.csv', Body=csv_buffer.getvalue())
        
        return {
            'statusCode': 200,
            'body': json.dumps('Clustering analysis complete!')
        }
    else:
        raise Exception('Query failed to execute')