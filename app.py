"""
This module contains the core setup of the app
"""

import dash
import dash_bootstrap_components as dbc
import os
# import the global layout of the application
#from layout import make_layout
# from index import global_layout
#from components import content, navbar, sidebar
from dash import dcc

# initialization of the Dash app instance
app= dash.Dash (__name__,suppress_callback_exceptions=True,prevent_initial_callbacks="initial_duplicate",compress=True,meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ],
            external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


# global variables accessible throughout the app
app.title = 'Sourcing Table App'
app._favicon=(os.path.join('assets', 'favicon.ico'))
server=app.server