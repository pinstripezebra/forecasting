import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx
import pandas as pd
import dash_bootstrap_components as dbc
from dotenv import find_dotenv, load_dotenv
import os


dash.register_page(__name__, path='/register')


layout = html.Div([
    html.H1('Account Creation')])