# For data manipulation, visualization, app
import dash
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
import numpy as np

# importing helper functions
from utility.data_query import return_surrounding_weather

# defining input variables
repull_data = False
latitude = 45.5152
longitude = -122.6784

# base_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))

# loading Data
df1 = ""
if repull_data: # if we want to repull data
    df1 = return_surrounding_weather(latitude, longitude)
else: # else load old data
    file_name = 'weather_data.csv'
    total_path = parent_path + '\\Data\\' 
    df1 = pd.read_csv(total_path + file_name)

print(total_path)
# building and Initializing the app
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])


# Runing the app
if __name__ == '__main__':
    app.run_server(debug=False)
