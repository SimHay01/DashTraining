import pages.archive.archive as archive
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

def get_Layout(year,data):

    if not isinstance(year,int):
        layout=html.Div([
            html.H2(f'TOPs',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.P("There are currently no archives selected. Please select one using the \"Select an archive\" button.")
        ])
           
    else:
        data=pd.read_json(data, orient='split')   
        layout = html.Div(
            [
                html.H2(f'TOPs',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
                html.Hr(),
                dag.AgGrid(
                        id="archive_tops",
                        columnDefs=col_def,
                        defaultColDef=defaultColDef,
                        rowData=data.to_dict("records"),
                        dashGridOptions = {'suppressRowTransform': True,'animateRows' : False},
                        style={'width': '100%', 'height': '700px', 'marginTop': '10px'},
                        getRowStyle=getRowStyle),
            
                ])
    return layout

