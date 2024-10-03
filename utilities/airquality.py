import requests
import pandas as pd
import datetime

class AirQuality:


    def __init__(self, location):

        self.location = location
        self.raw_data = []
        self.model = None


    def pull_data(self, data_points):

        """Function queries data from openAQ api and returns dataframe

            Input: data_points
                int, contains max datapoints to return from API
            Returns: 
                None, updates internal data structure
        """

        # Defining url for location and requesting data
        converted = []
        
        # Defining dates
        today = str(datetime.date.today())
        year = today[:4]
        month = today[5:7]
        day = today[-2:]
        print(year, month, day)
        if True:
            url = "https://api.openaq.org/v2/measurements?date_from=2024-05-30T00%3A00%3A00Z&date_to={}-{}-{}T20%3A45%3A00Z&limit={}&page=1&offset=0&sort=desc&parameter_id=2&radius=1000&location_id={}&order_by=datetime".format(year, month, day, data_points, self.location)
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            print(response.json)
            converted = response.json()['results']
        #except:
        else:
            print("no return")

        # Defining lists for data parsing
        values, date, location, parameter, latitude, longitude = [], [], [], [], [], []
        
        # Iterating through dict and appending values
        for entry in converted:
            values.append(entry['value'])
            date.append(entry['date']['utc'])
            location.append(entry['locationId'])
            parameter.append(entry['parameter'])
            latitude.append(entry['coordinates']['latitude'])
            longitude.append(entry['coordinates']['longitude'])

        df = pd.DataFrame.from_dict({"Date": date,
                                "Value": values,
                                "location": location,
                                "parameter": parameter,
                                'longitude': longitude,
                                "latitude": latitude})
        df['Date'] =  df['Date'].astype(str)
        
        # Converting datetime
        df['Data_Converted'] = df['Date'].str.slice(start = 0, stop = 10) + " " + df['Date'].str.slice(start = 11)
        df['Data_Converted'] = pd.to_datetime(df['Data_Converted'], format='mixed') 
        self.raw_data = df
