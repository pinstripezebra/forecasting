import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import pandas as pd
import dash_bootstrap_components as dbc
from dotenv import find_dotenv, load_dotenv
import os


dash.register_page(__name__, path='/register')


layout = html.Div([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H1('Account Creation'),
                html.H5('Username'),
                dcc.Input(placeholder='Enter your username',
                                        type='text', id='register-uname-box'),
                html.H5('Email'),
                dcc.Input(placeholder='Enter your email',
                                        type='text', id='register-email-box'),
                html.H5('Password'),
                dcc.Input(placeholder='Enter your password',
                            type='password', id='register-pwd-box'),
                html.H5('Confirm Password'),
                dcc.Input(placeholder='Confirm your password',
                            type='password', id='register-pwd-box2')
            ])
        ], style={"width": "25rem",'align': 'center'}),
        width={"offset": 4},
    )
])