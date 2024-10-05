from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output
from app import app
from pages.sourcing_table import dataframe
import datetime

# # Content of the sidebar
# submenu_sidebar = html.Div(
#             dbc.Row(id="content_sidebar",class_name="my-1"),
#             id="submenu",
#         ),

# Sidebar on the left of the application
layout = html.Div(
        [
            # Customize the header part of the side bar
            html.Div(id="header_sidebar",style={'display': 'flex', "flexDirection": 'column','justifyContent': 'center'}),
            
            # Content of the side bar in a Nav component
            dbc.Nav(
                html.Div(
                    dbc.Row(id="content_sidebar",class_name="my-1"),
                ),
                vertical=True, 
                pills=True
            ),
        ],
        id="sidebar",
    )

# Callback to change the name of the sidebar depending on the page.
# If you are adding a new page to the application, insert a new elif here with your condition, 
# then return the name you wish to allocate to the sidebar
@app.callback(
        Output(component_id="header_sidebar",component_property="children"), 
        # the url component is not directly available, that's why it's not reflected in the layout
        Input(component_id="url",component_property="pathname"),
        Input(component_id='login-status',component_property='data'),
        Input(component_id='archive_date_store',component_property='data')
        )

def render_sidebar_name(pathname,login_status,stored_date):
    if pathname in ["/"] or "/homepage" in pathname:
        content= [html.H4("Homepage",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
                html.Hr()]
        return content
    
    elif "sourcing_table" in pathname:
        if login_status=="authenticated":
            content= [
                    html.H3("Sourcing Table",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
                    dbc.Button('Import data',id='baseline_button',href="/sourcing_table/new_baseline",n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6","paddingTop":"5px"}),
                    html.P("Data from: ",style={"textAlign":"center","fontStyle":"italic","paddingTop":"10px"}),
                    html.B(dataframe.getDate(),id="data_date",style={"textAlign":"center","fontStyle":"italic","marginTop":"1px"}),
                    html.Hr(style={"marginTop":"5px"})]
            return content
    
    elif "archive" in pathname:
        content= [html.H3("Archives",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
                  dbc.Button('Select an archive',id='archive_button',href="/archive",n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6","paddingTop":"5px"}),
                  html.P("Archive selected: ",style={"textAlign":"center","fontStyle":"italic","paddingTop":"10px"}),
                  html.B(f"{stored_date}",id="selected_archive",style={"textAlign":"center","fontStyle":"italic","marginTop":"1px"}),
                  html.Hr(style={"marginTop":"1px"})]
        return content
    
# Callback to change the content of the sidebar depending on the page.
# If you are adding a new page to the application, insert a new elif here with your condition, then return the various tabs of your page with dbc.NavLink
@app.callback(Output("content_sidebar","children"), [Input("url", "pathname"),Input('login-status', 'data'),Input('archive_date_store', 'data')])
def render_sidebar_content(pathname,login_status,stored_date):

    if stored_date:
        stored_date=datetime.datetime.strptime(stored_date,"%d %B %Y")
        year=stored_date.year
        next_year=year+1
        year_two=next_year+1
    else:
        year=""
        next_year=""
        year_two=""
        


    if pathname in ["/"] or "homepage" in pathname:
       
        return[
            dbc.NavLink("Home",href="/homepage/home/",active=pathname in ["/", "/homepage/home/"]),
            ] 

    elif "sourcing_table" in pathname:
        if login_status=="authenticated":
            return [
                html.H4('Operational roles',style={'color': 'black','fontSize': '1.1rem'}),
                dbc.NavLink(f"Dashboard {dataframe.getYear()}",id="ope_year", href=f"/sourcing_table/dashboard_current_year", active=pathname == f"/sourcing_table/dashboard_current_year"),
                dbc.NavLink(f"Dashboard {dataframe.getNextYear()}",id="ope_next_year", href=f"/sourcing_table/dashboard_next_year", active=pathname == f"/sourcing_table/dashboard_next_year"),
                dbc.NavLink(f"Dashboard {dataframe.getYearTwo()}",id="ope_year_two", href=f"/sourcing_table/dashboard_next_next_year", active=pathname == f"/sourcing_table/dashboard_next_next_year"),
                dbc.NavLink("Simulation", href="/sourcing_table/simulation", active=pathname == "/sourcing_table/simulation"),
                html.H4('Functional roles',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
                dbc.NavLink(f"Dashboard {dataframe.getYear()}",id="func_year", href=f"/sourcing_table/dashboard_functional_current_year", active=pathname == f"/sourcing_table/dashboard_functional_current_year"),
                dbc.NavLink(f"Dashboard {dataframe.getNextYear()}",id="func_next_year", href=f"/sourcing_table/dashboard_functional_next_year", active=pathname == f"/sourcing_table/dashboard_functional_next_year"),
                dbc.NavLink(f"Dashboard {dataframe.getYearTwo()}",id="func_year_two", href=f"/sourcing_table/dashboard_functional_next_next_year", active=pathname == f"/sourcing_table/dashboard_functional_next_next_year"),
                dbc.NavLink(f"Simulation", href=f"/sourcing_table/simulation_functional", active=pathname == f"/sourcing_table/simulation_functional"),
                html.H4('Data export',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
                dbc.NavLink("Mass loading TOPs into RDPM", href="/sourcing_table/mass_loading", active=pathname == "/sourcing_table/mass_loading"),
            ]
        
    elif "archive" in pathname:
        return[
            html.H4('Operational roles',style={'color': 'black','fontSize': '1.1rem'}),
            dbc.NavLink(f"Dashboard {year}",id="archive_ope_year", href=f"/archive/dashboard_current_year", active=pathname == f"/archive/dashboard_current_year"),
            dbc.NavLink(f"Dashboard {next_year}",id="archive_ope_next_year", href=f"/archive/dashboard_next_year", active=pathname == f"/archive/dashboard_next_year"),
            dbc.NavLink(f"Dashboard {year_two}",id="archive_ope_year_two", href=f"/archive/dashboard_next_next_year", active=pathname == f"/archive/dashboard_next_next_year"),
            dbc.NavLink("Simulation", href="/archive/simulation", active=pathname == "/archive/simulation"),
            html.H4('Functional roles',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
            dbc.NavLink(f"Dashboard {year}",id="archive_func_year", href=f"/archive/dashboard_functional_current_year", active=pathname == f"/archive/dashboard_functional_current_year"),
            dbc.NavLink(f"Dashboard {next_year}",id="archive_func_next_year", href=f"/archive/dashboard_functional_next_year", active=pathname == f"/archive/dashboard_functional_next_year"),
            dbc.NavLink(f"Dashboard {year_two}",id="archive_func_year_two", href=f"/archive/dashboard_functional_next_next_year", active=pathname == f"/archive/dashboard_functional_next_next_year"),
            dbc.NavLink(f"Simulation", href=f"/archive/simulation_functional", active=pathname == f"/archive/simulation_functional"),
            html.H4('TOPs dashboard',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
            dbc.NavLink("TOPs", href="/archive/mass_loading", active=pathname == "/archive/mass_loading"),
        ]