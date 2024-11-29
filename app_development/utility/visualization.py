
#import plotly.plotly as py
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

kpi_card_style = {
    'color': 'black', 
    'opacity': '0.8',
    'background':'LightGray'
}

graph_card_style = {
    'color': 'black', 
    'background':'LightGray'
}

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
                    dcc.Graph(figure=input_figure.update_layout(template='ggplot2')
                    ) 
                ])
            , style = graph_card_style),  
        ])

def draw_Text(input_text):

    return html.Div([
            dbc.Card(
                dbc.CardBody([
                        html.Div([
                            html.H2(input_text),
                        ], style={'textAlign': 'center'}) 
                ])
            ,style = kpi_card_style),
        ])

def draw_Text_With_Background(input_text, input_img):

    '''
    return html.Div([
            dbc.Card(
                dbc.CardBody([
                        html.Div([
                            html.H2(input_text),
                        ], style={'textAlign': 'center'}) 
                ])
            ,style = kpi_card_style),
        ])
        '''

    return html.Div([dbc.Card(
    [
        dbc.CardImg(
            src=input_img,
            top=True,
            style={"opacity": 0.3},
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Card title", className="card-title"),
                    html.H2(input_text),
                ],
            ),
        ),
    ],
    style={"width": "18rem"},
)])
def generate_timeseries_plot(df, x:str, y:str, s1: list, s2: list):


    time_fig = px.line(df, x = 'time', y = y,
                            title = '{type} Forecast'.format(type = y), 
                           markers=True)
    i = 0
    # Finding min/max times from forecast series to align with day/night series
    min_time = df['time'].min().tz_localize('UTC')
    max_time = df['time'].max().tz_localize('UTC')
    while i < len(s1)-1:

        # start is todays sunset
        start = s2[i]
        # end is tomorrows sunrise
        end = s1[i]
        print(start, end)

        # If both night start/end are within our forecast series
        if (start > min_time) and (end < max_time):
            # add shaded region
            time_fig.add_vrect(
                x0=start,
                x1=end,
                fillcolor="black",
                opacity=0.5,
                line_width=1
            )
        # If its a left edgecase
        elif (start < min_time) and (end > min_time):
            start = min_time
            time_fig.add_vrect(
                x0=start,
                x1=end,
                fillcolor="black",
                opacity=0.5,
                line_width=1
            )
        
        # If its a right edgecase
        elif ( start < max_time) and (end > max_time):
            end = max_time
            time_fig.add_vrect(
                x0=start,
                x1=end,
                fillcolor="black",
                opacity=0.5,
                line_width=1,
            )
        
        i += 1
    time_fig.update_layout(xaxis=dict(
        range=[min_time, max_time],  # Set the range of the x-axis
        side='bottom'  # Set the position of the x-axis to the bottom
        ))
    return time_fig