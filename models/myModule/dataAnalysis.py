# myModule/dataAnalysis.py

#Explain the detectGrowth function
import pandas as pd
import math
import ruptures as rpt
import matplotlib.pyplot as plt

def detectGrowth(data, threshold=0.5, window_size=7):
    """
    Detects the growth type based on the rolling mean trend of a given dataset.

    Parameters:
    - data: DataFrame, the input data.
    - threshold: float, a threshold to categorize the growth type.
    - window_size: int, the window size for calculating the rolling mean.

    Returns:
    - str, the detected growth type.
    """

    # Make a copy of the data
    growth_df = data.copy()

    # Calculate the rolling mean with a specified window size
    growth_df['rolling_mean'] = growth_df['y'].rolling(window=window_size).mean()

    # Determine growth type based on the rolling mean trend
    mean_diff = growth_df['rolling_mean'].diff().mean()

    # Categorize the growth type
    if abs(mean_diff) < threshold:
        growth = 'flat'
    elif mean_diff != 0:
        growth = 'linear'
    else:
        growth = 'discontinuous'

    # Return the detected growth type
    return growth

#Explain the detectChangepoints function

def detectChangepoints(data, pltModelType, PenaltySensitivity):
    """
    Detects the changepoints in a given dataset.

    Parameters:
    - data: DataFrame, the input data.
    - pltModelType: str, the model type for changepoint detection.
    - PenaltySensitivity: str, the sensitivity level for changepoint detection.

    Returns:
    - DataFrame, the detected changepoints.
    """ 
    def calculate_penalty(data, sensitivity, cal=[6, 3, 1.5]):
        if sensitivity == "Low":
            return cal[0] * math.log(len(data))
        elif sensitivity == "Medium":
            return cal[1] * math.log(len(data))
        elif sensitivity == "High":
            return cal[2] * math.log(len(data))

    peltdata = data['y'].values

    # You can choose between "l1" and "l2" cost functions
    algo = rpt.Pelt(model=pltModelType, min_size=1, jump=1).fit(peltdata)
    penalty= calculate_penalty(peltdata, PenaltySensitivity)
    result = algo.predict(pen=3)

    changepointDates=[]
    for index in result:
        a=data.iloc[index-1]['ds']
        changepointDates.append(a)

    changepointDates=pd.DataFrame(changepointDates, columns=['ds'])
    changepointDates['ds'] = pd.to_datetime(changepointDates['ds'])
    return changepointDates['ds']


#Explain the detectOutliers function
def detectOutliers(data, IQRRange):
    print(data['y'].describe())
    Q1 = data['y'].quantile(0.25)
    Q3 = data['y'].quantile(0.75)
    
    IQR = Q3 - Q1
    lower_bound = Q1 - IQRRange * IQR
    upper_bound = Q3 + IQRRange * IQR

    return lower_bound, upper_bound




#return lower_bound, upper_bound

