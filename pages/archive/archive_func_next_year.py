import datetime
import dash_ag_grid as dag #Must use version 2.4.0
import dash
from dash import html, Patch
from app import app
from dash.dependencies import Input, Output, State
import pages.sourcing_table.dataframe as dataframe
import pages.archive.archive as archive
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import utils
import pandas as pd

#=====================================================================================
#                                       Variables

#Imports variables from the “utils” and "dataframe" files for improved maintainability 


service_name=utils.service_name
service_code=utils.service_code
role=utils.role
region=utils.region
info=utils.info

Q1_WL=utils.Q1_WL
Q2_WL=utils.Q2_WL
Q3_WL=utils.Q3_WL
Q4_WL=utils.Q4_WL
H1_WL=utils.H1_WL
H2_WL=utils.H2_WL
AVG_WL=utils.AVG_WL

Q1_HC=utils.Q1_HC
Q2_HC=utils.Q2_HC
Q3_HC=utils.Q3_HC
Q4_HC=utils.Q4_HC
H1_HC=utils.H1_HC
H2_HC=utils.H2_HC
AVG_HC=utils.AVG_HC

Q1_110AC=utils.Q1_110AC
Q2_110AC=utils.Q2_110AC
Q3_110AC=utils.Q3_110AC
Q4_110AC=utils.Q4_110AC
H1_110AC=utils.H1_110AC
H2_110AC=utils.H2_110AC
AVG_110AC=utils.AVG_110AC

Q1_AD10C=utils.Q1_AD10C
Q2_AD10C=utils.Q2_AD10C
Q3_AD10C=utils.Q3_AD10C
Q4_AD10C=utils.Q4_AD10C
H1_AD10C=utils.H1_AD10C
H2_AD10C=utils.H2_AD10C
AVG_AD10C=utils.AVG_AD10C

Q1_TOPS=utils.Q1_TOPS
Q2_TOPS=utils.Q2_TOPS
Q3_TOPS=utils.Q3_TOPS
Q4_TOPS=utils.Q4_TOPS
H1_TOPS=utils.H1_TOPS
H2_TOPS=utils.H2_TOPS
AVG_TOPS=utils.AVG_TOPS

Q1_TOPS_110A=utils.Q1_TOPS_110A
Q2_TOPS_110A=utils.Q2_TOPS_110A
Q3_TOPS_110A=utils.Q3_TOPS_110A
Q4_TOPS_110A=utils.Q4_TOPS_110A
H1_TOPS_110A=utils.H1_TOPS_110A
H2_TOPS_110A=utils.H2_TOPS_110A
AVG_TOPS_110A=utils.AVG_TOPS_110A

Q1_TOPS_AD10=utils.Q1_TOPS_AD10
Q2_TOPS_AD10=utils.Q2_TOPS_AD10
Q3_TOPS_AD10=utils.Q3_TOPS_AD10
Q4_TOPS_AD10=utils.Q4_TOPS_AD10
H1_TOPS_AD10=utils.H1_TOPS_AD10
H2_TOPS_AD10=utils.H2_TOPS_AD10
AVG_TOPS_AD10=utils.AVG_TOPS_AD10

Q1_CONT=utils.Q1_CONT
Q2_CONT=utils.Q2_CONT
Q3_CONT=utils.Q3_CONT
Q4_CONT=utils.Q4_CONT
H1_CONT=utils.H1_CONT
H2_CONT=utils.H2_CONT
AVG_CONT=utils.AVG_CONT

Q1_WF=utils.Q1_WF
Q2_WF=utils.Q2_WF
Q3_WF=utils.Q3_WF
Q4_WF=utils.Q4_WF
H1_WF=utils.H1_WF
H2_WF=utils.H2_WF
AVG_WF=utils.AVG_WF

Q1_COVER=utils.Q1_COVER
Q2_COVER=utils.Q2_COVER
Q3_COVER=utils.Q3_COVER
Q4_COVER=utils.Q4_COVER
H1_COVER=utils.H1_COVER
H2_COVER=utils.H2_COVER
AVG_COVER=utils.AVG_COVER

Q1_GAP=utils.Q1_GAP
Q2_GAP=utils.Q2_GAP
Q3_GAP=utils.Q3_GAP
Q4_GAP=utils.Q4_GAP
H1_GAP=utils.H1_GAP
H2_GAP=utils.H2_GAP
AVG_GAP=utils.AVG_GAP

Q1_FLEX=utils.Q1_FLEX
Q2_FLEX=utils.Q2_FLEX
Q3_FLEX=utils.Q3_FLEX
Q4_FLEX=utils.Q4_FLEX
H1_FLEX=utils.H1_FLEX
H2_FLEX=utils.H2_FLEX
AVG_FLEX=utils.AVG_FLEX

id=utils.id_factory('archive_dashboard_func_next_year')


#=====================================================================================
#                               Definition of the layout

DIV_STYLE = {
    "height": "80vh",
}


def get_Layout(next_year,data):

    if not isinstance(next_year,int):
        layout=html.Div([
            html.H2(f'Dashboard',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
            html.Hr(),
            html.P("There are currently no archives selected. Please select one using the \"Select an archive\" button.")
        ])
    else:
    
        columnDefs,defaultColDef,getRowStyle=dataframe.get_dashboard_functional(next_year)
        data=pd.read_json(data, orient='split')
        layout=html.Div(
            [
                html.H2(f'Dashboard {next_year}',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
                html.Hr(),
                html.Div([
                    html.Div(dbc.Button('Global view',id=id('global_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
                    html.Div(dbc.Button('Corporate view',id=id('corpo_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
                    html.Div(dbc.Button('CSUs view',id=id('csu_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
                    html.Div(dbc.Button('Reset view',id=id('reset_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '50%', 'display': 'inline-block'}),
                ],
                style={"paddingBottom":"15px"}),
                dag.AgGrid(
                    id=id("dashboard-functional-current-year"),
                    columnDefs=columnDefs,
                    rowData=data.to_dict("records"),
                    defaultColDef=defaultColDef,
                    style={"height":"100%", "width":"100%"},
                    persistence=True,persistence_type='session',
                    persisted_props=['filterModel'],
                    dashGridOptions={"rowBuffer": 1,'rowSelection':'multiple',"tooltipShowDelay": 0},
                    getRowStyle=getRowStyle,
                ),
            ],
            style=DIV_STYLE,
        )
    return layout


#===========================================================================================================
#                                       Definition of the callbacks

@app.callback(Output(id('dashboard-functional-current-year'),'filterModel',allow_duplicate=True),
              Input(id('global_button'),'n_clicks'),
              prevent_initial_call=True)
def global_view(n_clicks):
    if n_clicks:
        filter_value= {"type": "equals", "filter" : "ALL"}
        return {role : filter_value}
    return dash.no_update

@app.callback(Output(id('dashboard-functional-current-year'),'filterModel',allow_duplicate=True),
              Input(id('corpo_button'),'n_clicks'),
              prevent_initial_call=True)
def corporate_view(n_clicks):
    if n_clicks:
        filter_value= {"operator": "AND", "conditions": [
             {"type": "notContains", "filter" : "17"},
             {"type": "notContains", "filter" : "Total CSUs"},
             {"type": "notContains", "filter" : "Total CSO"},
             {"type": "notContains", "filter" : "BS"},
        ]}
        return {service_code : filter_value}
    return dash.no_update

@app.callback(Output(id('dashboard-functional-current-year'),'filterModel',allow_duplicate=True),
              Input(id('csu_button'),'n_clicks'),
              prevent_initial_call=True)
def csu_view(n_clicks):
    if n_clicks:
        filter_value= {"operator": "OR", "conditions": [
             {"type": "contains", "filter" : "17"},
             {"type": "contains", "filter" : "Total CSUs"},
        ]}
        return {service_code : filter_value}
    return dash.no_update


@app.callback(Output(id('dashboard-functional-current-year'),'filterModel',allow_duplicate=True),
              Input(id('reset_button'),'n_clicks'),
              prevent_initial_call=True)
def reset_view(n_clicks):
    if n_clicks:
        filter_value= {"type": "contains", "filter" : ""}
        return {role : filter_value}
    return dash.no_update


@app.callback(
    Output(id("dashboard-functional-current-year"),"dashGridOptions",allow_duplicate=True),
    Input(id("dashboard-functional-current-year"), "selectedRows"),
)
def row_pinning_bottom(selection):
    
    if selection is None or len(selection)<1:
        grid_option_patch = Patch()
        grid_option_patch["pinnedBottomRowData"] = []
        return grid_option_patch

    hc_q1=0
    hc_q2=0
    hc_q3=0
    hc_q4=0
    hc_h1=0
    hc_h2=0

    A110_q1=0
    A110_q2=0
    A110_q3=0
    A110_q4=0
    A110_h1=0
    A110_h2=0

    AD10_q1=0
    AD10_q2=0
    AD10_q3=0
    AD10_q4=0
    AD10_h1=0
    AD10_h2=0
    
    TOPS_q1=0
    TOPS_q2=0
    TOPS_q3=0
    TOPS_q4=0
    TOPS_h1=0
    TOPS_h2=0

    cont_q1=0
    cont_q2=0
    cont_q3=0
    cont_q4=0
    cont_h1=0
    cont_h2=0

    wf_q1=0
    wf_q2=0
    wf_q3=0
    wf_q4=0
    wf_h1=0
    wf_h2=0
        
    selected_list=[]
        
    for s in selection:
        
        if s[region]=="":
            selected_list.append(f"{s[role]} from {s[service_name]} ({s[service_code]})")
        else:
            selected_list.append(f"{s[role]} ({s[region]}) from {s[service_name]} ({s[service_code]})")

        hc_q1+=s[Q1_HC]
        hc_q2+=s[Q2_HC]
        hc_q3+=s[Q3_HC]
        hc_q4+=s[Q4_HC]
        hc_h1+=s[H1_HC]
        hc_h2+=s[H2_HC]
        
        A110_q1+=s[Q1_110AC]
        A110_q2+=s[Q2_110AC]
        A110_q3+=s[Q3_110AC]
        A110_q4+=s[Q4_110AC]
        A110_h1+=s[H1_110AC]
        A110_h2+=s[H2_110AC]
        
        AD10_q1+=s[Q1_AD10C]
        AD10_q2+=s[Q2_AD10C]
        AD10_q3+=s[Q3_AD10C]
        AD10_q4+=s[Q4_AD10C]
        AD10_h1+=s[H1_AD10C]
        AD10_h2+=s[H2_AD10C]
        
        TOPS_q1+=s[Q1_TOPS]
        TOPS_q2+=s[Q2_TOPS]
        TOPS_q3+=s[Q3_TOPS]
        TOPS_q4+=s[Q4_TOPS]
        TOPS_h1+=s[H1_TOPS]
        TOPS_h2+=s[H2_TOPS]

        cont_q1+=s[Q1_CONT]
        cont_q2+=s[Q2_CONT]
        cont_q3+=s[Q3_CONT]
        cont_q4+=s[Q4_CONT]
        cont_h1+=s[H1_CONT]
        cont_h2+=s[H2_CONT]
    
        wf_q1+=s[Q1_WF]
        wf_q2+=s[Q2_WF]
        wf_q3+=s[Q3_WF]
        wf_q4+=s[Q4_WF]
        wf_h1+=s[H1_WF]
        wf_h2+=s[H2_WF]  
    

    hc_avg=(hc_h1+hc_h2)/2
    A110_avg=(A110_h1+A110_h2)/2
    AD10_avg=(AD10_h1+AD10_h2)/2
    TOPS_avg=(TOPS_h1+TOPS_h2)/2
    cont_avg=(cont_h1+cont_h2)/2
    wf_avg=(wf_h1+wf_h2)/2
    
        
    grid_option_patch = Patch()
    grid_option_patch["pinnedBottomRowData"] = [{service_name: "Selected rows", role: selected_list,
                                                 Q1_HC: hc_q1, Q2_HC: hc_q2, Q3_HC: hc_q3, Q4_HC: hc_q4, H1_HC: hc_h1, H2_HC: hc_h2, AVG_HC: hc_avg,
                                                 Q1_110AC: A110_q1, Q2_110AC: A110_q2, Q3_110AC: A110_q3, Q4_110AC: A110_q4, H1_110AC: A110_h1, H2_110AC: A110_h2, AVG_110AC: A110_avg,
                                                 Q1_AD10C: AD10_q1, Q2_AD10C: AD10_q2, Q3_AD10C: AD10_q3, Q4_AD10C: AD10_q4, H1_AD10C: AD10_h1, H2_AD10C: AD10_h2, AVG_AD10C: AD10_avg,
                                                 Q1_TOPS: TOPS_q1, Q2_TOPS: TOPS_q2, Q3_TOPS: TOPS_q3, Q4_TOPS: TOPS_q4, H1_TOPS: TOPS_h1, H2_TOPS: TOPS_h2, AVG_TOPS: TOPS_avg,
                                                 Q1_CONT: cont_q1, Q2_CONT: cont_q2, Q3_CONT: cont_q3, Q4_CONT: cont_q4, H1_CONT: cont_h1, H2_CONT: cont_h2, AVG_CONT: cont_avg,
                                                 Q1_WF: wf_q1, Q2_WF: wf_q2, Q3_WF: wf_q3, Q4_WF: wf_q4, H1_WF: wf_h1, H2_WF: wf_h2, AVG_WF: wf_avg}]
    return grid_option_patch