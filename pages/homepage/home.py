from dash import html,dcc
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

layout=html.Div(
    style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '95vh','margin': '0','padding': '0','overflow': 'hidden'},
    children=[
        html.H1(f'CSO OPCM Sourcing Table App',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
        html.Img(src=app.get_asset_url('sanofi.png'),height="100px", alt="Sanofi logo",style={'display': 'block','margin': '20px auto'}),
        html.Hr(),
        html.H2("What is the Sourcing Table App ?"),
        html.P('The Sourcing Table App is a web application designed to visualize the workload and workforce of the CSO platform and to make insourcing adjustments.',style={'fontSize': '20px', 'marginTop': '20px'}),
        html.H2("How to use the Sourcing Table App ?",style={'marginTop': '40px'}),
        html.P("To create a baseline and make adjustments, please go to the “Sourcing Table” page (for security reasons, access to this page is password-restricted to specific persons). If you wish to view and download data from a completed baseline, please go to the “Archives” page. A baseline is considered completed when the TOPs have been inserted into RDPM.",style={'fontSize': '20px', 'marginTop': '20px'}),
        html.P("For a better user experience, you can zoom in/out by holding down the ctrl key and using the scroll wheel. You can also use your browser's zoom in/out functionality.",style={'fontSize': '20px','fontWeight': 'bold'}),
        html.P("For more details on how the Sourcing Table App works and the features it offers, please download and read the user's guide using the button below.",style={'fontSize': '20px'}),
        html.Div(
            [
                dbc.Button('Download the user guide',id='user_guide_button',n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6",'fontSize': '20px'}),
                dcc.Download(id="download_user_guide"),                   
            ],
        style={"textAlign":"center","paddingTop":"20px", "margin":"0 auto"},
        ),
        html.H2("Who do I contact if I have a problem ?",style={'marginTop': '40px'}),
        html.P("In the event of bugs or problems encountered while using the application, please send an e-mail to the following address: Simon.Hay@sanofi.com",style={'fontSize': '20px'}),
        html.P("Please try to be as precise as possible when writing your email. Indicate the expected result from the application, the result obtained and the steps taken to get this result. Do not hesitate to attach screenshots or videos to illustrate your problem.",style={'fontSize': '20px'}),
        html.Footer("Developed by Corentin Lespagnol for the CSO OPCM team - Version 2.0 - 09/09/2024",style={'textAlign': 'center','padding': '10px 0','backgroundColor': '#f1f1f1','marginTop': 'auto', 'color': '#888'})
    ]
)

@app.callback(
        Output(component_id="download_user_guide", component_property="data"), 
        Input(component_id="user_guide_button", component_property="n_clicks"),
        prevent_initial_call=True
    )
def func(n_clicks):
    if n_clicks:
        return dcc.send_file(r"/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/ASSETS/user-guide.pdf")



style={"textAlign":"center","paddingTop":"20px","width":"17rem", "margin":"0 auto"}


