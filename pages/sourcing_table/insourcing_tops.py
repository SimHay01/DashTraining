import pages.sourcing_table.dataframe as dataframe
import dash_ag_grid as dag #Must use version 2.4.0
from dash import html,dcc
from app import app
import utils
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import os
import pandas as pd

service_name=utils.service_name
service_code=utils.service_code
role=utils.role
region=utils.region
info=utils.info

# List of expected columns
list_columns = ['Name', 'Network ID', 'Primary skill', 'Default Operationality', 'Service Finance Code', 'Site',
                'Base Entity', 'Element of', 'Contract type', 'Quantity', '% Direct', '% Contract', '% Allocation',
                'Effective start date', 'Effective end date', 'Simulation?']






col_def=[
            {
                "headerName":"Name",
                "field": "Name",  
                "filter":True,                
                "width":105,
            },
            {
                "headerName":"Network ID",
                "field":"Network ID",  
                "filter":True,
                "width":115,
                
            },
            {
                "headerName":"Primary skill",
                "field":"Primary skill",
                "filter":True,     
                "width":115,
            },
            {
                "headerName":"Default Operationality",
                "field":"Default Operationality", 
                "filter":True,   
                "width":125,
                },
            {
                "headerName":"Service Finance Code",
                "field":"Service Finance Code", 
                "filter":True,   
                "width":135,
            },
            {
                "headerName":"Site",
                "field":"Site",
                "filter":True,    
                "width":115,
            },
            {
                "headerName":"Base Entity",
                "field":"Base Entity", 
                "filter":True,   
                "width":115,
            },
            {
                "headerName":"Element of",
                "field":"Element of",
                "filter":True,    
                "width":115,
            },
            {
                "headerName":"Contract type",
                "field":"Contract type", 
                "filter":True,   
                "width":115,
            },
            {
                "headerName":"Quantity",
                "field":"Quantity", 
                "filter":True,   
                "width":105,
            },
            {
                "headerName":"% Direct",
                "field":"% Direct",   
                "filter":True, 
                "width":105,
            },
            {
                "headerName":"% Contract",
                "field":"% Contract", 
                "filter":True,   
                "width":110,
            },
            {
                "headerName":"% Allocation",
                "field":"% Allocation", 
                "filter":True,   
                "width":115,
            },
            {
                "headerName":"Effective start date",
                "field":"Effective start date",
                "filter":True,    
                "width":115,
            },
            {
                "headerName":"Effective end date",
                "field":"Effective end date",  
                "filter":True,  
                "width":115,
            },
            {
                "headerName":"Simulation?",
                "field":"Simulation?",    
                "width":115,
            },
        ]

defaultColDef = {"resizable": True, "filter": False,"wrapHeaderText": True,"suppressMovable": True, "editable": False, "cellStyle": {'borderLeft': '1px solid lightgrey', 'textAlign':'center'},"filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},}

getRowStyle={
    "styleConditions": 
        [
            {
                "condition": f"params.data['% Direct'] === null",
                "style": {"color":"red"},
            },
            {
                "condition": f"params.data['% Direct'] === undefined",
                "style": {"color":"red"},
            }
        ]
    }

def get_Layout():
    df=dataframe.tops_export
    missing_ope = df['% Direct'].isna().sum()
    if missing_ope>0 or df.empty :
        disabled=True
    else:
        disabled=False

    if missing_ope>0:
        string=f"To proceed with data export, {missing_ope} operational rates are currently missing. Please enter them using the button on the right."
    else:
        string=" "
    
    layout = html.Div(
        [
            html.H2(f'Export TOPs',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.Div([
                html.Div(string,style={'width': '85%', 'display': 'inline-block'}),
                html.Div(dbc.Button('Set operational rate',id='set_rate',n_clicks=0,class_name="me-2", href="/sourcing_table/operational_rate",style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '15%', 'display': 'inline-block'}),
            ],      
            style={"width": "100%","paddingTop":"10px"}),
            dag.AgGrid(
                    id="export",
                    columnDefs=col_def,
                    defaultColDef=defaultColDef,
                    rowData=df.to_dict("records"),
                    dashGridOptions = {'suppressRowTransform': True,'animateRows' : False},
                    style={'width': '100%', 'height': '700px', 'marginTop': '10px'},
                    getRowStyle=getRowStyle),
            html.Div(
                            [
                                dbc.Button('Export',id='export_button',n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"},disabled=disabled ),
                                dcc.Download(id="download_CSO_tops"),                     
                            ],
                        style={"textAlign":"center","paddingTop":"20px","width":"17rem", "margin":"0 auto"},
                        ),
        
            ])
    return layout


@app.callback(
    Output("download_CSO_tops", "data"),
    Input("export_button", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    if dataframe.dev_mod:
        archive_path=os.path.join(os.getcwd(), 'data/archive')
    elif dataframe.uat_mod:
         archive_path="/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/UAT_TEST/ARCHIVE/"
    else:
        archive_path="/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/ARCHIVE/"
        
    dataframe.dashboard_ope.to_csv(os.path.join(archive_path, f"dashboard_ope - {dataframe.date}.csv"),index=False,sep=';')
    dataframe.dashboard_func.to_csv(os.path.join(archive_path, f"dashboard_func - {dataframe.date}.csv"),index=False,sep=';')
    dataframe.simu_ope.to_csv(os.path.join(archive_path, f"simulation_ope - {dataframe.date}.csv"),index=False,sep=';')
    dataframe.simu_func.to_csv(os.path.join(archive_path, f"simulation_func - {dataframe.date}.csv"),index=False,sep=';')
    dataframe.tops_export.to_csv(os.path.join(archive_path, f"CSO_Tops - {dataframe.date}.csv"),sep=';',index=False)
    return dcc.send_data_frame(dataframe.tops_export.to_csv,f"CSO_Tops - {dataframe.date}.csv",sep=';',index=False)