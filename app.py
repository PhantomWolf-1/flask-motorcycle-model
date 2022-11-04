from pickle import load

import numpy as np
import pandas as pd
import shap
from flask import Flask, request, abort
from keras.saving.save import load_model

app = Flask(__name__)

model = load(open("model/motor-modelV2.pkl", "rb"))
model_classifications = ['Custom / cruiser', 'Naked bike', 'Sport', 'Touring']
'''
for the describe function, indexes
0 = count
1 = mean
2 = std
3 = min 
4 = 25%
5 = 50%
6 = 75%
7 = max
'''

@app.route('/', methods=['GET'])
def modelInformation():
    print("GET request received!!")

    return { 
        'message' : "GET request not in use..."
    }

    # print("GET request received!!")
    # df = pd.read_csv('model/cleaned_dfV2.csv')
    # df_describtion = df.describe()
    # #print(df.describe())
    # # Getting al the min and max input possibilities
    # minDisplacement = df_describtion['Displacement (ccm)'].iloc[3]
    # maxDisplacement = df_describtion['Displacement (ccm)'].iloc[7]

    # minPower = df_describtion['Power (hp)'].iloc[3]
    # maxPower = df_describtion['Power (hp)'].iloc[7]

    # minTorque = df_describtion['Torque (Nm)'].iloc[3]
    # maxTorque = df_describtion['Torque (Nm)'].iloc[7]

    # minDry_weight = df_describtion['Dry weight (kg)'].iloc[3]
    # maxDry_weight = df_describtion['Dry weight (kg)'].iloc[7]

    # minWheelbase = df_describtion['Wheelbase (mm)'].iloc[3]
    # maxWheelbase = df_describtion['Wheelbase (mm)'].iloc[7]

    # minSeat_height = df_describtion['Seat height (mm)'].iloc[3]
    # maxSeat_height = df_describtion['Seat height (mm)'].iloc[7]




    # print("min value of power", df_describtion['Power (hp)'].iloc[3])
    

    # #print(model.describe())
    # return {
    #     'message' : "get request accepted",
    #     'displacement' : {
    #         'min' : int(minDisplacement),
    #         'max' : int(maxDisplacement)
    #     },
    #     'power' : {
    #         'min' : int(minPower),
    #         'max' : int(maxPower)
    #     },
    #     'torque' : {
    #         'min' : int(minTorque),
    #         'max' : int(maxTorque)
    #     },
    #     'dry_weight' : {
    #         'min' : int(minDry_weight),
    #         'max' : int(maxDry_weight)
    #     },
    #     'wheelbase' : {
    #         'min' : int(minWheelbase),
    #         'max' : int(maxWheelbase)
    #     },
    #     'seat_height' : {
    #         'min' : int(minSeat_height),
    #         'max' : int(maxSeat_height)
    #     },
    # }

    

@app.route('/', methods=['POST'])
def predict():
    print("POST request received!!")
    json = request.get_json(force=True, silent=False, cache=True)
    print("json received:\n", json)
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
    outcome_index = np.argmax(outcome)
    outcome_classification = model_classifications[outcome_index]
    print(outcome_classification)

    clf_explainer = shap.TreeExplainer(model)
    shap_values = np.array(clf_explainer.shap_values(prediction_input))
    feature_values_prediction = shap_values[(outcome_index+1) + outcome_index][0]


    return {
        'response': "HGHELLUU",
        'initial message' : message,
        'outcome' : outcome_classification,
        'feature_values_prediction' : {
            'displacement' : feature_values_prediction[0],
            'power' : feature_values_prediction[1],
            'torque' : feature_values_prediction[2],
            'dry_weight' : feature_values_prediction[3],
            'wheelbase' : feature_values_prediction[4],
            'seat_height' : feature_values_prediction[5],
        }
    }


#@app.before_request
#def only_json():
#    if not request.is_json:
#        abort(400)