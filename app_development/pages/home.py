import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import folium
from folium.plugins import HeatMap
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__, path='/')

# Note will need to pass these in from app
df1 = pd.read_csv("C:/Users/seelc/OneDrive/Desktop/Lucas Desktop Items/Projects/forecasting/Data/weather_data.csv")
df1['time'] = df1['time'].astype('datetime64[ns]')
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
                html.H1('Weather Forecast'),
                dcc.Markdown('Choose the best time to be out and about'),

                html.Label('Date'),
                html.Div([
                    html.Button('7-day-forecast', id='btn-nclicks-1', n_clicks=0),
                    html.Button('1-day-forecast', id='btn-nclicks-2', n_clicks=0),
                    html.Div(id='container-button-timestamp')
                ])

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
    [Input('7-day-forecast', 'n_clicks'),
    Input('1-day-forecast', 'n_clicks')],
)
def update_timeseries(button1, button2):

    print("here")
    #Making copy of DF and filtering
    filtered_df = df1
    if "7-day-forecast" == ctx.triggered_id:
        filtered_df = df1
    elif "1-day-forecast" == ctx.triggered_id:
        filtered_df = filtered_df[filtered_df['time'].dt.date <  filtered_df['time'].dt.date.min() + 1]
    else:
        filtered_df = df1

    print(len(filtered_df))

    #Creating figure
    time_fig = px.scatter(filtered_df, x = 'time', y = 'temperature_2m',
                              title = 'Temperature Forecast')

    return dbc.Row([
                dbc.Col([
                    draw_Image(time_fig)
                ], width={"size": 6, "offset": 0}),

            ])
