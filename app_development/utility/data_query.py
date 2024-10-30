from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions


def query_weather_forecast(longitude, latitude):
    hourly = HourlyForecast()
    daily = DailyForecast()

    options = ForecastOptions(latitude, longitude)

    mgr = OpenMeteo(options, hourly.shortwave_radiation(), daily.shortwave_radiation_sum())

    # Download data
    meteo = mgr.get_pandas()

    print(meteo)
    