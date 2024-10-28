# For data manipulation, visualization, app
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
import numpy as np

# For modeling
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#base_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))

# loading Data
file_name = 'DailyDelhiClimate.csv'
total_path = parent_path + '\\Data\\' 
df1 = pd.read_csv(total_path + file_name)


# Building and Initializing the app
dash_app = Dash(external_stylesheets=[dbc.themes.SLATE])
app = dash_app.server

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display":"inline-block",
    "width": "100%"
}

# Creating layout
dash_app.layout = html.Div(children = [ ], style = CONTENT_STYLE)

# Runing the app
if __name__ == '__main__':
    dash_app.run_server(debug=False)
