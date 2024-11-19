
#import plotly.plotly as py
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px


df = pd.read_csv('./Data/test.csv')
def generate_run_plot():

    import plotly.graph_objects as go

    r = df['counts'].tolist()
    theta = np.arange(7.5,368,15)
    width = [15]*24

    ticktexts = [f'$\large{i}$' if i % 6 == 0 else '' for i in np.arange(24)]

    fig = go.Figure(go.Barpolar(
        r=r,
        theta=theta,
        width=width,
        marker_color=df['counts'],
        marker_colorscale='Blues',
        marker_line_color="white",
        marker_line_width=2,
        opacity=0.8
    ))

    fig.update_layout(
        template=None,
        polar=dict(
            hole=0.4,
            bgcolor='rgb(223, 223,223)',
            radialaxis=dict(
                showticklabels=False,
                ticks='',
                linewidth=2,
                linecolor='white',
                showgrid=False,
            ),
            angularaxis=dict(
                tickvals=np.arange(0,360,15),
                ticktext=ticktexts,
                showline=True,
                direction='clockwise',
                period=24,
                linecolor='white',
                gridcolor='white',
                showticklabels=True,
                ticks=''
            )
        )
    )
    return fig

def draw_Image(input_figure):
    '''draw images returns a graph inside a card and div component'''

    return html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=input_figure.update_layout(
                            template='ggplot2',
                        )
                    ) 
                ])
            ),  
        ])

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

def generate_timeseries_plot(df, x:str, y:str, s1: list, s2: list):


    time_fig = px.scatter(df, x = 'time', y = y,
                            title = '{type} Forecast'.format(type = y))
    i = 0
    while i < len(s1)-1:

        # start is todays sunset
        start = s2[i]
        # end is tomorrows sunrise
        end = s1[i+1]
        print(start, end)
        # add shaded region
        time_fig.add_vrect(
            x0=start,
            x1=end,
            fillcolor="black",
            opacity=0.5,
            line_width=1,
        )
        i += 1
    return time_fig