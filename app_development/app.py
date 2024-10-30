# For data manipulation, visualization, app
import dash
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
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display":"inline-block",
    "width": "100%"
}



# Runing the app
if __name__ == '__main__':
    app.run_server(debug=False)
