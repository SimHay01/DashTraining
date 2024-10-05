"""
This module has several purposes:

- it is the entry point for running the app ;

- serves as the central layout hub for the app:
it defines the overall structure of the user interface, 
often including navigation components and placeholders 
for dynamic content ;

- it handles routing logic, determining which components or pages 
to display based on user interactions (such as URL changes).

Its primary role is to integrate various app components 
into a cohesive and navigable layout, while delegating the actual 
content and callback logic to more specialized modules.
"""
# Connect to main app.py file
from app import app
# import the global layout of the application
# from layout import make_layout
import dash_bootstrap_components as dbc
from dash import dcc, html
from components import navbar, sidebar, content

# app.layout=make_layout()

# Every object defined in the app.layout is accessible in other file of the app without need to explicitly import it
app.layout=dbc.Container( # The Container component can be used to center and horizontally pad your app's content
            [
                dcc.Location(id="url"),
                navbar.layout,
                dcc.Store(id='login-status', storage_type='session'), # stores the authentication status of the user
                dcc.Store(id='archive_date_store', storage_type='session'),
                dcc.Store(id='data_ope_year', storage_type='session'),
                dcc.Store(id='data_ope_next_year', storage_type='session'),
                dcc.Store(id='data_ope_year_two', storage_type='session'),
                dcc.Store(id='data_func_year', storage_type='session'),
                dcc.Store(id='data_func_next_year', storage_type='session'),
                dcc.Store(id='data_func_year_two', storage_type='session'),
                dcc.Store(id='data_archive_simu_ope', storage_type='session'),
                dcc.Store(id='data_archive_simu_func', storage_type='session'),
                dcc.Store(id='data_archive_tops', storage_type='session'),
                dbc.Row(
                    [
                        dbc.Col(sidebar.layout,width=1,style={"backgroundColor": "#F4F2F6",'overflow': 'auto'}),
                        dbc.Col(content.layout,width={"size":11}),
                    ],
                    #class_name="g-0",
                    style={"height":"100vh"},
                ),
            ],
            fluid=True,
        )

    
# server set-up
# debug=True parameter enables the hot-reloading option in your application. 
# This means that when you make a change to your app, it reloads automatically, 
# without you having to restart the server
if __name__ == '__main__':
   app.run_server(debug=True)