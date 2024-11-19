import pandas as pd
from random import randint
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta, timezone
from dotenv import find_dotenv, load_dotenv
import os



def makelist(count):
    return [randint(1, 100) for _ in range(count)]

test_optimal = {'temperature_2m': 20,
        'cloudcover': 5,
        'windspeed_10m': 0}

test_forecast = {'temperature_2m':makelist(200),
                 'cloudcover': makelist(200),
                 'windspeed_10m': makelist(200)
}

def measure_running_conditions(optimal_values, forecasted_values):

    '''helper function to measure difference between two lists, one containing
    forecasted conditions and one containing actual conditions'''

    score = sum([abs(float(i) - float(j))**2 for i, j in zip(optimal_values, forecasted_values)])
    return score


def find_optimal_window(optimal_conditions, forecasted_conditions, max_window):

    '''takes forecasts of temperature and returns tuples cotnaining the optimal indices to go on a run
    ranked from best to worst

    INPUT:
        optimal_conditions: dict
            contains (feature: optimal_condition) pair where feature is wind, temp, etc in int form
        forecasted_conditions: dict
            contains (feature: forecast) pair where feature is wind, temp, etc and forecast is a list
        
    RETURNS:
        ranked_windows: list
            list of tupples containing the start/stop time for optimal runs
            ex. [(start1, stop1), (start2, stop2),...,(startn, stopn)]
    
    '''

    ranking_indice, ranking = [],[]
    
    factor_keys = list(optimal_conditions.keys())
    optimal_values = [optimal_conditions[i] for i in factor_keys]
    # Iterating through all indices and evaluating score
    for indice in range(len(forecasted_conditions[factor_keys[0]])):

        # returning forecasted values at current timestep
        forecasted_values = [forecasted_conditions[i][indice] for i in factor_keys]

        # evaulating quality at current indice
        current_score = measure_running_conditions(optimal_values, forecasted_values)
        ranking_indice.append(indice)
        ranking.append(current_score)

    score_df = pd.DataFrame({'Indice': ranking_indice,
                             'Score': ranking})
    return score_df



# Testing function
#score = find_optimal_window(test_optimal, test_forecast, 1000)
#print(score)

def return_nightimes(df):

    """takes input series of dates and returns a series two lists
    one of daytime start and one of nightime start to span series"""

    # loading environmental variables
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    LATITUDE = float(os.getenv("LATITUDE"))
    LONGITUDE = float(os.getenv("LONGITUDE"))

    # sunrise/sunset times
    sun = Sun(LATITUDE, LONGITUDE)
    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    test = df['time'].to_list()[0].to_pydatetime()

    # Determining difference between start of unique_dates and today
    delta = (today_sr - test.replace(tzinfo=timezone.utc)).days

    # unique_dates
    df['time_mod'] = df['time'].dt.date
    unique_dates = df['time_mod'].unique()

    # calculating start and end series
    start_series = [today_sr + timedelta(days = delta + i) for i in range(len(unique_dates))]
    end_series = [today_sr + timedelta(days = delta + i) for i in range(len(unique_dates))]

    return start_series, end_series



# testing
#df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/app_development/Data/weather_data.csv")
#df1['time'] = pd.to_datetime(df1['time'])

#s1, s2 = return_nightimes(df1)
#print(s1)
