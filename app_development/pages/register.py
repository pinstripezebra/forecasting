import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import pandas as pd
import dash_bootstrap_components as dbc
from dotenv import find_dotenv, load_dotenv
import os
import json
#from utilities.data_manipulation import insert_user

# registering page
dash.register_page(__name__, path='/register')

# Loading json files containing registration pages style
REGISTER_STYLE = {}
with open('app_development\\style\\register_style.json') as f:
    REGISTER_STYLE = json.load(f)

# Defining page layout
layout = html.Div([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Img(
                        alt="Link to Github",
                        src="./assets/logo.png",
                        style={'height':'3%', 'width':'16%', 'margin': 'auto', "opacity": '0.8','display': 'inline'}
                    ),
                    html.H3('Optirun', style={'display': 'inline' }),
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
                                type='password', id='register-pwd-box2'),
                    html.Br(),
                    html.Br(),
                    dbc.Button(children='Register', n_clicks=0,type='submit', id='Register-button')

                ],style = {'align-items':'center', 'justify-content':'center', })
            ])
        ], className='text-center', style={"width": "25rem", 'background-color': 'rgba(245, 245, 245, 1)', 'opacity': '.8'}),
        width={"offset": 4},
    )
], style=REGISTER_STYLE)

# Callback for registering user
'''
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
'''