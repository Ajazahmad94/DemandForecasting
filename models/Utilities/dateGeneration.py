# myModule/dateGeneration.py

import pandas as pd
from hijri_converter import convert
from datetime import date,datetime, timedelta

def generateRamadanDates(start_year, end_year):
    ramadan_dates = []

    for year in range(start_year, end_year + 1):
        # The Umm al-Qura calendar uses Hijri dates for Islamic months
        hijri_year_start = convert.Gregorian(year, 1, 1).to_hijri()
        hijri_year_end = convert.Gregorian(year, 12, 30).to_hijri()

        for day in range(1, 30):  # Assuming Ramadan lasts for 29 or 30 days
            # Find the date of Ramadan in the Hijri calendar
            ramadan_date = convert.Hijri(hijri_year_start.year, 9, day).to_gregorian()

            # Append the date to the list
            ramadan_dates.append(ramadan_date)

    # Create a DataFrame with a column named 'ramadan_dates'
    ramadan_df = pd.DataFrame({'ds': ramadan_dates})
    return ramadan_df


 

def generateWeekends(startDate, endDate, *weekend_days):
    '''
    This function will generate weekends dataframe with ds and holiday columns
    Parameters:
    - startDate: start date of the data of type datetime
    - endDate: end date of the data of type datetime
    - weekend_days: list of weekend days ex: [4] for Friday
    Returns: weekends dataframe with ds and holiday columns
    '''
    weekends = []
    current_date = pd.to_datetime(startDate)
    end_date = pd.to_datetime(endDate)

    while current_date <= end_date:
        if current_date.dayofweek in weekend_days:
            weekends.append(current_date)
        current_date += timedelta(days=1)

    # Create a DataFrame with day names and dates
    weekend_df = {'ds': weekends,
                  'holiday': [day.strftime('%A') for day in weekends]}

    df_weekends = pd.DataFrame(weekend_df)
    return df_weekends





def generateWeekdays(startDate, endDate):
  
    return 1

def generateUncertainEventsDates():
    # Your implementation
    return 1



