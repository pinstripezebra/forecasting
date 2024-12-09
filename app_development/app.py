# For data manipulation, visualization, app
import dash
from dash import Dash, dcc, html, callback,Input, Output,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
import numpy as np
from dotenv import find_dotenv, load_dotenv
import json
from utility.data_query import data_pipeline
import dash_auth
import flask
from flask_login import LoginManager, UserMixin



# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
LATITUDE, LONGITUDE = float(os.getenv("LATITUDE")), float(os.getenv("LONGITUDE"))
repull_data = True

# authentication
username, password = os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")

# defining path
parent_path = os.path.dirname(os.path.dirname(__file__))

# loading Data
df1 = data_pipeline(repull_data, LATITUDE, LONGITUDE)

# Loading json files containing component styles
SIDEBAR_STYLE , CONTENT_STYLE = {}, {}
with open(parent_path + '/app_development/style/sidebar_style.json') as f:
    SIDEBAR_STYLE = json.load(f)
with open(parent_path + '/app_development/style/content_style.json') as f:
    CONTENT_STYLE = json.load(f)


# defining and Initializing the app
server = flask.Flask(__name__)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets', assets_url_path='/assets/', server = server)
#auth = dash_auth.BasicAuth(app,{username:password})

# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=os.getenv('SECRET_KEY'))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# User data model. It has to have at least self.id as a minimum

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@ login_manager.user_loader
def load_user(username):
    ''' This function loads the user by user id. Typically this looks up the user from a user database.
        We won't be registering or looking up users in this example, since we'll just login using LDAP server.
        So we'll simply return a User object with the passed in username.
    '''
    return User(username)


# Defining components
sidebar = html.Div(children = [
            html.Img(
                        alt="Link to Github",
                        src="./assets/app_logo.png",
                        style={'height':'10%', 'width':'40%', 'margin': 'auto'}
                    ),
            html.H3("Pages"),
            html.Hr(),
            html.Div([ 
                dbc.Nav([
                    dbc.NavLink(f"{page['name']}", href = page["relative_path"]) for page in dash.page_registry.values()
                ], vertical=True)

            ]),
            html.H3("Description"),
            html.P(
                "Your custom running companion allowing you to plan out your perfect time to run ensuring you never miss a workout.", className="text"
            ),
            html.H3("Model"
            ),
            html.P(
                "This project uses machine learning to forecast running conditions and provides a personalized running reccommendation time based on user preferences.", className="text"
            ),

            html.H3("Code"
            ),
            html.P(
                "The complete code for this project is available on github.", className="text"
            ),
            html.A(
                href="https://github.com/pinstripezebra/Dash-Tutorial",
                children=[
                    html.Img(
                        alt="Link to Github",
                        src="./assets/github_logo.png",
                        style={'height':'3%', 'width':'8%'}
                    )
                ],
                style = {'color':'black'}
            )

        ], style=SIDEBAR_STYLE
    )

app.layout = html.Div([sidebar,
    html.Div([
            dash.page_container
    ], style=CONTENT_STYLE)
])

# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
