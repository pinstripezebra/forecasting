import sys
sys.path.append("..")

import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import folium
from folium.plugins import HeatMap
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime
import numpy as np
from utility.visualization import generate_run_plot, draw_Image, draw_Text, generate_timeseries_plot, draw_Text_With_Background, draw_table
from utility.measurement import find_optimal_window, return_nightimes, get_current_conditions
from utility.chatbot import query_condition_description
import dash_daq as daq
from suntime import Sun, SunTimeException
from dotenv import find_dotenv, load_dotenv
import os


dash.register_page(__name__, path='/landing')

# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))
api_key = os.getenv("ANTHROPIC_API_KEY")
optimal_conditions = {'temperature_2m': float(os.getenv("OPTIMAL_TEMP")),
                      'cloudcover': float(os.getenv("OPTIMAL_CLOUD")),
                      'windspeed_10m': float(os.getenv("OPTIMAL_WIND"))}


# Note will need to pass these in from app
df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/app_development/Data/weather_data.csv")
df1['time'] = pd.to_datetime(df1['time'])

# calculating nightime windows
timezone_offset = 8
s1, s2 = return_nightimes(df1, timezone_offset)

forecasted_conditions = {'temperature_2m': df1['temperature_2m'].to_list(),
                         'cloudcover': df1['cloudcover'].to_list(),
                         'windspeed_10m': df1['windspeed_10m'].to_list()}

# Rating weather conditions
max_window = len(df1['temperature_2m'].to_list())
conditions = find_optimal_window(optimal_conditions, forecasted_conditions, max_window)

# Adding forecast to dataframe
df1['Forecast_Score'] = conditions['Score']

latitude = 45.5152
longitude = -122.6784
df1 = df1[(df1['latitude'] == latitude) & (df1['longitude'] == longitude)]

# Defining layout
layout = html.Div([
    html.H1('Optirun: ', style={'display': 'inline' }),
    html.H3('Choosing the best time to be out and about.', style={'display': 'inline' }),

    # Adding selector for overall forecast
    html.Div([
        html.Div([

            # Top row with filters + KPIs
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Button('7-day-forecast', color = 'primary', id='forecast-click1',className="btn active", n_clicks=0),
                        dbc.Button('1-day-forecast', color = 'primary', id='forecast-click2',className="me-1", n_clicks=0),
                        ]),
                    html.Div(children= [
                    html.P('Choose the type of forecast', className = 'text'),
                    html.Div([
                        dbc.Button('Forecast_Score', color = 'primary', id='overall-click',className="btn active", n_clicks=0),
                        dbc.Button('temp',  color = 'primary', id='temp-click',className="me-1", n_clicks=0),
                        dbc.Button('wind',  color = 'primary', id='wind-click',className="me-1", n_clicks=0),
                        dbc.Button('cloud',  color = 'primary', id='cloud-click',className="me-1", n_clicks=0)
                    ])

                    ])
                ], style = {"display":"inline-block"}),

                # kpi row
                dbc.Col([
                    html.Div([
                        html.H3('Current Conditions'),
                        # Div for kpis
                        html.Div([], id='kpi-indicators')

                    ])
                ], style = {"display":"inline-block"})
            ])

        ])
    ]),
    # Adding filter for forecast period
    html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div(children= [
                            html.H3('Running Condition Forecast'),
                        ]),
                    ]),
                ]),
    html.Div([
                dbc.Row([ 
                        # Div for forecast
                        dbc.Col([
                            html.Div([], id='test-forecast-out')
                        ]),
                        dbc.Col([
                            html.Div(html.H3('Placeholder'))#[draw_Text(query_condition_description(api_key, 
                                                            #                [df1['temperature_2m'][0],
                                                             #                df1['windspeed_10m'][0],
                                                              #               df1['cloudcover'][0]]))])
                        ])
                    ]) ,

                dbc.Row([
                    dbc.Col([
                        # Div for datatable
                        html.Div([], id = 'table-forecast-out')
                    ])
                ])  
                    
                ])
        ]),
])



# callback for weekly forecast for individual series(temp, wind, etc)
@callback(
    [Output(component_id='test-forecast-out', component_property='children'),
     Output(component_id='table-forecast-out', component_property='children')],
    Input('forecast-click1', 'n_clicks'),
    Input('forecast-click2', 'n_clicks'),
    Input('temp-click', 'n_clicks'),
    Input('wind-click', 'n_clicks'),
    Input('cloud-click', 'n_clicks'),
    Input('overall-click', 'n_clicks')

)
def update_timeseries(button1, button2, button3, button4, button5, button6):

    filtered_df = df1
    # if we're filtering for only 1 day
    if "forecast-click2" == ctx.triggered_id:
        filtered_df = df1[df1['time'].dt.date <  df1['time'].dt.date.min() + + datetime.timedelta(days=1)]
   

    time_fig = ""
    forecast_type = "temperature_2m"
    if 'wind-click'== ctx.triggered_id:
        forecast_type = 'windspeed_10m'
    elif 'cloud-click' == ctx.triggered_id:
        forecast_type = 'cloudcover'
    elif 'overall-click' == ctx.triggered_id:
        forecast_type = 'Forecast_Score'

    # Creating graph figure
    time_fig = generate_timeseries_plot(filtered_df, 'time', forecast_type, s1, s2)

    # Creating table figure
    my_datatable = dash_table.DataTable(data = filtered_df.to_dict('records'), 
                                        columns = [{"name": i, "id": i} for i in filtered_df.columns],
                                        page_size=10,
                                        style_header={
                                            'color': 'white'
                                        },
                                        style_table={'overflowX': 'scroll'})
  
    return [dbc.Col([draw_Image(time_fig)], width={"size": 10, "offset": 0}),
            dbc.Col([draw_table(my_datatable)], width={"size": 10, "offset": 0})]
    
                


# callback for kpi's
@callback(
    Output(component_id='kpi-indicators', component_property='children'),
    Input('forecast-click1', 'n_clicks'),
    Input('forecast-click2', 'n_clicks'),
)

def update_kpi(val1, val2):

    filtered_df = df1
    filtered_df = get_current_conditions(filtered_df)
    temp = filtered_df['temperature_2m']
    wind = filtered_df['windspeed_10m']
    cloud= filtered_df['cloudcover']

    return dbc.Row([
                    dbc.Col([
                        draw_Text_With_Background("Temp: " + str(temp), "./assets/temperature.png")
                    ], width=3),
                    dbc.Col([
                            draw_Text_With_Background("Wind: " + str(wind), "./assets/wind.png")
                    ], width=3),
                    dbc.Col([
                            draw_Text_With_Background("Cloud: " + str(cloud), "./assets/clouds.png")
                    ], width=3),
                ], style = {'margin-left': '0px',
                            "width": "80%",
                            "padding": "0rem 0rem"})


@callback(
    [Output("forecast-click1", "className"), 
     Output("forecast-click2", "className")],
    [Input("forecast-click1", "n_clicks"),
     Input("forecast-click2", "n_clicks") ],
)
def set_active_forecast_window(*args):
    ctx = dash.callback_context

    if not ctx.triggered or not any(args):
       return ["btn active"] + ["btn" for _ in range(1, 2)] 
    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return [
        "btn active" if button_id == "forecast-click1" else "btn",
        "btn active" if button_id == "forecast-click2" else "btn" 
    ]

@callback(
    [Output("overall-click", "className"), 
     Output("temp-click", "className"),
     Output("wind-click", "className"),
     Output("cloud-click", "className")],
    [Input("overall-click", "n_clicks"),
     Input("temp-click", "n_clicks"),
     Input("wind-click", "n_clicks"),
     Input("cloud-click", "n_clicks")] ,
)
def set_active_forecast_type(*args):
    ctx = dash.callback_context
    if not ctx.triggered or not any(args):
       return ["btn"] + ["btn active"] + ["btn" for _ in range(1, 2)] 

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return [
        "btn active" if button_id == "overall-click" else "btn",
        "btn active" if button_id == "temp-click" else "btn", 
        "btn active" if button_id == "wind-click" else "btn",
        "btn active" if button_id == "cloud-click" else "btn"
    ]
