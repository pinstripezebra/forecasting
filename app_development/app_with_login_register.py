# For data manipulation, visualization, app
import dash
from dash import Dash, dcc, html, callback, dash_table, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
import numpy as np
from dotenv import find_dotenv, load_dotenv
import json
from utility.data_query import data_pipeline, retrieve_users
import dash_auth
import flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
LATITUDE, LONGITUDE = float(os.getenv("LATITUDE")), float(os.getenv("LONGITUDE"))
repull_data = True

# authentication
users = retrieve_users()

# defining path
parent_path = os.path.dirname(os.path.dirname(__file__))

# loading Data
df1 = data_pipeline(repull_data, LATITUDE, LONGITUDE)

# Loading json files containing component styles
SIDEBAR_STYLE , CONTENT_STYLE, LOGIN_STYLE = {}, {}, {}
with open(parent_path + '/app_development/style/sidebar_style.json') as f:
    SIDEBAR_STYLE = json.load(f)
with open(parent_path + '/app_development/style/content_style.json') as f:
    CONTENT_STYLE = json.load(f)
with open(parent_path + '/app_development/style/login_style.json') as f:
    LOGIN_STYLE = json.load(f)


# defining and Initializing the app
server = flask.Flask(__name__)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY], assets_folder='assets', assets_url_path='/assets/', server = server)
#auth = dash_auth.BasicAuth(app,{username:password})
username, password = os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
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

# Login screen
login = html.Div([
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
], style = LOGIN_STYLE)



# Registration using register.py
register = html.Div([
                dash.page_container
        ])

# Failed Login
failed = html.Div([html.Div([html.H2('Log in Failed. Please try again.'),
                             html.Br(),
                             html.Div([login]),
                             dcc.Link('Home', href='/')
                             ])  
                   ])  

# logout
logout = html.Div([html.Div(html.H2('You have been logged out - Please login')),
                   html.Br(),
                   html.Br(),
                   dcc.Link('Login', href='/login')
                   ])  

# logout
error404 = html.Div([html.Div(html.H2('Error 404 - page not found')),
                   html.Br(),
                   dcc.Link('Login', href='/login')
                   ])  


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='page-content'),
])

print([page["relative_path"] for page in dash.page_registry.values()])
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
                    dbc.NavLink(f"{page['name']}", href = page["relative_path"]) for page in dash.page_registry.values() if page["relative_path"] != '/register'
                ], vertical=True)

            ]),
            html.H3("Login"),
            html.Div([
                dcc.Link('Logout', href='/logout'),
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
home_page = html.Div([sidebar,
        html.Div([
                dash.page_container
        ], style=CONTENT_STYLE)
    ])




# Callback function to login the user, or update the screen if the username or password are incorrect
@callback(
    [Output('url_login', 'pathname'), Output('output-state', 'children')], [Input('login-button', 'n_clicks')], [State('uname-box', 'value'), State('pwd-box', 'value')])
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if username in users['username'].to_list() and password == users[users['username']== username]['password'].values:
            user = User(username)
            login_user(user)
            # navigate to landing page if logged in successfully 
            return '/landing', ''
        else:
            return '/login', 'Incorrect username or password'

    return dash.no_update, dash.no_update  # Return a placeholder to indicate no update

# Main router
@callback(Output('page-content', 'children'), 
          Output('redirect', 'pathname'),
              Input('url', 'pathname'))
def display_page(pathname):
    ''' callback to determine layout to return '''
    # We need to determine two things for everytime the user navigates:
    # Can they access this page? If so, we just return the view
    # Otherwise, if they need to be authenticated first, we need to redirect them to the login page
    # So we have two outputs, the first is which view we'll return
    # The second one is a redirection to another page is needed
    # In most cases, we won't need to redirect. Instead of having to return two variables everytime in the if statement
    # We setup the defaults at the beginning, with redirect to dash.no_update; which simply means, just keep the requested url
    view = None
    url = dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if pathname == '/login':
        view = login
    elif pathname == '/success':
        if current_user.is_authenticated:
            view = home_page
        else:
            view = failed
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            view = logout
        else:
            view = login
            url = '/login'
    
    
    # if we're logged in and want to view one of the pages
    elif pathname == '/analytic' or pathname == '/landing' or pathname == '/map':
        if current_user.is_authenticated:
            view = home_page
        else:
            view = 'Redirecting to login...'
            url = '/login'
    
    # if we're not logged in and want to register
    elif not current_user.is_authenticated and pathname == '/register':
        view = register
        #url = '/register'


    #else:
    else:
        view = error404
    return view, url
'''
@callback(Output('user-status-div', 'children'), Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    # callback to display login/logout link in the header 
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
            and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
        return dcc.Link('logout', href='/logout'), current_user.get_id()
    else:
        return dcc.Link('login', href='/login'), 'loggedout'
'''

# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
