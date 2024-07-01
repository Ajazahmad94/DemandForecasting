#Declare a class Same neuralProphet Same as the HoltWintersModel
import os
import sys

class neuralProphetModel:
    def train_and_forecast(self, data,testDays, predictionDays):
        # # **Neural Prophet Parameters**
        # ### ******Input Parameters from Interface******

        #predictionDays=30
        #Excel file Path
        filePath= '/home/ajaz/DemandForecasting/Data/data.csv'  

        print("Inside Neural Prophet Model Section")
        print(os.getcwd())
        print(sys.executable)

        #os.chdir('/home/ajaz/DemandForecasting/models')
        #sys.path.append('/home/ajaz/DemandForecasting')

        # 
        #NeuralProphet
        #1. **Growth Parameters:**
        detectGrowth=True #bool
        growth='off'  #Literal['off', 'linear', 'discontinuous']

        #2. **Changepoints Parameters:**
        detectChangepoints=True #bool
        changepoints= None #Optional[list]
        n_changepoints =None    #0, #int
        changepoints_range=None     #0.8 #float

        #3. **Seasonality Parameters:**
        #To Control Seasonality
        yearly_seasonality= None  #'auto'ss
        weekly_seasonality= None   #'auto'
        daily_seasonality = None   #'auto'

        seasonality_mode='multiplicative' #['additive', 'multiplicative']
        seasonality_reg= None    #float 0

        #4. **Confidence Interval Parameters:**
        confidence_lv = 0.9
        #quantiles  = None      #[]   #List[float]
        quantiles = [round(((1 - confidence_lv) / 2), 2), round((confidence_lv + (1 - confidence_lv) / 2), 2)]

        #5. **Missing Data Handling:**
        impute_missing= None,     #bool
        impute_linear = None,    #int
        impute_rolling= None,  #int
        drop_missing  = None   #bool

        #6. **Normalization Parameters:**
        normalize=None         #'off'     # Literal['auto', 'soft', 'soft1', 'minmax', 'standardize', 'off']

        #7. **Lags and Forecasts:**
        n_lags=None        #0    # int 0    
        n_forecasts=None   #0 #int 1

        #8. **Autoregression Parameters:**  
        ar_layers=None     #[]    #Optional[list]   
        ar_reg= None       #Optional[float]     
        lagged_reg_layers= None    #[]   #Optional[list]       
        learning_rate= 0.1   #Optional[float]

        #9. **Training Parameters:**
        epochs= None      #Optional[int]
        batch_size= None   #Optional[int]
        loss_func=None     #'Huber'
        optimizer=None     #'AdamW'

        #10. **Global/Local Parameters:**
        season_global_local=None #['global', 'local']
        trend_global_local= None   #str 'global', 'local'

        #11. **Trend Parameters:**
        trend_reg= None  #Optional[float]
        trend_reg_threshold =None  #Optional[Union[bool, float]]
        newer_samples_weight= None  # float
        newer_samples_start =None   #float

        #12. **Additional Configuration:**
        collect_metrics= None      #Union [bool, list, dict]

        global_normalization=None
        global_time_normalization=None
        unknown_data_normalization=None

        accelerator=None  #Optional[str] None
        trainer_config=None # dict {},
        prediction_frequency=None  # Optional[dict]

        #Additional  Seasonality regressors

        #Custom holidays
        country_name= 'SA'   #   'SA' # Country Code  (ISO 3166-2) for holidayss

        yearly_add_seasonality=True
        yearly_season_period=365.25
        yearly_season_fourier_order=2

        quarterly_add_seasonality=False
        quarterly_season_period=None
        quarterly_season_fourier_order=None

        monthly_add_seasonality=False
        monthly_season_period=None
        monthly_season_fourier_order=None

        # Weekend days (0-6, Mon-Sun)
        weekendDays = [4]  # 4 is Friday 

        Weekend_add_seasonality=False
        weekendDaysCount=1
        Weekends_fourier_order=5

        WorkingDays_add_seasonality=False
        workingDaysCount=6
        WorkingDays_fourier_order=5

        ramadan_add_seasonality=False
        ramadan_period=29.33
        ramadan_fourier_order=10


        # #### ******Parameters used in other calc, other than the model******

        # Penalty sensitivity for PELT algorithm: 'High', 'Medium', 'Low' : Used to determine the penalty value for the PELT algo which is used for changepoint detection
        PenaltySensitivity ="High"  

        # Model type for changepoint detection: 'l1' (linear 1), 'l2' (linear 2), 'rbf' (radial basis function)
        pltModelType = "l2"  # "l2", "rbf"

        detectOutliers =False # If True, outliers are detected and removed from the data else outliers are not detected and not removed from the data

        #IQR stands for Interquartile Range, which is a measure of statistical dispersion of data
        #IQR Range for outlier detection (1.5 is default) 3 is too high ,  upper_bound = Q3 + IQRRange * IQR and lower_bound = Q1 - IQRRange * IQR 

        IQRRange=1.5


        # # ****Prophet Algorithm****
        # ### ****Importing Libraries****

        from neuralprophet import NeuralProphet, set_log_level
        import pandas as pd
        import matplotlib.pyplot as plt
        import math
        import ruptures as rpt
        import warnings
        import holidays
        from hijri_converter import convert
        from datetime import date,datetime, timedelta
        from prophet.diagnostics import performance_metrics, cross_validation

        from Utilities.fileIO import loadCsvExcelFile
        from Utilities.dataAnalysis import detectGrowth 
        from Utilities.dataAnalysis import detectChangepoints
        from Utilities.dataAnalysis import detectOutliers
        from Utilities.dateGeneration import generateRamadanDates
        from Utilities.dateGeneration import generateWeekends
        warnings.filterwarnings("ignore")

        # ### ****Importing the dataset****
        # ##### Importing Data using the Function



        #For testing to run using a class Im not using the above method for now.
        
        trainData=data

        #Load Data 
        #data = loadCsvExcelFile(filePath)

        trainData['ds'] = pd.to_datetime(trainData['ds'])
        """ trainData.rename(columns={'ds':'ds','y':'y'},inplace=True) """
        # Get the first and last dates of the filtered data
        startDate = pd.to_datetime( trainData['ds'].iloc[0])
        endDate = pd.to_datetime( trainData['ds'].iloc[-1])
        startYear = startDate.year
        endYear = endDate.year
        trainData.head()


        #Growth Detection
        if detectGrowth:
            growth = detectGrowth(trainData)
            print("Growth Detected : ",growth)
        else:
            print("Manual, Growth Detection is Off")


        #detect Change points
        if detectChangepoints:
            changepoints= detectChangepoints(trainData, pltModelType, PenaltySensitivity)
            print("Sucessfully detected Change points")
            #print("Change points : ",changepoints)
        else:
            print("Manual, Change points Detection is Off")

        #detect Outliers
        if detectOutliers:
            lower_bound, upper_bound = detectOutliers(trainData, IQRRange)
            outliers = trainData[((trainData['y'] < lower_bound) | (trainData['y'] > upper_bound))]
            trainData.loc[outliers.index, 'y'] = trainData['y'].mean()
            print("Sucessfully Removed the Outliers")
        print("Outlier Detection  is disabled")

        #Add Ramadan Seasonality

        if ramadan_add_seasonality:
            ramadan_df = generateRamadanDates(startYear, endYear)
            trainData['is_ramadan'] = trainData['ds'].isin(ramadan_df['ds']).astype(int)
            print("Sucessfully Added Ramadan dates in prophet Training Data")
            print(trainData)
        else:
            print("Ramadan Seasonality is disabled")

        #Variables for Weekend and Working days must be imported from input parameters
        if Weekend_add_seasonality:
            df_weekends = generateWeekends(startDate, endDate, *weekendDays)
            trainData['is_weekend'] = trainData['ds'].isin(df_weekends['ds']).astype(int)  
            print("Sucessfully Added Weekend dates in prophet Training Data")
        else:
            print("Weekend Seasonality is disabled")

        if WorkingDays_add_seasonality:
            trainData['is_weekday'] = (trainData['is_weekend'] == 0).astype(int)
            print("Sucessfully Added Working days in prophet Training Data")
        else:
            print("Working days Seasonality is disabled")

        # # Create a Prophet model with flexible parameters

        neuralprophet_params = {
        'growth':growth,
        'changepoints':changepoints,
        'n_changepoints':n_changepoints,
        'changepoints_range':changepoints_range,

        'yearly_seasonality':yearly_seasonality,
        'weekly_seasonality':weekly_seasonality,
        'daily_seasonality':daily_seasonality,

        'seasonality_mode':seasonality_mode,
        'seasonality_reg':seasonality_reg,

        'quantiles':quantiles,

        'impute_missing':impute_missing,
        'impute_linear':impute_linear,
        'impute_rolling':impute_rolling,
        'drop_missing':drop_missing,
        'normalize':normalize,

        'n_lags':n_lags,
        'n_forecasts':n_forecasts,

        'ar_layers':ar_layers,
        'ar_reg':ar_reg,
        'lagged_reg_layers':lagged_reg_layers,
        'learning_rate':learning_rate,

        'epochs':epochs,
        'batch_size':batch_size,
        'loss_func':loss_func,
        'optimizer':optimizer,

        'season_global_local':season_global_local,

        'trend_reg':trend_reg,
        'trend_reg_threshold':trend_reg_threshold,
        'trend_global_local':trend_global_local,

        'newer_samples_weight':newer_samples_weight,
        'newer_samples_start':newer_samples_start,

        'collect_metrics':collect_metrics,

        'global_normalization':global_normalization,
        'global_time_normalization':global_time_normalization,
        'unknown_data_normalization':unknown_data_normalization,

        'accelerator':accelerator,
        'trainer_config':trainer_config,
        'prediction_frequency':prediction_frequency

        }
        print(neuralprophet_params)
        # Remove parameters with value None
        neuralprophet_params = {key: value for key, value in neuralprophet_params.items() if value is not None}
        print(neuralprophet_params)

        # # **Training Model**

        # #### ****Initialize the Model**** ####
        model = NeuralProphet (**neuralprophet_params)

        # ### ****Custom  Seasonalties****

        #Custom seasonality
        #if the  passed condition is True or Not none then it  execute the below code
        #Check the names of the variables from the variables

        if country_name:
            model.add_country_holidays(country_name=country_name)

        if yearly_add_seasonality:
            model.add_seasonality(name='yearly_season' ,period=yearly_season_period ,fourier_order=yearly_season_fourier_order )

        if quarterly_add_seasonality:
            model.add_seasonality(name='quarterly_season' ,period=quarterly_season_period ,fourier_order=quarterly_season_fourier_order )

        if monthly_add_seasonality:
            model.add_seasonality(name='monthly_season' ,period=monthly_season_period ,fourier_order=monthly_season_fourier_order )

        if Weekend_add_seasonality:
            model.add_seasonality(name='Weekends_season' ,period=weekendDaysCount ,fourier_order=Weekends_fourier_order ,condition_name="is_weekend")

        if WorkingDays_add_seasonality:
            model.add_seasonality(name='WorkingDays_season' ,period=workingDaysCount ,fourier_order=WorkingDays_fourier_order ,condition_name="is_weekday")

        if ramadan_add_seasonality:
            model.add_seasonality(name='ramadan_season' ,period=ramadan_period ,fourier_order=ramadan_fourier_order ,condition_name="is_ramadan")

        # #### ****Fit the model to the data**** ####
        model.fit(trainData)

        # ## Generate future Dataframe Dates
        # Create a new dataframe reaching 365 into the future for our forecast, n_historic_predictions also shows historic data
        df_future = model.make_future_dataframe(trainData, n_historic_predictions=True, periods=testDays+predictionDays)


        # Predict the future
        forecast = model.predict(df_future)

        # Visualize the forecast
        predicted_values_neuralProphet = forecast[['ds','yhat1']].tail(testDays+predictionDays)
        #return predicted_values_neuralProphet to ds and predicted
        predicted_values_neuralProphet.rename(columns={'ds':'ds','yhat1':'predicted'},inplace=True)
        
        #forecast.to_csv('/home/ajaz/DemandForecasting/Data/Output/forecast.csv', index=False)
        #print("Sucessfully Generated the forecast Output for NeuralProphet")
        return predicted_values_neuralProphet  # Returning the predicted values """


"""     def predict(self, testDays, predictionDays):
        # Implement the prediction logic for NeuralProphet model
        print("Predicting with NeuralProphet") """