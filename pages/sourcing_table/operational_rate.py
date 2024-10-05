import pages.sourcing_table.dataframe as dataframe
import dash_ag_grid as dag #Must use version 2.4.0
from dash import html,dcc
from app import app
import utils
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate
import pandas as pd
import os

service_name=utils.service_name
service_code=utils.service_code
role=utils.role
region=utils.region





col_def=[
            {
                "headerName":service_code,
                "field": service_code,  
                "filter":True,                
                "width":105,
            },
            {
                "headerName":service_name,
                "field": service_name,  
                "filter":True,                
                "width":105,
            },
            {
                "headerName":role,
                "field": role,  
                "filter":True,                
                "width":105,
            },
            {
                "headerName":region,
                "field": region,  
                "filter":True,                
                "width":105,
            },
            {
               "headerName": "% Contractor operational rate",
                "field": "% Direct_110A",  
                "filter":True,   
                "editable":True,  
                "cellEditor": {"function": "DirectInput"},             
                "width":200, 
                "cellStyle": {'borderLeft': '3px solid lightgrey'}
            },
            {
               "headerName": "Source",
                "field": "Source_110A",
                "filter":True,  
                "valueGetter": {"function" : f"valueGetterDirect110A(params)"},            
                "width":100, 
            },
             {
               "headerName": "% Interim operational rate",
                "field": "% Direct_AD10",  
                "filter":True, 
                "editable":True,     
                "cellEditor": {"function": "DirectInput"},          
                "width":200, 
                "cellStyle": {'borderLeft': '3px solid lightgrey'}
            },
            {
               "headerName": "Source",
                "field": "Source_AD10",  
                "filter":True,   
                "valueGetter": {"function" : f"valueGetterDirectAD10(params)"},              
                "width":100, 
                "cellStyle": {'borderRight': '1px solid lightgrey'}
            },
            {
               "headerName": "Missing",
                "field": "Missing",  
                "hide":True,                
                "width":100, 
            }            
        ]

defaultColDef = {"resizable": True, "filter": False,"wrapHeaderText": True,"suppressMovable": True, "editable": False, "cellStyle": {'borderLeft': '1px solid lightgrey', 'textAlign':'center'},"filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']}}
def getStyle():
    getRowStyle={
        "styleConditions": 
            [
                {
                    "condition": f"params.data.Missing =='True'",
                    "style": {"color":"red"},
                },
                {
                    "condition": f"params.data.Missing ==true",
                    "style": {"color":"red"},
                }
            ]
        }
    return getRowStyle

def get_Layout():
    df=dataframe.initial_rate
    layout=html.Div(
        [   
            html.H2(f'Operational rate',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.Div("You can edit here the contractor and the interim operational rates by double-clicking on it.",style={"paddingTop":"15px"}),
            dag.AgGrid
            (
                id="rate",
                columnDefs=col_def,
                defaultColDef=defaultColDef,
                rowData=df.to_dict("records"),
                dashGridOptions = {'suppressRowTransform': True,'animateRows' : False,'undoRedoCellEditing': True,'undoRedoCellEditingLimit': 20},
                style={'height': '700px', 'marginTop': '10px'},
                getRowStyle=getStyle()
            ),
            html.Div
            (
                [
                    dbc.Alert(children=None,color="success",id='alert_rate',is_open=False,duration=2000,className='ms-4'),
                    dbc.Button('Save',id='save_rate',n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"})                     
                ],
                style={"textAlign":"center","paddingTop":"20px","width":"17rem", "margin":"0 auto"},
            ),
        ]
    )
    return layout

@app.callback(
    Output("rate", "rowData", allow_duplicate=True),
    Input("rate", "cellValueChanged"),
    prevent_initial_call=True)
def user(cellValueChanged):
    # Extract the row index and column ID from the changed cell
    row_index = int(cellValueChanged['rowId'])
    col_id = cellValueChanged['colId']
    new_value = cellValueChanged['value']
    dataframe.initial_rate.at[row_index, col_id] = new_value
    if col_id == "% Direct_110A":
        col_id="Source_110A"
    else:
        col_id="Source_AD10"
    value="User"
    # Update the specific cell in the DataFrame to keep the new value even if the user change the current tab
    dataframe.initial_rate.at[row_index, col_id] = value
    return dataframe.initial_rate.to_dict("records")


@app.callback(
            Output("alert_rate", "is_open"),
            Output("alert_rate", "children"),
            Input('save_rate','n_clicks'),
            State('rate','rowData'),
            prevent_initial_call=True)
def update_simulation(n_clicks, rowData):
    if n_clicks==0:
        raise PreventUpdate
    else:
        dataframe.initial_rate=pd.DataFrame(rowData)
        dataframe.initial_rate.to_csv(os.path.join(dataframe.base_path, "operational_rate.csv"),index=False,sep=';')
        dataframe.tops_export=dataframe.prepare_Tops(dataframe.simu_ope,dataframe.simu_func,dataframe.initial_rate) 
       
        return True, "Data successfully saved !"