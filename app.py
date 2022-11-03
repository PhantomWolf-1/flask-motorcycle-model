from pickle import load

import numpy as np
import pandas as pd
import shap
from flask import Flask, request, abort
from keras.saving.save import load_model

app = Flask(__name__)

model = load(open("model/motor-model.pkl", "rb"))
model_classifications = ['Custom / cruiser', 'Naked bike', 'Sport', 'Touring']


@app.route('/', methods=['POST'])
def predict():
    json = request.get_json(force=True, silent=False, cache=True)
    #retrieving input data
    message = json['message']
    seat_height = json['seat_height']
    dry_weight = json['dry_weight']
    wheelbase = json['wheelbase']
    power = json['power']
    displacement = json['displacement']
    torque = json['torque']
    
    #makes the prediction
    prediction_input = np.reshape([displacement, power, torque, dry_weight, wheelbase, seat_height], (1, -1))
    outcome = model.predict(prediction_input)
    #gets the classification
    outcome_classification = model_classifications[np.argmax(outcome)]

    #TODO: implement shap and get some feature affection and get that in the json

    return {
        'response': "HGHELLUU",
        'initial message' : message,
        'outcome' : outcome_classification
    }


@app.before_request
def only_json():
    if not request.is_json:
        abort(400)