#HoltWintersModel

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
from datetime import timedelta
class HoltWintersModel:
    """
    Holt-Winters Model for demand forecasting.

    This class provides methods to train the Holt-Winters model on given data and forecast future values.

    Attributes:
        None

    Methods:
        train_and_forecast(data, predictionDays):
            Trains the Holt-Winters model on the given data and forecasts values for the specified number of days.

    """

    def train_and_forecast(self, data,testDays ,predictionDays):
        """
        Trains the Holt-Winters model on the given data and forecasts values for the specified number of days.

        Args:
            data (pandas.DataFrame): The input data containing 'ds' (datetime) and 'y' (target variable) columns.
            predictionDays (int): The number of days to forecast.

        Returns:
            pandas.DataFrame: A DataFrame containing the forecasted values and corresponding dates.

        """
     
        # Fit the Exponential Smoothing model
        model_hw = ExponentialSmoothing(data['y'], seasonal='add', seasonal_periods=12)
        trained_hw = model_hw.fit()
        
        # Forecast for the next predictionDays days
        predicted_values_hw = trained_hw.forecast(steps=testDays+predictionDays)

        # Ensure 'ds' column is in datetime format
        data['ds'] = pd.to_datetime(data['ds'])
        
        # Step 1: Find the maximum date in 'ds'
        last_date = data['ds'].max()
        
        # Generate next dates for predictionDayss
        next_dates = [last_date + timedelta(days=i) for i in range(1, testDays+predictionDays + 1)] 

        # Create a DataFrame for the forecasted values and dates
        forecast_df = pd.DataFrame({
            'ds': next_dates,
            'predicted': predicted_values_hw
        })
        
        return forecast_df
    
"""         def predict(self,testDays, predictionDays):
            # Implement the prediction logic for Holt Winter model
            print("Predicting with Holt Winter ")
            return None """
