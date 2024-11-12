import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc





def draw_Text(input_text):

    return html.Div([
            dbc.Card(
                dbc.CardBody([
                        html.Div([
                            html.H2(input_text),
                        ], style={'textAlign': 'center'}) 
                ])
            ),
        ])

# Note will need to pass these in from app
df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/Data/weather_data.csv")

# Temp line until data pull is live
df1['time'] = df1['time'].astype('datetime64[ns]') + np.timedelta64(12, 'D')


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
    html.Div(id='analytics-output')
])


# callback for kpi row
@callback(
    Output(component_id='kpi-Row', component_property='children'),
    Input('forecast-click', 'n_clicks'),
)
def update_kpi(button1):

    # Copying and filtering dataframe
    filtered_df = df1
    start_time = current_datetime + timedelta(hours=9)
    end_time = current_datetime + timedelta(hours=12)
    return dbc.Row([
                        dbc.Col([
                                draw_Text("Window Start: " + str(start_time))
                        ], width=4),
                        dbc.Col([
                            draw_Text("Window End: " + str(end_time))
                        ], width=4),
                    ])