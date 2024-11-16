import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import folium
from folium.plugins import HeatMap
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime
import numpy as np
from utility.visualization import generate_run_plot, draw_Image, draw_Text
from utility.measurement import find_optimal_window

dash.register_page(__name__, path='/')



# Note will need to pass these in from app
df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/Data/weather_data.csv")

# Temp line until data pull is live
df1['time'] = df1['time'].astype('datetime64[ns]') + np.timedelta64(12, 'D')

# Defining optimal conditions
optimal_conditions = {'temperature_2m': 20,
        'cloudcover': 5,
        'windspeed_10m': 0}

forecasted_conditions = {'temperature_2m': df1['temperature_2m'].to_list(),
                         'cloudcover': df1['cloudcover'].to_list(),
                         'windspeed_10m': df1['windspeed_10m'].to_list()}

# Rating weather conditions
conditions = find_optimal_window(optimal_conditions, optimal_conditions)

# Adding forecast to dataframe
df1['Forecast_Score'] = conditions['Score']

latitude = 45.5152
longitude = -122.6784
df1 = df1[(df1['latitude'] == latitude) & (df1['longitude'] == longitude)]

# Defining layout
layout = html.Div([
    html.H1('This is our Home page'),

    # Selector to choose what type of forecast to show
    html.Div([
            dbc.Row([
                html.Div(children= [
                html.P('Choose the type of forecast', className = 'text'),
                html.Div([
                    dbc.Button('temp', outline = True, color = 'primary', id='temp-click',className="me-1", n_clicks=0),
                    dbc.Button('wind', outline = True, color = 'primary', id='wind-click',className="me-1", n_clicks=0),
                    dbc.Button('cloud', outline = True, color = 'primary', id='cloud-click',className="me-1", n_clicks=0),
                    html.Div(id='container-forecast-type')
                ])

                ])
            ])
    ]),

    # Selector for choosing forecast window
    html.Div([
            dbc.Row([
                html.Div(children= [
                html.H1('Weather Forecast'),
                html.P('Choose the best time to be out and about', className = 'text'),

                html.Label('Date'),
                html.Div([
                    dbc.Button('7-day-forecast', outline = True, color = 'primary', id='btn-nclicks-1',className="me-1", n_clicks=0),
                    dbc.Button('1-day-forecast', outline = True, color = 'primary', id='btn-nclicks-2',className="me-1", n_clicks=0),
                    html.Div(id='container-button-timestamp')
                ])

                ])
            ])
    ]),


    # Generates a graph of the forecast
    html.Div([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row(id = 'weekly-forecast'), 
                ])
            )
    ])


])

# callback for weekly forecast
@callback(
    Output(component_id='weekly-forecast', component_property='children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('temp-click', 'n_clicks'),
    Input('wind-click', 'n_clicks'),
    Input('cloud-click', 'n_clicks'),
)
def update_timeseries(button1, button2, button3, button4, button5):

    # Filtering for how far back
    filtered_df = df1
    if "btn-nclicks-1" == ctx.triggered_id:
        filtered_df = df1
    elif "btn-nclicks-2" == ctx.triggered_id:
        filtered_df = df1[df1['time'].dt.date <  df1['time'].dt.date.min() + + datetime.timedelta(days=1)]
    else:
        filtered_df = df1

    # Selecting forecast type
    forecast_type = "temperature_2m"
    if 'wind-click'== ctx.triggered_id:
        forecast_type = 'windspeed_10m'
    elif 'cloud-click' == ctx.triggered_id:
        forecast_type = 'cloudcover'


    #Creating figure
    time_fig = px.scatter(filtered_df, x = 'time', y = forecast_type,
                              title = '{type} Forecast'.format(type = forecast_type))

    return dbc.Row([
                dbc.Col([
                    draw_Image(time_fig)
                ], width={"size": 6, "offset": 0}),

            ])
