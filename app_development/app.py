# For data manipulation, visualization, app
import dash
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
import numpy as np
from dotenv import find_dotenv, load_dotenv
import json

# importing helper functions
from utility.data_query import return_surrounding_weather

# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("ONGITUDE")

# defining input variables
repull_data = False
#latitude = 45.5152
#longitude = -122.6784

# base_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))

# loading Data
df1 = ""
if repull_data: # if we want to repull data
    df1 = return_surrounding_weather(LATITUDE, LONGITUDE)
else: # else load old data
    file_name = 'weather_data.csv'
    total_path = parent_path + '\\Data\\' 
    df1 = pd.read_csv(total_path + file_name)

# Loading json files containing component styles
SIDEBAR_STYLE , CONTENT_STYLE = {}, {}
with open(parent_path + '/app_development/style/sidebar_style.json') as f:
    SIDEBAR_STYLE = json.load(f)
with open(parent_path + '/app_development/style/content_style.json') as f:
    CONTENT_STYLE = json.load(f)


# defining and Initializing the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Defining components
sidebar = html.Div(children = [
            html.H3("Pages"),
            html.Hr(),
            html.Div([ 
                dbc.Nav([
                    dbc.NavLink(f"{page['name']}", href = page["relative_path"]) for page in dash.page_registry.values()
                ], vertical=True)

            ]),
            html.H3("Description"),
            html.P(
                "Your custom running companion allowing you to plan out your perfect time to run ensuring you never miss a workout.", className="text"
            ),
            html.H3("Model"
            ),
            html.P(
                "This project uses machine learning to forecast running conditions and provides a personalized running reccommendation time based on user preferences.", className="text"
            ),

            html.H3("Code"
            ),
            html.P(
                "The complete code for this project is available on github.", className="text"
            ),
            html.A(
                href="https://github.com/pinstripezebra/Dash-Tutorial",
                children=[
                    html.Img(
                        alt="Link to Github",
                        src="./assets/github_logo.png",
                        style={'height':'3%', 'width':'8%'}
                    )
                ],
                style = {'color':'black'}
            )

        ], style=SIDEBAR_STYLE
    )

app.layout = html.Div([sidebar,
    html.Div([
            dash.page_container
    ], style=CONTENT_STYLE)
])


# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
