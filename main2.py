#Main Class

from models.FBProphetModel import FBProphetModel
from models.ARIMAModel import ARIMAModel
from models.HoltWintersModel import HoltWintersModel

import pandas as pd

if __name__ == "__main__":
    # Read the Excel file into a DataFrame
    data =  pd.read_csv('Data/data.csv')
    
    # Create an instance of FBProphetModel
    fb_prophet_model = FBProphetModel()
    # Call train_and_forecast for FBProphetModel and pass the data
    prediction_FBProphetModel = fb_prophet_model.train_and_forecast(data)

    # Create an instance of ARIMAModel
    arima_model = ARIMAModel()
    # Call train_and_forecast for arima_model ARIMAModel and pass the data
    prediction_ARIMAModel = arima_model.train_and_forecast(data)

    # Create an instance of HoltWintersModel
    HoltWintersModel = HoltWintersModel()
    
    # Call train_and_forecast for  HoltWintersModel and pass the data
    prediction_HoltWintersModel = HoltWintersModel.train_and_forecast(data)

    # Export the predicted values to an Excel file
    prediction_FBProphetModel.to_csv('Data/Output/FBProphetModel.csv', index=False) 
    prediction_ARIMAModel.to_csv('Data/Output/ARIMAModel.csv', index=False)
    prediction_HoltWintersModel.to_csv('Data/Output/HoltWintersModel.csv', index=False)

    print("Predictions exported successfully to CSV files")





