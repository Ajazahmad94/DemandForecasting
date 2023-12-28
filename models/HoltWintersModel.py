#HoltWintersModel

from statsmodels.tsa.holtwinters import ExponentialSmoothing

class HoltWintersModel:
    def train_and_forecast(self, data):

        # Fit the Exponential Smoothing model
        model_hw = ExponentialSmoothing(data['GroupQuantity'], seasonal='add', seasonal_periods=12)
        trained_hw = model_hw.fit()

        # Forecast for the next 30 days
        predicted_values_hw = trained_hw.forecast(steps=30)

        return predicted_values_hw  # Returning the predicted values
