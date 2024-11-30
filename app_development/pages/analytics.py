import dash
import os
from dash import html, dcc, callback, Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from utility.visualization import generate_run_plot
from utility.visualization import generate_run_plot, draw_Image, draw_Text, generate_gauge_plot
from dotenv import find_dotenv, load_dotenv
from utility.measurement import find_optimal_window, return_nightimes

# Note will need to pass these in from app
df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/app_development/Data/weather_data.csv")
df1['time'] = pd.to_datetime(df1['time'])

# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
optimal_conditions = {'temperature_2m': float(os.getenv("OPTIMAL_TEMP")),
                      'cloudcover': float(os.getenv("OPTIMAL_CLOUD")),
                      'windspeed_10m': float(os.getenv("OPTIMAL_WIND"))}
forecasted_conditions = {'temperature_2m': df1['temperature_2m'].to_list(),
                         'cloudcover': df1['cloudcover'].to_list(),
                         'windspeed_10m': df1['windspeed_10m'].to_list()}

# Rating weather conditions
max_window = len(df1['temperature_2m'].to_list())
conditions = find_optimal_window(optimal_conditions, forecasted_conditions, max_window)

# Adding forecast to dataframe
df1['Forecast_Score'] = conditions['Score']


dash.register_page(__name__)

current_datetime = pd.Timestamp.now()

layout = html.Div([
    html.H1('Here is your Running Forecast Today'),

    html.Div([
            dbc.Button('Forecast', outline = True, color = 'primary', id='forecast-click',className="me-1", n_clicks=0),
            dbc.Card(
                dbc.CardBody([
                    dbc.Row(id = 'kpi-Row'),   
                ]), color = 'dark'
            )
        ]),
    html.Br(),

   # Generates a graph of the forecast
    html.Div([
        dbc.Row([
            dbc.Col([
                    draw_Image(generate_run_plot(df1, 'Forecast_Score')), 
                ],  
            width={"size": 6, "offset": 0}),
            dbc.Col([
                    dbc.Row([
                        draw_Image(generate_gauge_plot(df1, 'temperature_2m'), 200)
                    ]),
                    dbc.Row([
                        draw_Image(generate_gauge_plot(df1, 'cloudcover'), 200)
                    ]),
                    dbc.Row([
                        draw_Image(generate_gauge_plot(df1, 'windspeed_10m'), 200)
                    ]),

                 ]) 
        ])
            
    ])
])





# callback for kpi row
@callback(
    Output(component_id='kpi-Row', component_property='children'),
    Input('forecast-click', 'n_clicks'),
)
def update_kpi(button1):

    # Copying and filtering dataframe
    filtered_df = df1
    next_12_hours = df1.head(12)
    best_bucket = df1[df1['Forecast_Score'] == df1['Forecast_Score'].max()]
    #start_time = current_datetime + timedelta(hours=9)
    #end_time = current_datetime + timedelta(hours=12)

    start_time = best_bucket['time'].to_list()[0]
    end_time = start_time + timedelta(hours=1)
    return dbc.Row([
                        dbc.Col([
                                draw_Text("Start: " + str(start_time))
                        ], width=4),
                        dbc.Col([
                            draw_Text("End: " + str(end_time))
                        ], width=4),
                    ])