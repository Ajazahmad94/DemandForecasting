import time
from flask import Flask, request, jsonify
import pandas as pd
from models.FBProphetModel import FBProphetModel
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    data_set = {'Page': 'Home', 'Message': 'Successfully Loaded the Home Page', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/upload_dataframe', methods=['POST'])
def upload_dataframe():
    try:
        json_data = request.get_json()  # Get JSON data from the request
        if json_data:
            # Assuming the DataFrame is sent in JSON format
            df = pd.read_json(json.dumps(json_data))
            
            #print(df)
            # Create an instance of FBProphetModel
            fb_prophet_model = FBProphetModel()
            
            # Call train_and_forecast for FBProphetModel and pass the data
            prediction_FBProphetModel = fb_prophet_model.train_and_forecast(df)
            print(prediction_FBProphetModel)
            # Convert predictions to JSON and return
            predictions_json = prediction_FBProphetModel.to_json()
            return jsonify({'predictions': json.loads(predictions_json)})
        else:
            return jsonify({'error': 'No JSON data received'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    