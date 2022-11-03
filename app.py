from pickle import load

import pandas as pd
import shap
from flask import Flask, request, abort
from keras.saving.save import load_model

app = Flask(__name__)



@app.route('/', methods=['POST'])
def predict():
    #json = request.get_json(force=True, silent=False, cache=True)

    return {
        'response': "HGHELLUU",
    }


#@app.before_request
#def only_json():
#    if not request.is_json:
#        abort(400)