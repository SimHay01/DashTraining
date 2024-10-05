from dash import html, Input, Output, State
from app import app
import datetime

from pages.sourcing_table import dataframe
from pages.homepage import home

from pages.sourcing_table import (
    dashboard_current_year, 
    dashboard_functional_current_year, 
    dashboard_next_year, 
    dashboard_next_next_year, 
    simulation,
    insourcing_tops,
    dataframe,
    dashboard_functional_next_year,
    dashboard_functional_next_next_year,
    simulation_functional,operational_rate
)

from pages.archive import (
    archive,
    archive_dashboard_current_year,
    archive_dashboard_next_year,
    archive_dashboard_year_two,
    archive_tops,
    archive_func_current_year,
    archive_func_next_year,
    archive_func_year_two,
    archive_simulation_ope,
    archive_simulation_func
)

# page content 
layout = html.Div(id="page-content")

# Callback to change the content of the page depending on the page/tab selected.
# If you are adding a new page to the application, insert a new elif here with your pathname, then return the corresponding layout.
@app.callback(Output("page-content", "children"), [Input("url", "pathname"),Input('login-status', 'data')],
              [State('archive_date_store','data'),State("data_ope_year",'data'),State("data_ope_next_year",'data'),State("data_ope_year_two",'data'),
               State("data_archive_tops",'data'),State("data_archive_simu_ope",'data'),State("data_archive_simu_func",'data'),
               State("data_func_year",'data'),State("data_func_next_year",'data'),State("data_func_year_two",'data')])
def render_page_content(pathname,login_status,date,data_ope_year,data_ope_next_year,data_ope_year_two,data_archive_tops,data_archive_simu_ope,data_archive_simu_func,data_func_year,data_func_next_year,data_func_year_two):

    if date:
        date=datetime.datetime.strptime(date,"%d %B %Y")
        year=date.year
        next_year=year+1
        year_two=next_year+1
    else:
        year=""
        next_year=""
        year_two=""


    # Content from homepage
    if pathname in ["/","/homepage/home/"]:
        return home.layout
    
    
    # Content from the Sourcing Table page
    # We use functions to retrieve the layout in order to have an automatic update of the data
    elif pathname == "/sourcing_table/dashboard_current_year":
        return dashboard_current_year.get_Layout(login_status)
    elif pathname == "/sourcing_table/dashboard_next_year":
        return dashboard_next_year.get_Layout()
    elif pathname == "/sourcing_table/dashboard_next_next_year":
        return dashboard_next_next_year.get_Layout()
    elif pathname == "/sourcing_table/simulation":
        return simulation.get_Layout(simulation.modif)
    elif pathname == "/sourcing_table/mass_loading":
        return insourcing_tops.get_Layout()
    elif pathname=="/sourcing_table/new_baseline":
        return dataframe.layout
    elif pathname=="/sourcing_table/operational_rate":
        return operational_rate.get_Layout()
    elif pathname == "/sourcing_table/dashboard_functional_current_year":
        return dashboard_functional_current_year.get_Layout()
    elif pathname == "/sourcing_table/dashboard_functional_next_year":
        return dashboard_functional_next_year.get_Layout()
    elif pathname == "/sourcing_table/dashboard_functional_next_next_year":
        return dashboard_functional_next_next_year.get_Layout()
    elif pathname == "/sourcing_table/simulation_functional":
        return simulation_functional.get_Layout(simulation_functional.modif)
    
 
    # Content from the Archive page
    # We use functions to retrieve the layout in order to have an automatic update of the data
    elif pathname == "/archive":
        return archive.get_Layout()
    elif pathname == "/archive/dashboard_current_year":
        return archive_dashboard_current_year.get_Layout(year,data_ope_year)
    elif pathname == "/archive/dashboard_next_year":
        return archive_dashboard_next_year.get_Layout(next_year,data_ope_next_year)
    elif pathname == "/archive/dashboard_next_next_year":
        return archive_dashboard_year_two.get_Layout(year_two,data_ope_year_two)
    elif pathname == "/archive/mass_loading":
        return archive_tops.get_Layout(year,data_archive_tops)
    elif pathname == "/archive/dashboard_functional_current_year":
        return archive_func_current_year.get_Layout(year,data_func_year)
    elif pathname == "/archive/dashboard_functional_next_year":
        return archive_func_next_year.get_Layout(next_year,data_func_next_year)
    elif pathname == "/archive/dashboard_functional_next_next_year":
        return archive_func_year_two.get_Layout(year_two,data_func_year_two)
    elif pathname == "/archive/simulation":
        return archive_simulation_ope.get_Layout(year,next_year,year_two,data_archive_simu_ope)
    elif pathname == "/archive/simulation_functional":
        return archive_simulation_func.get_Layout(year,next_year,year_two,data_archive_simu_func)
    
    # If the user tries to reach a different page, return a 404 error message
    else:
        return[
            html.H1("Error 404: Page not found", className="text-danger", style={"paddingTop":"20px"}),
            html.Hr(),
            html.P(f"The requested URL \"{pathname}\" does not exist. Please check that the address entered is correct or that the requested URL exists on the application."),
        ]