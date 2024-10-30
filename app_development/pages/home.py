import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table
import folium
from folium.plugins import HeatMap
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__, path='/')

# Note will need to pass these in from app
df1 = pd.read_csv('C:\Users\seelc\OneDrive\Desktop\Lucas Desktop Items\Projects\forecasting\Data\weather_data.csv')
latitude = 45.5152
longitude = -122.6784
df1 = df1[(df1['latitude'] == latitude) & (df1['longitude'] == longitude)]

# Defining layout
layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('Next Week Forecast'),
    html.Div([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row(id = 'weekly-forecast'), 
                ])
            )
    ]),
    html.Div([
            dbc.Row([
                html.Div(children= [
                html.H1('Heart Failure Prediction'),
                dcc.Markdown('A comprehensive tool for examining factors impacting heart failure'),

                html.Label('Date'),
                dcc.Slider(
                    min = min(df1['time'].drop_duplicates()),
                    max = max(df1['time'].drop_duplicates()),
                    step = 1,
                    value = min(df1['time'].drop_duplicates()),
                    id='date-filter')

                ])
            ])
    ])

])

def draw_Image(input_figure):

    return html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=input_figure.update_layout(
                            template='plotly_dark',
                            plot_bgcolor= 'rgba(0, 0, 0, 0)',
                            paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        )
                    ) 
                ])
            ),  
        ])

# callback for weekly forecast
@callback(
    Output(component_id='weekly-forecast', component_property='children'),
    Input('date-filter', 'value')
)
def update_timeseries(date):

    #Making copy of DF and filtering
    filtered_df = df1
    filtered_df = filtered_df[filtered_df['time']> date]

    #Creating figure
    time_fig = px.scatter(filtered_df, x = 'time', y = 'temperature_2m',
                              title = 'Temperature Forecast')

    return dbc.Row([
                dbc.Col([
                    draw_Image(time_fig)
                ], width={"size": 6, "offset": 0}),

            ])
