#FBProphetModel

#import pandas as pd
from prophet import Prophet
 
class FBProphetModel:
    """
    A class representing the FBProphet model for demand forecasting.

    Attributes:
        None

    Methods:
        train_and_forecast(data, predictionDays):
            Trains the FBProphet model on the given data and makes future predictions.

    """

    def train_and_forecast(self, data,testDays, predictionDays):
        """
        Trains the FBProphet model on the given data and makes future predictions.

        Args:
            data (pandas.DataFrame): The input data for training the model.
            predictionDays (int): The number of days to forecast into the future.

        Returns:
            pandas.DataFrame: A DataFrame containing the predicted values for the next `predictionDays` days.

        """
        # Prepare the data for Prophet
        prophet_data = data.rename(columns={'ds': 'ds', 'y': 'y'})

        # Initialize Prophet model
        m = Prophet(interval_width=0.95)

        # Fit the Prophet model
        m.fit(prophet_data)

        # Make future predictions for the next `predictionDays` days
        future = m.make_future_dataframe(periods=testDays+predictionDays)
        forecast_prophet = m.predict(future)

        # Extract predicted values for the next `predictionDays` days
        predicted_values_prophet = forecast_prophet[['ds', 'yhat']].tail(testDays+predictionDays)
        # Rename the columns to 'ds' and 'predicted'
        predicted_values_prophet = predicted_values_prophet.rename(columns={'yhat': 'predicted'})
        return predicted_values_prophet  # Returning the predicted values

"""      def predict(self,testDays, predictionDays):
        # Implement the prediction logic for FBProphet
        print("Predicting with FBProphet")
        return None """





