#Main Class

from models.FBProphetModel import FBProphetModel
from models.ARIMAModel import ARIMAModel
from models.HoltWintersModel import HoltWintersModel
from models.Utilities.fileIO import loadCsvExcelFile
from models.neuralProphetModel import neuralProphetModel

import pandas as pd
import os
import sys
from datetime import timedelta

# Change to the desired working directory
os.chdir('/home/ajaz/DemandForecasting')
# Add the directory containing the Utilities module to the sys.path
sys.path.append('/home/ajaz/DemandForecasting/models')


predictionDays = 10
testDays = 30
# main.py


def split_data(data, testDays, predictionDays):
    """
    Splits the given data into training and testing sets.

    Parameters:
    - data: The input data to be split.
    - predictionDays: The number of days to be used for testing.

    Returns:
    - train_data: The training data containing all but the last `predictionDays` rows.
    - test_data: The testing data containing the last `predictionDays` rows.
    """
    return data.iloc[:-testDays], data.iloc[-testDays:]

def predict(model_instance, testDays, predictionDays):
    """
    Make predictions using the trained model_instance.
    Args:
        model_instance: The trained model instance used for making predictions.
        predictionDays: The number of days for which predictions are to be made.
    Returns:
        forecasts: The predicted values for the specified number of days.
    """
    forecasts = model_instance.predict(predictionDays)
    return forecasts


if __name__ == "__main__":
    # Read the Excel file into a DataFrame
    
    data =  pd.read_csv('/home/ajaz/DemandForecasting/Data/data.csv')
    trainData , testData = split_data(data, testDays, predictionDays)

    #Create an instance of FBProphetModel
    fb_prophet_model = FBProphetModel()
    prediction_FBProphetModel = fb_prophet_model.train_and_forecast(trainData,testDays, predictionDays)

    # Create an instance of ARIMAModel
    arima_model = ARIMAModel()
    prediction_ARIMAModel = arima_model.train_and_forecast(trainData,testDays, predictionDays)

    # Create an instance of HoltWintersModel
    HoltWintersModel = HoltWintersModel()
    prediction_HoltWintersModel = HoltWintersModel.train_and_forecast(trainData,testDays, predictionDays)

    # Create an instance of neuralProphetModel
    neuralProphetModel = neuralProphetModel()
    prediction_neuralProphetModel = neuralProphetModel.train_and_forecast(trainData, testDays,predictionDays) 

    testData['ds'] = pd.to_datetime(testData['ds'])
    #export the test data and the predictions to a csv file


    #join the prediction_FBProphetModel and forecasted_dates on the basis of ds column and Add the model name as column name for the predicted values

    final_output = pd.merge(testData, prediction_FBProphetModel, on='ds', how='outer')
    final_output.rename(columns={'predicted':'fbProphetValue'}, inplace=True)
    #join the prediction_ARIMAModel and forecasted_dates on the basis of ds column and Add the model name as column name for the predicted values
    final_output = pd.merge(final_output, prediction_ARIMAModel, on='ds', how='outer')
    final_output.rename(columns={'predicted':'ARIMAValue'}, inplace=True)
    #join the prediction_HoltWintersModel and forecasted_dates on the basis of ds column and Add the model name as column name for the predicted values
    final_output = pd.merge(final_output, prediction_HoltWintersModel, on='ds', how='outer')
    final_output.rename(columns={'predicted':'HoltValue'}, inplace=True)
    
    #join the prediction_neuralProphetModel and forecasted_dates on the basis of ds column and Add the model name as column name for the predicted values
    final_output = pd.merge(final_output, prediction_neuralProphetModel, on='ds', how='outer')
    final_output.rename(columns={'predicted':'neuralProphetValue'}, inplace=True)
     
    final_output.to_csv('Data/Output/FinalOutput.csv', index=False)
    print("Final Output exported successfully to CSV file")


