#FBProphetModel

#import pandas as pd
from prophet import Prophet
 
class FBProphetModel:
    def train_and_forecast(self, data):

 
        # Prepare the data for Prophet
        prophet_data = data.rename(columns={'TransactionDate': 'ds', 'GroupQuantity': 'y'})

        # Initialize Prophet model
        m = Prophet( interval_width=0.95)
        

        # Fit the Prophet model
        m.fit(prophet_data)

        # Make future predictions for the next 30 days
        future = m.make_future_dataframe(periods=30)
        forecast_prophet = m.predict(future)

        # Extract predicted values for the next 30 days
        predicted_values_prophet = forecast_prophet[['ds', 'yhat']].tail(30)
        return predicted_values_prophet  # Returning the predicted values

 




