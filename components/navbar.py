from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output
from app import app

layout = dbc.Row(
        [
            #dbc.Col(
               dbc.Navbar([
                    dbc.Col(
                        html.Div(
                                [   
                                    html.Img(src=app.get_asset_url('sanofi_white.png'), height="40px", alt="Sanofi logo",style={"verticalAlign": "bottom"}),
                                    dbc.NavbarBrand("CSO OPCM Sourcing Table App",style={"fontSize":"x-large"})
                                ],
                                style={"display": "flex", "alignItems": "center"}
                        ),
                        width={"size": 2},
                ),
                    dbc.Col(
                                dbc.Nav(
                                    [
                                        # Add your new pages here
                                        dbc.NavItem(dbc.NavLink("Home",href="/homepage/home/",active=True,id="page-1")),
                                        dbc.NavItem(html.Span(style={"margin": "0 10px"})),
                                        dbc.NavItem(dbc.NavLink("Sourcing Table",href="/sourcing_table/dashboard_current_year",active=True,id="page-2")),
                                        dbc.NavItem(html.Span(style={"margin": "0 10px"})),
                                        dbc.NavItem(dbc.NavLink("Archives",href="/archive",active=True,id="page-3"))             
                                    ],
                                    navbar=True,
                                    pills=True,
                                ),
                                width={"size": 2, "offset":8},    
                            )],
                color="#23004C",
                dark=True,
                ),
            #),
        ],
        #class_name="g-0",
    )

# Callback used to highlight the name of the current page on your navbar.
# If you are adding a new page to the application, please assign it the id "page-X" (with X the number following that of the previous pages) and add 1 to the upper bound of the range.
# Add your condition and remember to add a "False" in the existing conditions   
@app.callback(
        [Output(component_id=f'page-{i}',component_property="active") for i in range (1,4)],
        # the url component is not directly available, that's why it's not reflected in the layout
        # the pathname property of url is used here to only return the filename of the current page
        Input(component_id="url",component_property="pathname")
    )
# The function returns the active property of NavLink item of the Nav component
def toggle_active_page(selected_pathname):
    if selected_pathname in ["/"] or "/homepage" in selected_pathname:
        return True, False,False
    elif "sourcing_table" in selected_pathname:
        return False, True,False
    elif "archive" in selected_pathname:
        return False, False, True
    else:
        return False,False,False