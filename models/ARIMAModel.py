#ARIMAModel

from statsmodels.tsa.statespace.sarimax import SARIMAX  
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
from datetime import timedelta

class ARIMAModel:
    """
    ARIMAModel class for training and forecasting using SARIMA model.

    Attributes:
        None

    Methods:
        train_and_forecast: Trains the SARIMA model on the given data and forecasts future values.

    """

    def train_and_forecast(self, data, testDays , predictionDays):
        """
        Trains the SARIMA model on the given data and forecasts future values.

        Args:
            data (DataFrame): The input data containing 'ds' (date) and 'y' (target variable) columns.
            predictionDays (int): The number of days to forecast.

        Returns:
            DataFrame: A DataFrame containing the forecasted dates and predicted values.

        """

        p = 1  # Non-seasonal autoregressive order
        d = 1  # Non-seasonal differencing order
        q = 1  # Non-seasonal moving average order

        P = 1  # Seasonal autoregressive order
        D = 1  # Seasonal differencing order
        Q = 1  # Seasonal moving average order

        s = 12  # Seasonal period
        order = (p, d, q)
        seasonal_order = (P, D, Q, s)       

        model_sarima = SARIMAX(data['y'], order=order, seasonal_order=seasonal_order)

        # Fit the SARIMA model
        trained_sarima = model_sarima.fit()

        # Forecast for the next 'predictionDays' days
        forecast_sarima = trained_sarima.get_forecast(steps= testDays+predictionDays)
        predicted_values_sarima = forecast_sarima.predicted_mean
 
        data['ds'] = pd.to_datetime(data['ds'])
        last_date = data['ds'].max()
        next_dates = [last_date + timedelta(days=i) for i in range(1, testDays+predictionDays + 1)] 
        forecast_df = pd.DataFrame({
            'ds': next_dates,
            'predicted': predicted_values_sarima
        })
                
        return forecast_df
 
"""     def predict(self,testDays, predictionDays):
        # Implement the prediction logic for ARIMA model
        print("Predicting with ARIMA")
        return None """