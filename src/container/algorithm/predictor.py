from __future__ import print_function
from sklearn.preprocessing import StandardScaler

import os
import json
import pickle
from io import StringIO
import sys
import signal
import traceback
import logging
import time
import os
import psutil #type: ignore
import flask 

import pandas as pd

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
logging.basicConfig(level=logging.INFO)

# A predictor model that can be adjusted to whatver type of data format you would 
# like to feed. Opened up for customization to user's needs.

class ScoringService(object):
    model = {}               

    @classmethod
    def get_model(cls, model_name):
        if model_name not in cls.model:
            with open(os.path.join(model_path, f'{model_name}.pkl'), 'rb') as inp:
                cls.model[model_name] = pickle.load(inp)
        return cls.model[model_name]

    @classmethod
    def predict(cls, input):
        clf = cls.get_model()
        return clf.predict(input)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    model_name = flask.request.headers.get('model_name', 'default-model')
    health = ScoringService.get_model(model_name) is not None  

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    start_time = time.time()
    model_name = flask.request.headers.get('model_name', 'default-model')
    model = ScoringService.get_model(model_name)
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == 'text/csv':
        data = pd.read_csv(StringIO(flask.request.data.decode('utf-8')), header=None)
    elif flask.request.content_type == 'application/json':
        data = pd.read_json(StringIO(flask.request.data.decode('utf-8')))
    else:
        return flask.Response(response='This predictor only supports CSV and JSON data', status=415, mimetype='text/plain')

    logging.info('Invoked with {} records'.format(data.shape[0]))

    # Preprocessing Data
    scaler = StandardScaler()
    data = scaler.fit_transform(data) 

    # Do the prediction
    predictions = model.predict(data)
    print(predictions)

    # Postprocessing Data
    predictions = [1 if prob > 0.5 else 0 for prob in predictions]

    # Convert from numpy back to CSV
    out = StringIO()
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    # Logging outputs and system metrics
    elapsed_time = time.time() - start_time
    cpu_pct = psutil.cpu_percent()
    mem_pct = psutil.virtual_memory().percent
    logging.info(f'Elapsed time: {elapsed_time} seconds')
    logging.info(f'CPU Utilization: {cpu_pct}%')
    logging.info(f'Memory Usage: {mem_pct}%')

    return flask.Response(response=result, status=200, mimetype='text/csv')
