# import dash
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output, State
# import dash_bootstrap_components as dbc
# from app import app
# import datetime

# import pandas as pd

# # Connect to your app pages
# from pages.homepage import home
# from pages.sourcing_table import dashboard_current_year, dashboard_functional_current_year, dashboard_next_year, dashboard_next_next_year, simulation,insourcing_tops,dataframe,dashboard_functional_next_year,dashboard_functional_next_next_year,simulation_functional,operational_rate
# from pages.archive import archive,archive_dashboard_current_year,archive_dashboard_next_year,archive_dashboard_year_two,archive_tops,archive_func_current_year,archive_func_next_year,archive_func_year_two,archive_simulation_ope,archive_simulation_func


# Define the global layout of the application
# def make_layout():
    # navbar=dbc.Row(
    #     [
    #         dbc.Col(
    #             dbc.Navbar([
    #                 dbc.Col(
    #                     html.Div(
    #                             [   
    #                                 html.Img(src=app.get_asset_url('sanofi_white.png'), height="40px", alt="Sanofi logo",style={"verticalAlign": "bottom"}),
    #                                 dbc.NavbarBrand("CSO OPCM Sourcing Table App",style={"fontSize":"x-large"})
    #                             ],
    #                             style={"display": "flex", "alignItems": "center"}
    #                     ),
    #                     width={"size": 2},
    #             ),
    #                 dbc.Col(
    #                             dbc.Nav(
    #                                 [
    #                                     # Add your new pages here
    #                                     dbc.NavItem(dbc.NavLink("Home",href="/homepage/home/",id="page-1")),
    #                                     dbc.NavItem(html.Span(style={"margin": "0 10px"})),
    #                                     dbc.NavItem(dbc.NavLink("Sourcing Table",href="/sourcing_table/dashboard_current_year",id="page-2")),
    #                                     dbc.NavItem(html.Span(style={"margin": "0 10px"})),
    #                                     dbc.NavItem(dbc.NavLink("Archives",href="/archive",id="page-3"))             
    #                                 ],
    #                                 navbar=True,
    #                                 pills=True,
    #                             ),
    #                             width={"size": 2, "offset":8},    
    #                         )],
    #             color="#23004C",
    #             dark=True,
    #             ),
    #         ),
    #     ],
    #     #class_name="g-0",
    # )

    # #Content of the sidebar
    # submenu = [
    #     html.Div(
    #         dbc.Row(
    #             id="content_sidebar",
    #             class_name="my-1",
    #         ),
    #         id="submenu",
    #     ),
    # ]

    # # Sidebar on the left of the application
    # sidebar = html.Div(
    #     [
    #         html.Div(id="header_sidebar",style={'display': 'flex', "flexDirection": 'column','justifyContent': 'center'}),
    #         dbc.Nav(submenu, vertical=True, pills=True),
    #     ],
    #     id="sidebar",
    # )

    # page content 
    # content = html.Div(id="page-content")

    # global_layout= dbc.Container(
    #     [
    #         dcc.Location(id="url"),
    #         navbar,
    #         dcc.Store(id='login-status', storage_type='session'),# Stock if the user is authentificated or not
    #         dcc.Store(id='archive_date_store', storage_type='session'),
    #         dcc.Store(id='data_ope_year', storage_type='session'),
    #         dcc.Store(id='data_ope_next_year', storage_type='session'),
    #         dcc.Store(id='data_ope_year_two', storage_type='session'),
    #         dcc.Store(id='data_func_year', storage_type='session'),
    #         dcc.Store(id='data_func_next_year', storage_type='session'),
    #         dcc.Store(id='data_func_year_two', storage_type='session'),
    #         dcc.Store(id='data_archive_simu_ope', storage_type='session'),
    #         dcc.Store(id='data_archive_simu_func', storage_type='session'),
    #         dcc.Store(id='data_archive_tops', storage_type='session'),
    #         dbc.Row(
    #             [
    #                 #dbc.Col(sidebar,width=1,style={"backgroundColor": "#F4F2F6",'overflow': 'auto'}),
    #                 #dbc.Col(content,width={"size":11}),
    #             ],
    #             #class_name="g-0",
    #             style={"height":"100vh"},
    #         ),
    #     ],
    #     fluid=True,
    # )

    # return global_layout

# # Callback to change the name of the sidebar depending on the page.
# # If you are adding a new page to the application, insert a new elif here with your condition, then return the name you wish to allocate to the sidebar
# @app.callback(Output("header_sidebar","children"), [Input("url", "pathname")],Input('login-status', 'data'),Input('archive_date_store', 'data'))
# def render_sidebar_name(pathname,login_status,stored_date):


        
#     if pathname in ["/"] or "/homepage" in pathname:
#         content= [html.H4("Homepage",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
#                 html.Hr()]
#         return content
    
#     elif "sourcing_table" in pathname:
#         if login_status=="authenticated":
#             content= [
#                     html.H3("Sourcing Table",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
#                     dbc.Button('Import data',id='baseline_button',href="/sourcing_table/new_baseline",n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6","paddingTop":"5px"}),
#                     html.P("Data from: ",style={"textAlign":"center","fontStyle":"italic","paddingTop":"10px"}),
#                     html.B(dataframe.getDate(),id="data_date",style={"textAlign":"center","fontStyle":"italic","marginTop":"1px"}),
#                     html.Hr(style={"marginTop":"5px"})]
#             return content
    
#     elif "archive" in pathname:
#         content= [html.H3("Archives",id="name_sidebar",style={"textAlign":"center","color":"#23004C", "paddingTop":"15px"}),
#                   dbc.Button('Select an archive',id='archive_button',href="/archive",n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6","paddingTop":"5px"}),
#                   html.P("Archive selected: ",style={"textAlign":"center","fontStyle":"italic","paddingTop":"10px"}),
#                   html.B(f"{stored_date}",id="selected_archive",style={"textAlign":"center","fontStyle":"italic","marginTop":"1px"}),
#                   html.Hr(style={"marginTop":"1px"})]
#         return content


# # Callback to change the content of the sidebar depending on the page.
# # If you are adding a new page to the application, insert a new elif here with your condition, then return the various tabs of your page with dbc.NavLink
# @app.callback(Output("content_sidebar","children"), [Input("url", "pathname"),Input('login-status', 'data'),Input('archive_date_store', 'data')])
# def render_sidebar_content(pathname,login_status,stored_date):

#     if stored_date:
#         stored_date=datetime.datetime.strptime(stored_date,"%d %B %Y")
#         year=stored_date.year
#         next_year=year+1
#         year_two=next_year+1
#     else:
#         year=""
#         next_year=""
#         year_two=""
        


#     if pathname in ["/"] or "homepage" in pathname:
       
#         return[
#             dbc.NavLink("Home",href="/homepage/home/",active=pathname in ["/", "/homepage/home/"]),
#             ] 

#     elif "sourcing_table" in pathname:
#         if login_status=="authenticated":
#             return [
#                 html.H4('Operational roles',style={'color': 'black','fontSize': '1.1rem'}),
#                 dbc.NavLink(f"Dashboard {dataframe.getYear()}",id="ope_year", href=f"/sourcing_table/dashboard_current_year", active=pathname == f"/sourcing_table/dashboard_current_year"),
#                 dbc.NavLink(f"Dashboard {dataframe.getNextYear()}",id="ope_next_year", href=f"/sourcing_table/dashboard_next_year", active=pathname == f"/sourcing_table/dashboard_next_year"),
#                 dbc.NavLink(f"Dashboard {dataframe.getYearTwo()}",id="ope_year_two", href=f"/sourcing_table/dashboard_next_next_year", active=pathname == f"/sourcing_table/dashboard_next_next_year"),
#                 dbc.NavLink("Simulation", href="/sourcing_table/simulation", active=pathname == "/sourcing_table/simulation"),
#                 html.H4('Functional roles',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
#                 dbc.NavLink(f"Dashboard {dataframe.getYear()}",id="func_year", href=f"/sourcing_table/dashboard_functional_current_year", active=pathname == f"/sourcing_table/dashboard_functional_current_year"),
#                 dbc.NavLink(f"Dashboard {dataframe.getNextYear()}",id="func_next_year", href=f"/sourcing_table/dashboard_functional_next_year", active=pathname == f"/sourcing_table/dashboard_functional_next_year"),
#                 dbc.NavLink(f"Dashboard {dataframe.getYearTwo()}",id="func_year_two", href=f"/sourcing_table/dashboard_functional_next_next_year", active=pathname == f"/sourcing_table/dashboard_functional_next_next_year"),
#                 dbc.NavLink(f"Simulation", href=f"/sourcing_table/simulation_functional", active=pathname == f"/sourcing_table/simulation_functional"),
#                 html.H4('Data export',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
#                 dbc.NavLink("Mass loading TOPs into RDPM", href="/sourcing_table/mass_loading", active=pathname == "/sourcing_table/mass_loading"),
#             ]
        
#     elif "archive" in pathname:
#         return[
#             html.H4('Operational roles',style={'color': 'black','fontSize': '1.1rem'}),
#             dbc.NavLink(f"Dashboard {year}",id="archive_ope_year", href=f"/archive/dashboard_current_year", active=pathname == f"/archive/dashboard_current_year"),
#             dbc.NavLink(f"Dashboard {next_year}",id="archive_ope_next_year", href=f"/archive/dashboard_next_year", active=pathname == f"/archive/dashboard_next_year"),
#             dbc.NavLink(f"Dashboard {year_two}",id="archive_ope_year_two", href=f"/archive/dashboard_next_next_year", active=pathname == f"/archive/dashboard_next_next_year"),
#             dbc.NavLink("Simulation", href="/archive/simulation", active=pathname == "/archive/simulation"),
#             html.H4('Functional roles',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
#             dbc.NavLink(f"Dashboard {year}",id="archive_func_year", href=f"/archive/dashboard_functional_current_year", active=pathname == f"/archive/dashboard_functional_current_year"),
#             dbc.NavLink(f"Dashboard {next_year}",id="archive_func_next_year", href=f"/archive/dashboard_functional_next_year", active=pathname == f"/archive/dashboard_functional_next_year"),
#             dbc.NavLink(f"Dashboard {year_two}",id="archive_func_year_two", href=f"/archive/dashboard_functional_next_next_year", active=pathname == f"/archive/dashboard_functional_next_next_year"),
#             dbc.NavLink(f"Simulation", href=f"/archive/simulation_functional", active=pathname == f"/archive/simulation_functional"),
#             html.H4('TOPs dashboard',style={'color': 'black','fontSize': '1.1rem',"paddingTop":"10px"}),
#             dbc.NavLink("TOPs", href="/archive/mass_loading", active=pathname == "/archive/mass_loading"),
#         ]
    
# # Callback to change the content of the page depending on the page/tab selected.
# # If you are adding a new page to the application, insert a new elif here with your pathname, then return the corresponding layout.
# @app.callback(Output("page-content", "children"), [Input("url", "pathname"),Input('login-status', 'data')],
#               [State('archive_date_store','data'),State("data_ope_year",'data'),State("data_ope_next_year",'data'),State("data_ope_year_two",'data'),
#                State("data_archive_tops",'data'),State("data_archive_simu_ope",'data'),State("data_archive_simu_func",'data'),
#                State("data_func_year",'data'),State("data_func_next_year",'data'),State("data_func_year_two",'data')])
# def render_page_content(pathname,login_status,date,data_ope_year,data_ope_next_year,data_ope_year_two,data_archive_tops,data_archive_simu_ope,data_archive_simu_func,data_func_year,data_func_next_year,data_func_year_two):

#     if date:
#         date=datetime.datetime.strptime(date,"%d %B %Y")
#         year=date.year
#         next_year=year+1
#         year_two=next_year+1
#     else:
#         year=""
#         next_year=""
#         year_two=""


#     # Content from homepage
#     if pathname in ["/","/homepage/home/"]:
#         return home.layout
    
    
#     # Content from the Sourcing Table page
#     # We use functions to retrieve the layout in order to have an automatic update of the data
#     elif pathname == "/sourcing_table/dashboard_current_year":
#         return dashboard_current_year.get_Layout(login_status)
#     elif pathname == "/sourcing_table/dashboard_next_year":
#         return dashboard_next_year.get_Layout()
#     elif pathname == "/sourcing_table/dashboard_next_next_year":
#         return dashboard_next_next_year.get_Layout()
#     elif pathname == "/sourcing_table/simulation":
#         return simulation.get_Layout(simulation.modif)
#     elif pathname == "/sourcing_table/mass_loading":
#         return insourcing_tops.get_Layout()
#     elif pathname=="/sourcing_table/new_baseline":
#         return dataframe.layout
#     elif pathname=="/sourcing_table/operational_rate":
#         return operational_rate.get_Layout()
#     elif pathname == "/sourcing_table/dashboard_functional_current_year":
#         return dashboard_functional_current_year.get_Layout()
#     elif pathname == "/sourcing_table/dashboard_functional_next_year":
#         return dashboard_functional_next_year.get_Layout()
#     elif pathname == "/sourcing_table/dashboard_functional_next_next_year":
#         return dashboard_functional_next_next_year.get_Layout()
#     elif pathname == "/sourcing_table/simulation_functional":
#         return simulation_functional.get_Layout(simulation_functional.modif)
    
 
#     # Content from the Archive page
#     # We use functions to retrieve the layout in order to have an automatic update of the data
#     elif pathname == "/archive":
#         return archive.get_Layout()
#     elif pathname == "/archive/dashboard_current_year":
#         return archive_dashboard_current_year.get_Layout(year,data_ope_year)
#     elif pathname == "/archive/dashboard_next_year":
#         return archive_dashboard_next_year.get_Layout(next_year,data_ope_next_year)
#     elif pathname == "/archive/dashboard_next_next_year":
#         return archive_dashboard_year_two.get_Layout(year_two,data_ope_year_two)
#     elif pathname == "/archive/mass_loading":
#         return archive_tops.get_Layout(year,data_archive_tops)
#     elif pathname == "/archive/dashboard_functional_current_year":
#         return archive_func_current_year.get_Layout(year,data_func_year)
#     elif pathname == "/archive/dashboard_functional_next_year":
#         return archive_func_next_year.get_Layout(next_year,data_func_next_year)
#     elif pathname == "/archive/dashboard_functional_next_next_year":
#         return archive_func_year_two.get_Layout(year_two,data_func_year_two)
#     elif pathname == "/archive/simulation":
#         return archive_simulation_ope.get_Layout(year,next_year,year_two,data_archive_simu_ope)
#     elif pathname == "/archive/simulation_functional":
#         return archive_simulation_func.get_Layout(year,next_year,year_two,data_archive_simu_func)
    
#     # If the user tries to reach a different page, return a 404 error message
#     else:
#         return[
#             html.H1("Error 404: Page not found", className="text-danger", style={"paddingTop":"20px"}),
#             html.Hr(),
#             html.P(f"The requested URL \"{pathname}\" does not exist. Please check that the address entered is correct or that the requested URL exists on the application."),
#         ]


# # Callback used to highlight the name of the current page on your navbar.
# # If you are adding a new page to the application, please assign it the id "page-X" (with X the number following that of the previous pages) and add 1 to the upper bound of the range.
# # Add your condition and remember to add a "False" in the existing conditions   
# @app.callback([Output(f'page-{i}',"active") for i in range (1,4)],[Input("url","pathname")])
# def toggle_active_page(pathname):
#     if pathname in ["/"] or "/homepage" in pathname:
#         return True, False,False
#     elif "sourcing_table" in pathname:
#         return False, True,False
#     elif "archive" in pathname:
#         return False, False, True
#     else:
#         return False,False,False





