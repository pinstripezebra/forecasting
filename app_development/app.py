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

# Defining component styles
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "display":"inline-block"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display":"inline-block",
    "width": "100%"
}


# Defining components
sidebar = html.Div(children = [
            html.H2("Description", className="display-4"),
            html.Hr(),
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

# defining and Initializing the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([sidebar,
    html.Div([

            html.H1('Multi-page app with Dash Pages'),
            html.Div([
                html.Div(
                    dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                ) for page in dash.page_registry.values()
            ]),
            dash.page_container
    ], style=CONTENT_STYLE)
])


# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
