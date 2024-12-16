import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx, State
import pandas as pd
import dash_bootstrap_components as dbc
from dotenv import find_dotenv, load_dotenv
import os
import json

# registering page
dash.register_page(__name__, path='/login')

# Loading json files containing registration pages style
LOGIN_STYLE = {}
with open('app_development\\style\\login_style.json') as f:
    LOGIN_STYLE = json.load(f)


# Login screen
layout = html.Div([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                # Login
                html.Div([dcc.Location(id='url_login', refresh=True),
                        html.H2('''Please log in to continue:''', id='h1'),
                        dcc.Input(placeholder='Enter your username',
                                    type='text', id='uname-box'),
                        html.Br(),
                        dcc.Input(placeholder='Enter your password',
                                    type='password', id='pwd-box'),
                        html.Br(),
                        dbc.Button(children='Login', n_clicks=0,type='submit', id='login-button'),
                        html.Div(children='', id='output-state'),
                        html.Br()]),
                        

                # Registration
                html.Div([html.H2('Dont have an account? Create yours now!', id='h1'),
                        dbc.Button(children='Register', href="/register"),
                        ])
            ])
        ], className='text-center', style={"width": "30rem", 'background-color': 'rgba(245, 245, 245, 1)', 'opacity': '.8'}),
        width={"offset": 4},
    ),

    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div(
                    [
                        dbc.Button(
                            "What is Runcast?",
                            id="collapse-button1",
                            className="mb-3",
                            color="primary",
                            n_clicks=0,
                        ),
                        dbc.Collapse(
                            dbc.Card(dbc.CardBody("""Runcast forecasts running conditions over the next next 24 hours to 1 week, utilizing user preferences
                                                  and open source weather forecasts to help you identify the best running windows.""")),
                            id="collapse1",
                            is_open=False,
                        ),
                        html.Br(),
                        dbc.Button(
                            "What Data is Used?",
                            id="collapse-button2",
                            className="mb-3",
                            color="primary",
                            n_clicks=0,
                        ),
                        dbc.Collapse(
                            dbc.Card(dbc.CardBody("""Runcast relies on user provided data, location and weather conditions, combined with open source 
                                                  weather forecasts from Open-Meteo to generate cusomizable running forecasts.""")),
                            id="collapse2",
                            is_open=False,
                        ),
                    ]
                )
            ])
        ], className='text-center', style={"width": "30rem", 'background-color': 'rgba(245, 245, 245, 1)', 'opacity': '.8'}),
        width={"offset": 4},
    )
], style=LOGIN_STYLE)

# Callback for first collapse
@callback(
    Output("collapse1", "is_open"),
    [Input("collapse-button1", "n_clicks")],
    [State("collapse1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Callback for second collapse
@callback(
    Output("collapse2", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2", "is_open")],
)
def toggle_collapse1(n, is_open):
    if n:
        return not is_open
    return is_open