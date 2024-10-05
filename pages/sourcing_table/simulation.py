import pages.sourcing_table.dataframe as dataframe
import dash
from dash import html
from app import app
import dash_ag_grid as dag
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
from dash import dcc
import dash_bootstrap_components as dbc
import utils
import os



service_name=utils.service_name
service_code=utils.service_code
role=utils.role
region=utils.region
info=utils.info


# Generates a unique ID to the simulation_ope page
id=utils.id_factory('simulation_ope')

def field_quarter(year,quarter):
    """
    """
    return f"{year} Q{quarter}"

def getColDefSimu(year,next_year,next_next_year):
    #Transform the year from the format YYYY to the format YY
    year_yy= year % 100
    next_year_yy= next_year % 100
    next_next_year_yy=next_next_year % 100

    #Variable used to name the different columns for the current year
    Q1 = f"1Q {year_yy}"
    Q2 = f"2Q {year_yy}"
    Q3 = f"3Q {year_yy}"
    Q4 = f"4Q {year_yy}"

    #Variable used to name the different columns for the next year
    Q1_next = f"1Q {next_year_yy}"
    Q2_next = f"2Q {next_year_yy}"
    Q3_next = f"3Q {next_year_yy}"
    Q4_next = f"4Q {next_year_yy}"

    #Variable used to name the different columns for the next next year
    Q1_two = f"1Q {next_next_year_yy}"
    Q2_two = f"2Q {next_next_year_yy}"
    Q3_two = f"3Q {next_next_year_yy}"
    Q4_two = f"4Q {next_next_year_yy}"

    # Defintion of the columns used to perform insourcing TOPs adjustments   
    col_def_simu=[
                {
                "headerName": "",
                "children":[
                    {
                        "headerName":service_code,
                        "field": service_code, # field name in the data source that this column will display                 
                        "width":115,
                        "editable": False,
                        "cellClassRules": {"spanned-row": "params.value"}, # Defines CSS class rules for the cells in this column
                        "cellStyle":{"styleConditions":[{"condition": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs'", "style":{"color":"rgba(0,0,0,0)"}}],"defaultStyle": {"color": "black"}},
                        "hide":True,
                    },
                    {
                        "headerName":service_name,
                        "field":service_name,  
                        "width":105,
                        'floatingFilter': False,
                        "filter":True,
                        "filterParams":{"maxNumConditions":1,'buttons': ['reset']},
                        "editable": False,
                        "cellClassRules": {"spanned-row": "params.value"},
                        "cellStyle":{"styleConditions":[{"condition": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs'", "style":{"color":"rgb(0,0,0,0)"}}],"defaultStyle": {"color": "black"}},
                        "hide":True,
                        
                        
                    },
                    {
                        "headerName":role,
                        "field":role,     
                        "width":105,
                        'floatingFilter': False,
                        "filter":True,
                        "filterParams":{"maxNumConditions":1,'buttons': ['reset']},
                        "editable": False,
                        "cellClassRules": {"spanned-row": "params.value"},
                        "hide":True,
                        "cellStyle":{"styleConditions":[{"condition": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs'", "style":{"color":"rgb(0,0,0,0)"}}],"defaultStyle": {"color": "black"}},
                        
                    },
                    {
                        "headerName":region,
                        "field":region,    
                        "width":105,
                        'floatingFilter': False,
                        "filter":True,
                        "filterParams":{"maxNumConditions":1,'buttons': ['reset']},
                        "editable": False,
                        "hide":True,
                        "cellClassRules": {"spanned-row": "params.value"},
                        "cellStyle":{"styleConditions":[{"condition": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs'", "style":{"color":"rgb(0,0,0,0)"}}],"defaultStyle": {"color": "black"}},
                    },
                    {
                        "headerName":"Indicator",
                        "field":info,    
                        "width":415,
                        "editable": False,
                        "cellStyle": {'borderLeft': '3px solid black'}, 
                        'cellRendererSelector': {'function': 'cellRendererSelector(params)'},
                    },
                    
                ]
                },
                {
                    "headerName":f"{str(year)}",

                    "children":
                    [
    
                        {
                            "headerName": Q1,
                            "field": field_quarter(year,1),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},  
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{year},1)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},
                            "cellStyle": {'borderLeft': '3px solid black'}, 
                                
                        },
                        {
                            "headerName": Q2,
                            "field": field_quarter(year,2),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{year},2)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},
                            "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                                                    
                            
                        },
                        {
                            "headerName": Q3,
                            "field": field_quarter(year,3),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{year},3)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"}, 
                            "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                            
                            
                        },
                        {
                            "headerName": Q4,
                            "field": field_quarter(year,4),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{year},4)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},   
                            "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                            
                            
                        },
                    ]
                    },
                    {
                    "headerName":f"{str(next_year)}",

                    "children":
                    [
    
                        {
                            "headerName": Q1_next,
                            "field": field_quarter(next_year,1),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_year},1)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},
                            "cellStyle": {'borderLeft': '3px solid black'},   
                            
                            
                        },
                        {
                            "headerName": Q2_next,
                            "field": field_quarter(next_year,2),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_year},2)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                            
                            
                        },
                        {
                            "headerName": Q3_next,
                            "field": field_quarter(next_year,3),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_year},3)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"}, 
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},  
                            
                            
                        },
                        {
                            "headerName": Q4_next,
                            "field": field_quarter(next_year,4),
                            "width":105,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_year},4)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},   
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},                         
                        },
                    ]
                    },
                                    {
                    "headerName":f"{str(next_next_year)}",

                    "children":
                    [
    
                        {
                            "headerName": Q1_two,
                            "field": field_quarter(next_next_year,1),
                            "width":85,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_next_year},1)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"}, 
                            "cellStyle": {'borderLeft': '3px solid black'},  
                            
                        },
                        {
                            "headerName": Q2_two,
                            "field": field_quarter(next_next_year,2),
                            "width":85,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_next_year},2)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},    
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},
                            
                            
                        },
                        {
                            "headerName": Q3_two,
                            "field": field_quarter(next_next_year,3),
                            "width":85,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_next_year},3)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},   
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},
                            
                            
                        },
                        {
                            "headerName": Q4_two,
                            "field": field_quarter(next_next_year,4),
                            "width":85,
                            "editable": {"function": f"params.data.{info} == '110A TOPs' || params.data.{info} == 'AD10 TOPs' "},
                            "cellEditor": {"function": "NumberInput"},
                            "valueGetter": {"function" : f"valueGetter(params,{next_next_year},4)"},
                            "valueFormatter": {"function" : "valuePercentage(params)"},    
                            "cellStyle": {'borderLeft': '1px solid lightgrey'},                        
                        },
                    ]
                    },
                    {
                        "headerName": f"Avg {str(year_yy)}",
                        "valueGetter": {"function" : f"Math.round(((params.data['{str(year)} Q1']+params.data['{str(year)} Q2']+params.data['{str(year)} Q3']+params.data['{str(year)} Q4'])/4)*10)/10"},
                        "width":95,
                        "valueFormatter": {"function" : "valuePercentage(params)"}, 
                        "cellStyle": {'borderLeft': '3px solid black'},  
                                                                    
                    },
                    {
                        "headerName": f"Avg {str(next_year_yy)}",
                        "valueGetter": {"function" : f"Math.round(((params.data['{str(next_year)} Q1']+params.data['{str(next_year)} Q2']+params.data['{str(next_year)} Q3']+params.data['{str(next_year)} Q4'])/4)*10)/10"},
                        "width":95,
                        "valueFormatter": {"function" : "valuePercentage(params)"},    
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},                                            
                    },
                    {
                        "headerName": f"Avg {str(next_next_year_yy)}",
                        "valueGetter": {"function" : f"Math.round(((params.data['{str(next_next_year)} Q1']+params.data['{str(next_next_year)} Q2']+params.data['{str(next_next_year)} Q3']+params.data['{str(next_next_year)} Q4'])/4)*10)/10"},
                        "width":95,
                        "valueFormatter": {"function" : "valuePercentage(params)"}, 
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},                                               
                    },
                    {
                        "headerName": f"Var {str(year_yy)}/{str(next_year_yy)}",
                        "width":100,
                        "valueFormatter": {"function" : "valuePercentage(params)"},
                        "valueGetter": {"function" : f"Math.round(Math.round(((params.data['{str(next_year)} Q1']+params.data['{str(next_year)} Q2']+params.data['{str(next_year)} Q3']+params.data['{str(next_year)} Q4'])/4)*10)-Math.round(((params.data['{str(year)} Q1']+params.data['{str(year)} Q2']+params.data['{str(year)} Q3']+params.data['{str(year)} Q4'])/4)*10))/10"},
                        "cellStyle": {'borderLeft': '3px solid black'},
                    },
                    {
                        "headerName": f"Var {str(next_year_yy)}/{str(next_next_year_yy)}",
                        "width":100,
                        "valueFormatter": {"function" : "valuePercentage(params)"},
                        "valueGetter": {"function" : f"Math.round(Math.round(((params.data['{str(next_next_year)} Q1']+params.data['{str(next_next_year)} Q2']+params.data['{str(next_next_year)} Q3']+params.data['{str(next_next_year)} Q4'])/4)*10)-Math.round(((params.data['{str(next_year)} Q1']+params.data['{str(next_year)} Q2']+params.data['{str(next_year)} Q3']+params.data['{str(next_year)} Q4'])/4)*10))/10"},
                        "cellStyle": {'borderLeft': '1px solid lightgrey','borderRight': '2px solid black'},
                    },

            ]
    return col_def_simu

# f": This indicates the start of a formatted string in Python.
# params.data.{info}: Within the curly braces {}, the variable info is being inserted into the string. 
# This means that info is a variable whose value will be dynamically included in the string.
getRowStyle = {
    "styleConditions": [
        {
            "condition": f"params.data.{info} ==='In-House Workload - Total FTEs - after PRP & Approved+Not Approved'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white","borderTop":"1px solid black","borderBottom":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='Total In-House Workforce - FTEs'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white","borderTop":"1px solid black","borderBottom":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='In House Coverage %'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white","borderTop":"1px solid black","borderBottom":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='110A TOPs'",
            "style": {"backgroundColor":"rgba(35,0,76,0.25)","color":"black","borderTop":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='AD10 TOPs'",
            "style": {"backgroundColor":"rgba(35,0,76,0.25)","color":"black","borderBottom":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='Total In-House Workforce - FTEs with TOPs'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white","borderTop":"1px solid black","borderBottom":"1px solid black"},
        },
        {
            "condition": f"params.data.{info} ==='In House Coverage % with TOPS'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white","borderTop":"1px solid black","borderBottom":"1px solid black"},
        },
        
    ],
}

defaultColDef_simu = {"resizable": True, "filter": False,"wrapHeaderText": True,"suppressMovable": True, "editable": False}

#===========================================================================================================
#                                               Definition of the layout

# Isolates existing services and links them to the corresponding code. Used in the graphical view dropdown
# We use a function rather than a variable to dynamically update the data
def serviceToCode(df):
    unique_services = df.drop_duplicates(subset=[service_name])
    service_to_code = {row[service_name]: row[service_code] for index, row in unique_services.iterrows()}
    return service_to_code

#Variable used to display or not the alert indicating that data has not been saved
modif=False

def get_Layout(modif):
    year=dataframe.year
    next_year=dataframe.next_year
    next_next_year=dataframe.next_next_year
    col_def_simu=getColDefSimu(year,next_year,next_next_year)
    
    layout=html.Div(
        [
            html.H2('Simulation (operational roles)',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            dcc.Loading(
            id="loading",
            type="circle",  # Types include 'graph', 'cube', 'circle', 'dot', etc.
            color="#7A00E6",
            children=[
                    html.Div(
                        [
                            dbc.Alert(children=None,color="success",id='alerting',is_open=False,duration=2000,className='ms-4'),
                            dbc.Button('Save',id='save_button',n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"})                     
                        ],
                    style={"textAlign":"center","paddingTop":"10px","paddingBottom":"20px","width":"17rem", "margin":"0 auto"},
                    ),
            ]
            ),
            html.Div(
                        [
                            dbc.Alert("Warning : Modified data have not been saved !", color="warning",is_open=modif,id="save_reminder",),                    
                        ],
                    style={"textAlign":"center","paddingTop":"3px","width":"30rem", "margin":"0 auto"},
                    ),
            html.Div([
                html.Div([
                    html.P("Service Name: ",style={'display': 'inline-block','marginRight': '5%'}),  # Ajout du texte avant le premier dropdown
                    dcc.Dropdown(
                        options=[{'label': f"{service} ({serviceToCode(dataframe.getDf(dataframe.simu_ope))[service]})", 'value': service} for service in dataframe.simu_ope[service_name].unique()],
                        value= dataframe.simu_ope[service_name].unique()[0],
                        id='dropdown_service_name',
                        style={'width': '60%','display': 'inline-block','verticalAlign': 'middle'}
                    ),
                ], style={'width': '25%', 'display': 'inline-block'}),
                html.Div([
                    html.P("Role: ",style={'display': 'inline-block','marginRight': '5%'}),  # Ajout du texte avant le deuxième dropdown
                    dcc.Dropdown(
                        options=[{'label': role, 'value': role} for role in dataframe.simu_ope['Role'].unique()],
                        value="ALL",
                        id='dropdown_role',
                        style={'width': '60%','display': 'inline-block','verticalAlign': 'middle'}
                    ),
                ], style={'width': '25%', 'display': 'inline-block'}),
                html.Div([
                    html.P("Region: ",style={'display': 'inline-block','marginRight': '5%'}),  # Ajout du texte avant le troisième dropdown
                    dcc.Dropdown(
                        options=[{'label': region, 'value': region} for region in dataframe.simu_ope['Region'].unique()],
                        value="ALL",
                        id='dropdown_region',
                        style={'width': '60%','display': 'inline-block','verticalAlign': 'middle'}
                    ),
                ], style={'width': '25%', 'display': 'inline-block'}),
            ], style={"width": "100%"}),
            dag.AgGrid(
                id="simulation_ope",
                columnDefs=col_def_simu,
                defaultColDef=defaultColDef_simu,
                rowData=dataframe.simu_ope.round(1).to_dict("records"),
                dashGridOptions = {'suppressRowTransform': True,'animateRows' : False, "singleClickEdit": True,"stopEditingWhenCellsLoseFocus": True },
                getRowStyle = getRowStyle,
                style={'width': '100%', 'height': '775px', 'marginTop': '10px'},
                columnSize="responsiveSizeToFit",
                filterModel={'Service Name':{'filterType' : 'text', 'type': 'contains', 'filter': f'{dataframe.simu_ope[service_name].unique()[0]}'},'Role':{'filterType' : 'text', 'type': 'contains', 'filter': 'ALL'},
                            'Region':{'filterType' : 'text', 'type': 'contains', 'filter': 'ALL'}}
            ),
            
        ],

    )
    return layout

#===========================================================================================================
#                                               Callbacks

@app.callback([Output('dropdown_role','options',allow_duplicate=True),
               Output('dropdown_role','value',allow_duplicate=True)],
              Input('dropdown_service_name','value'),
              prevent_initial_call=True)
def update_dd_role(value):
    """_summary_

    Args:
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    if value is None:
        return dataframe.simu_ope['Role'].unique()
    
    mask=dataframe.simu_ope['Service Name'] == value
    simu_ope=dataframe.simu_ope[mask]
    return simu_ope['Role'].unique(), 'ALL'


@app.callback([Output('dropdown_region','options',allow_duplicate=True),
               Output('dropdown_region','value',allow_duplicate=True)],             
              Input('dropdown_role','value'),
              State('dropdown_service_name','value'),
              prevent_initial_call=True)
def update_dd_region(role,service):
    """
    _summary_

    Args:
        role (_type_): _description_
        service (_type_): _description_

    Returns:
        _type_: _description_
    """

    if role is None:
        return dataframe.simu_ope['Region'].unique()
    
    mask_role = dataframe.simu_ope['Role'] == role
    mask_service = dataframe.simu_ope['Service Name'] == service
    filtered_df = dataframe.simu_ope[mask_role & mask_service]
    if len(filtered_df['Region'].unique()) == 2 and filtered_df['Region'].unique()[0] == " ":
        return filtered_df['Region'].unique()," "
    return filtered_df['Region'].unique(),'ALL'


@app.callback(Output('simulation_ope','filterModel',allow_duplicate=True),
              Input('dropdown_service_name','value'),
              prevent_initial_call=True)
def filter_service(dd_service):
    """_summary_

    Args:
        dd_service (_type_): _description_

    Returns:
        _type_: _description_
    """

    filter_role={"type": "equals", "filter" : ""}
    if dd_service is None:
        filter_name= {"type": "contains", "filter" : ""}
        return {"Service Name" : filter_name, "Role" : filter_role}
    filter_name= {"type": "equals", "filter" : dd_service}
    return {"Service Name" : filter_name, "Role" : filter_role}



@app.callback(Output('simulation_ope','filterModel',allow_duplicate=True),
              Input('dropdown_role','value'),
              State('dropdown_service_name','value'),
              prevent_initial_call=True)
def filter_role(dd_role,value):
    """_summary_

    Args:
        dd_role (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    filter_name={"type": "equals", "filter" : value}
    if dd_role is None:
        filter_role= {"type": "contains", "filter" : ""}
        return {"Role" : filter_role, "Service Name": filter_name}
    
    filter_role= {"type": "equals", "filter" : dd_role}

    return {"Role" : filter_role, "Service Name": filter_name}

@app.callback(Output('simulation_ope','filterModel',allow_duplicate=True),
              Input('dropdown_region','value'),
              State('dropdown_service_name','value'),
              State('dropdown_role','value'),
              prevent_initial_call=True)
def filter_region(dd_region,value_ser,value_rol):
    """_summary_

    Args:
        dd_region (_type_): _description_
        value_ser (_type_): _description_
        value_rol (_type_): _description_

    Returns:
        _type_: _description_
    """
    filter_name={"type": "equals", "filter" : value_ser}
    filter_role={"type": "equals", "filter" : value_rol}
    if dd_region is None:
        filter_region= {"type": "contains", "filter" : ""}
        return {"Role" : filter_role, "Service Name": filter_name, "Region" : filter_region}
    
    filter_region= {"type": "equals", "filter" : dd_region}

    return {"Role" : filter_role, "Service Name": filter_name, "Region": filter_region}


@app.callback(
    Output("save_reminder", "is_open", allow_duplicate=True),
    Input("simulation_ope", "cellValueChanged"),
    prevent_initial_call=True)
def remind_to_save(cellValueChanged):
    # Extract the row index and column ID from the changed cell
    row_index = int(cellValueChanged['rowId'])
    col_id = cellValueChanged['colId']
    new_value = cellValueChanged['value']

    # Update the specific cell in the DataFrame to keep the new value even if the user change the current tab
    dataframe.simu_ope.at[row_index, col_id] = new_value
    global modif
    modif=True
    if modif:
        return True
    else:
        return dash.no_update


@app.callback(
            Output("alerting", "is_open"),
            Output("alerting", "children"),
            Output("save_reminder","is_open", allow_duplicate=True),
            Input('save_button','n_clicks'),
            State('simulation_ope','rowData'),
            prevent_initial_call=True)
def update_simulation(n_clicks, rowData):
    if n_clicks==0:
        raise PreventUpdate
    else:
        dataframe.simu_ope=pd.DataFrame(rowData)
        dataframe.simu_ope.to_csv(os.path.join(dataframe.base_path, f"simulation_ope - {dataframe.date}.csv"),index=False,sep=';')
        dataframe.tops_export=dataframe.prepare_Tops(dataframe.simu_ope,dataframe.simu_func,dataframe.initial_rate) 
        
        global modif
        modif=False
        
        return True, "Data successfully saved !", False
