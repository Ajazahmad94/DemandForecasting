#ARIMAModel

from statsmodels.tsa.statespace.sarimax import SARIMAX  
from statsmodels.tsa.arima_model import ARIMA
 

class ARIMAModel:
    def train_and_forecast(self, data):

        p = 1  # Non-seasonal autoregressive order
        d = 1  # Non-seasonal differencing order
        q = 1  # Non-seasonal moving average order

        P = 1  # Seasonal autoregressive order
        D = 1  # Seasonal differencing order
        Q = 1  # Seasonal moving average order

        s = 12  # Seasonal period
        order = (p, d, q)
        seasonal_order = (P, D, Q, s)       

        model_sarima = SARIMAX(data['GroupQuantity'], order=order, seasonal_order=seasonal_order)

        # Fit the SARIMA model
        trained_sarima = model_sarima.fit()

        # Forecast for the next 30 days
        forecast_sarima = trained_sarima.get_forecast(steps=30)
        predicted_values_sarima = forecast_sarima.predicted_mean

        return predicted_values_sarima  # Returning the predicted values

