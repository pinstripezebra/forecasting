from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions
from itertools import product
import pandas as pd
import os
import pymysql 
import pyodbc
from dotenv import find_dotenv, load_dotenv



def return_single_point(latitude, longitude, forecast_days = 3):

    """
    returns weather data from a single latitude/longitude coordinate
    """

    hourly = HourlyForecast()
    # Extracting latitude and longtitude for call

    # Defining variables we want to return
    hourly = hourly.temperature_2m()
    hourly = hourly.cloudcover()
    hourly = hourly.windspeed_10m()

    # Selecting options
    options = ForecastOptions(latitude = latitude, 
                                longitude = longitude,
                                forecast_days=forecast_days,
                                timezone="America/Los_Angeles")
                                

    # Pulling Data
    client = OpenMeteo(options, hourly)

    # Download data
    sample = client.get_pandas()
    sample['latitude'] = latitude
    sample['longitude'] = longitude
    sample['location'] = str((latitude, longitude))
    return sample


def return_surrounding_weather(latitude, longitude, margin = 0.01, forecast_days = 3):
    
    """
    returns weather data for a central point + performs a gridsearch for points offset by
    a given margin
    """

    latitudes = [latitude, latitude + margin, latitude - margin]
    longitudes = [longitude, longitude + margin, longitude - margin]

    # all locations to query
    locations = list(product(latitudes, longitudes))
    output_data = []
    for location in locations:
        sample = return_single_point(location[0], location[1], forecast_days)
        output_data.append(sample)

    combined_weather_data = pd.concat(output_data)
    return combined_weather_data

def data_pipeline(repull_data, latitude, longitude):

    """
    Returns dataset for application either by querying the api or loading the latest downloaded dataset
    INPUT:
        repull_data: boolean,
            Whether to repull data or load
        latitude: float,
            latitude to pull data from
        longitude: float,
            longitude to pull data from
    OUTPUT:
        df: dataframe
            contains weather data
    """

    df = ""
    parent_path = str(os.path.dirname(os.path.dirname(__file__)))
    total_path = parent_path + '//app_development//Data//' 
    print(total_path)
    file_name = 'weather_data.csv'

    # repull data and save it
    if repull_data:
        df = return_single_point(latitude, longitude, forecast_days = 3)
        df.to_csv('C://Users//seelc//OneDrive//Desktop//Lucas Desktop Items//Projects//forecasting//app_development//Data//weather_data.csv')

    # if we want to load old data
    else:
        df = pd.read_csv('C://Users//seelc//OneDrive//Desktop//Lucas Desktop Items//Projects//forecasting//app_development//Data//weather_data.csv')
    return df

def query_database(server,db, query):

    '''returns user login information for authentication purposes'''
    #connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={db};UID={username};PWD={password}'
    #conn = pyodbc.connect(connectionString) 
    print(server)
    print(db)
    conn = pyodbc.connect('Driver={SQL Server};\
                         Server=' + server + ';\
                         Database=' + db + ';\
                         Trusted_Connection=yes')

    #connection = conn.cursor() 
    df = pd.read_sql(query, conn) 

    return df

query = 'app_development\queries\retrieve_users.txt'

def read_file_into_string(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Example usage
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
filename = 'app_development\\queries\\retrieve_users.txt'
query = read_file_into_string(filename)

server = os.getenv("SERVER")
db_name = os.getenv("DB_NAME")
# querying database
test = query_database(server, db_name, query)
print(test)