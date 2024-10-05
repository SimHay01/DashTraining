from pages.sourcing_table import dataframe
import dash
from app import app
from dash import html
import dash_bootstrap_components as dbc
import utils
import os
import re
import datetime
import pandas as pd
from dash import dcc
from dash.dependencies import Input, Output, State
import traceback

if dataframe.dev_mod:
    archive_path=os.path.join(os.getcwd(), 'data/archive')
elif dataframe.uat_mod:
    archive_path="/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/UAT_TEST/ARCHIVE/"    
else:
    archive_path="/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/ARCHIVE"

# Expression régulière pour trouver les motifs "Month YYYY", "Month DD YYYY", ou "YYYY"    
regex = re.compile(r'(\b\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b|'
                   r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b|'
                   r'\b\d{4}\b)')
     
def find_Archive():
    # Créer un ensemble pour stocker les dates uniques
    global date
    global year
    global next_year
    global year_two
    dates_set = set()
    # Parcourir tous les fichiers dans le répertoire
    for files in os.listdir(archive_path):
        # Vérifier si l'élément est un fichier
        path = os.path.join(archive_path, files)
        if os.path.isfile(path):
            # Trouver toutes les occurrences de la date dans le nom du fichier
            found_date = regex.findall(files)
            # Ajouter les dates trouvées à l'ensemble des dates uniques
            dates_set.update(found_date)


    
    # Fonction pour convertir une chaîne "Month YYYY" en objet datetime
    def convert_to_dateobject(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y").strftime("%Y")
        
        except ValueError:
            try:
                return datetime.datetime.strptime(date_str, "%B %Y").strftime("%B %Y")
            
            except ValueError:
                return datetime.datetime.strptime(date_str, "%d %B %Y").strftime("%d %B %Y")
    
    # Convertir toutes les dates en objets datetime
    dates_datetime = [convert_to_dateobject(date) for date in dates_set]
    
    # Trier les objets datetime de la plus récente à la plus ancienne
    dates_set = sorted(dates_datetime, reverse=True)
       
    global dates_unique
    dates_unique=dates_set
    
    if len(dates_set)==0:
        date="None"
        year=""
        next_year=""
        year_two=""

def getDate():
    global date
    return date

def getYear():
    global year
    return year

def getNextYear():
    global next_year
    return next_year

def getYearTwo():
    global year_two
    return year_two

date="None"    
year=""
next_year=""
year_two=""
dashboard_ope=""
dashboard_func=""
simu_ope=""
simu_func=""
tops=""

find_Archive()  



def get_Layout():
    global dates_unique
    find_Archive()
    if len(dates_unique)==0:
        layout=html.Div([
            html.H2(f'Select an archive',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.P("No archive is currently available. Please proceed to the first baseline to start storing archives")
        ])
    else:
        layout=html.Div([
            html.H2(f'Select an archive',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.P("Please select the archive you wish to view and click on the \"Load\" button below the drop-down bar. When the completion alert message appears, you can now navigate between the various tabs, which have been updated with the data from the selected archive."),
            html.Div([
                dcc.Dropdown(
                id="date_archive",
                options=[{'label': date,'value': date} for date in dates_unique],
                value=dates_unique[0],
                style={'width': '45%',"display": "inline-block", "textAlign": "center"}
            ),
            ],
            style={"display": "flex", "justifyContent": "center","width": "100%","paddingTop":"20px"},    
            ),
            dcc.Loading(
            id="loading-archive",
            type="circle",  # Types include 'graph', 'cube', 'circle', 'dot', etc.
            color="#7A00E6",
            children=[
                html.Div(
                    [
                        dbc.Alert(children=None, color="success", id='alert-loading', is_open=False, className='ms-4',duration=6000),
                        dbc.Button('Load the archive', id='load_archive', n_clicks=0, className="me-2", style={"backgroundColor": "#7A00E6", "borderColor": "#7A00E6"})
                    ],
                    style={"textAlign": "center", "paddingTop": "20px", "width": "17rem", "margin": "0 auto"},
                )
            ]
        ),
            
        ]) 
    return layout

@app.callback(
    [Output('alert-loading', 'children'),Output('alert-loading', 'color'),Output('alert-loading', 'is_open'),Output('selected_archive', 'children'),
     Output('archive_ope_year','children'),Output('archive_ope_next_year','children'),Output('archive_ope_year_two','children'),
     Output('archive_func_year','children'),Output('archive_func_next_year','children'),Output('archive_func_year_two','children'),
     Output('archive_date_store','data'),Output('data_ope_year','data'),Output('data_ope_next_year','data'),Output('data_ope_year_two','data'),
     Output('data_func_year','data'),Output('data_func_next_year','data'),Output('data_func_year_two','data'),
     Output('data_archive_simu_ope','data'),Output('data_archive_simu_func','data'),Output('data_archive_tops','data')],
    Input('load_archive',"n_clicks"),
    [State('date_archive', 'value')],
    prevent_initial_call=True
)
def update_output(n_clicks,value):
    if n_clicks==0:
        return dash.no_update
        
    def parse_date(date_str):
        # Essaie de convertir la date en fonction de différents formats attendus
        formats = ["%B %Y", "%d %B %Y", "%Y"]  # Formats à tester dans l'ordre
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
    date=value 
    date_object=parse_date(value)
    year=date_object.year
    next_year=year+1
    year_two=year+2
    
    dashboard_ope=pd.read_csv(f"{archive_path}/dashboard_ope - {date}.csv",sep=';')
    dashboard_func=pd.read_csv(f"{archive_path}/dashboard_func - {date}.csv",sep=';')
    simu_ope=pd.read_csv(f"{archive_path}/simulation_ope - {date}.csv",sep=';')
    simu_func=pd.read_csv(f"{archive_path}/simulation_func - {date}.csv",sep=';')
    tops=pd.read_csv(f"{archive_path}/CSO_Tops - {date}.csv",sep=';')
    
    
    data_ope_year=dataframe.get_dataframe(dashboard_ope,simu_ope,year,next_year,year_two)
    data_ope_next_year=dataframe.get_dataframe(dashboard_ope,simu_ope,next_year,year,year_two)
    data_ope_year_two=dataframe.get_dataframe(dashboard_ope,simu_ope,year_two,year,next_year)
    data_func_year=dataframe.get_dataframe_functional(dashboard_func,simu_func,year,next_year,year_two)
    data_func_next_year=dataframe.get_dataframe_functional(dashboard_func,simu_func,next_year,year,year_two)
    data_func_year_two=dataframe.get_dataframe_functional(dashboard_func,simu_func,year_two,year,next_year)
    
    data_ope_year=data_ope_year.to_json(date_format='iso', orient='split')
    data_ope_next_year=data_ope_next_year.to_json(date_format='iso', orient='split')
    data_ope_year_two=data_ope_year_two.to_json(date_format='iso', orient='split')
    data_func_year=data_func_year.to_json(date_format='iso', orient='split')
    data_func_next_year=data_func_next_year.to_json(date_format='iso', orient='split')
    data_func_year_two=data_func_year_two.to_json(date_format='iso', orient='split')
     
    simu_ope=simu_ope.to_json(date_format='iso', orient='split')
    simu_func=simu_func.to_json(date_format='iso', orient='split')
    tops=tops.to_json(date_format='iso', orient='split')
    
    
    return "The archive has been successfully loaded!","success",True, date,f"Dashboard {year}",f"Dashboard {next_year}",f"Dashboard {year_two}",f"Dashboard {year}",f"Dashboard {next_year}",f"Dashboard {year_two}",date,data_ope_year,data_ope_next_year,data_ope_year_two,data_func_year,data_func_next_year,data_func_year_two,simu_ope,simu_func,tops
