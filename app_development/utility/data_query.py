from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions
from itertools import product
import pandas as pd


def return_surrounding_weather(latitude, longitude, margin = 0.001):
    
    """
    Queries weather data from specified latitude/longitude as well as surrounding data points in a radius
    specified by the margin argument.
    """
    latitudes = [latitude, latitude + margin, latitude - margin]
    longitudes = [longitude, longitude + margin, longitude - margin]

    # all locations to query
    locations = list(product(latitudes, longitudes))
    output_data = []
    for location in locations:

        hourly = HourlyForecast()
        # Extracting latitude and longtitude for call
        lat_val = location[0]
        long_val = location[1]
        # Defining variables we want to return
        hourly = hourly.temperature_2m()
        hourly = hourly.cloudcover()
        hourly = hourly.windspeed_10m()

        # Selecting options
        options = ForecastOptions(latitude = lat_val, 
                                longitude = long_val,
                                forecast_days=3)

        # Pulling Data
        client = OpenMeteo(options, hourly)

        # Download data
        sample = client.get_pandas()
        sample['latitude'] = lat_val
        sample['longitude'] = long_val
        sample['location'] = location
        #sample = sample.reset_index()
        output_data.append(sample)

    combined_weather_data = pd.concat(output_data)
    return combined_weather_data
