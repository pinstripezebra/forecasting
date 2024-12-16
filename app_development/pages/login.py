import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
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
                        html.Button(children='Login', n_clicks=0,
                                    type='submit', id='login-button'),
                        html.Div(children='', id='output-state'),
                        html.Br()]),
                        

                # Registration
                html.Div([html.H2('Dont have an account? Create yours now!', id='h1'),
                        dbc.Button(children='Register', href="/register"),
                        ])
            ])
        ], className='text-center', style={"width": "30rem", 'background-color': 'rgba(245, 245, 245, 1)', 'opacity': '.8'}),
        width={"offset": 4},
    )
], style=LOGIN_STYLE)