import dash_ag_grid as dag #Must use version 2.4.0
import dash
from dash import html, Patch
from app import app
from dash.dependencies import Input, Output, State
import pages.sourcing_table.dataframe as dataframe
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import utils



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

id=utils.id_factory('dashboard_next_next_year')





DIV_STYLE = {
    "height": "80vh",
}

def get_Layout():
    year=dataframe.year
    next_year=dataframe.next_year
    next_next_year=dataframe.next_next_year
    columnDefs,defaultColDef,getRowStyle=dataframe.get_dashboard(next_next_year)
    data=dataframe.get_dataframe(dataframe.dashboard_ope,dataframe.simu_ope,next_next_year,year,next_year)
    unique_services = data.drop_duplicates(subset=[service_name])
    service_to_code = {row[service_name]: row[service_code] for index, row in unique_services.iterrows()}
    global df
    df=data
    
    layout = html.Div(

    [
        html.H2(f'Dashboard {next_next_year}',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
        html.Hr(),
        html.Div([
            html.Div(dbc.Button('Global view',id=id('global_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
            html.Div(dbc.Button('Corporate view',id=id('corpo_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
            html.Div(dbc.Button('CSUs view',id=id('csu_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
            html.Div(dbc.Button('Reset view',id=id('reset_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '50%', 'display': 'inline-block'}),
            html.Div(dbc.Button('Hide columns',id=id('show_hide'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
            dbc.Popover(
            [
                dbc.PopoverHeader("Select the columns you wish to hide"),
                dbc.PopoverBody(dbc.Checklist(options=[{"label": "Workload", "value": "workload"},{"label": "Headcounts", "value": "headcount"},{"label": "Contractors", "value": "contractor"},
                                                        {"label": "Coverage", "value": "coverage"},{"label": "Flexibility", "value": "flexibility"},{"label": "In-House Workforce", "value": "workforce"},
                                                        {"label": "Internal Workload Gap", "value": "gap"}],value=[],id=id("columns_to_hide"),inline=True)),
            ],
            target=id("show_hide"),
            body=True,
            trigger="legacy",
            placement="bottom"
            ),
            html.Div(dbc.Button('Graphic view',id=id('graphic_button'),n_clicks=0,class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}),style={'width': '10%', 'display': 'inline-block'}),
            ],
            style={"width": "100%","paddingBottom":"15px","paddingBottom":"15px"}),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Graphic View")),
                dbc.ModalBody([
                    html.Div(
                        [
                            dbc.Label("Select at least one time frame"),
                            dbc.Checklist(
                                options=[
                                    {"label": f"Average data for the year {next_next_year}", "value": "full_year"},
                                    {"label": f"1st half of {next_next_year}", "value": "first_half"},
                                    {"label": f"2nd half of {next_next_year}", "value": "second_half"},                                    
                                ],
                                value=["full_year"],
                                id=id("content_checklist"),
                                inline=True,
                            ),
                        ],
                        style={"paddingBottom":"10px"}
                    ),
                    dcc.Dropdown(
                        options=[{'label': f"{service} ({service_to_code[service]})",
                                  'value': service} for service in data[service_name].unique()],
                        multi=True,
                        id=id("content_dropdown"),
                        placeholder="Select at least one service"
                    ),
                    html.Div(id=id("modal_content")),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id=id("close"), class_name="me-2", style={"backgroundColor":"#7A00E6", "borderColor": "#7A00E6"}, n_clicks=0
                    )
                ),
            ],
            id=id("modal"),
            fullscreen=True,
            centered=True,
            is_open=False,
        ),
        dag.AgGrid(
            id=id("dashboard-next-next-year"),
            columnDefs=columnDefs,
            rowData=data.to_dict("records"),
            defaultColDef=defaultColDef,
            style={"height":"100%", "width":"100%"},
            persistence=True,persistence_type='session',
            persisted_props=['filterModel',"selectedRows"],
            dashGridOptions={"rowBuffer": 1,'rowSelection':'multiple',"tooltipShowDelay": 0},
            getRowStyle=getRowStyle,
        ),
    ],
    style=DIV_STYLE,
    )
    return layout


@app.callback(Output(id('dashboard-next-next-year'),'filterModel',allow_duplicate=True),
              Input(id('global_button'),'n_clicks'),
              prevent_initial_call=True)
def global_view(n_clicks):
    if n_clicks:
        filter_value= {"type": "equals", "filter" : "ALL"}
        return {role : filter_value}
    return dash.no_update

@app.callback(Output(id('dashboard-next-next-year'),'filterModel',allow_duplicate=True),
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

@app.callback(Output(id('dashboard-next-next-year'),'filterModel',allow_duplicate=True),
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


@app.callback(Output(id('dashboard-next-next-year'),'filterModel',allow_duplicate=True),
              Input(id('reset_button'),'n_clicks'),
              prevent_initial_call=True)
def reset_view(n_clicks):
    if n_clicks:
        filter_value= {"type": "contains", "filter" : ""}
        return {role : filter_value}
    return dash.no_update


@app.callback(
    Output(id("dashboard-next-next-year"), "columnState"),
    Input(id("columns_to_hide"), "value"),
    State(id("dashboard-next-next-year"), "columnState"),
    prevent_initial_call=True,
)
def update_hide(value,state):

    col_to_hide=[]
    
    if "workload" in value:
        col_to_hide.extend([H1_WL,H2_WL,AVG_WL,Q1_WL,Q2_WL,Q3_WL,Q4_WL])
        
    if "headcount" in value:
        col_to_hide.extend([H1_HC,H2_HC,AVG_HC,Q1_HC,Q2_HC,Q3_HC,Q4_HC])
        
    if "contractor" in value:
        col_to_hide.extend([H1_CONT, H2_CONT, AVG_CONT, Q1_CONT, Q2_CONT, Q3_CONT, Q4_CONT, H1_110AC, H2_110AC, AVG_110AC, Q1_110AC,
                            Q2_110AC, Q3_110AC, Q4_110AC,H1_AD10C, H2_AD10C, AVG_AD10C, Q1_AD10C, Q2_AD10C, Q3_AD10C, Q4_AD10C,
                            H1_TOPS, H2_TOPS,AVG_TOPS, Q1_TOPS, Q2_TOPS, Q3_TOPS, Q4_TOPS])    
        
    if "coverage" in value:
        col_to_hide.extend([H1_COVER, H2_COVER, AVG_COVER, Q1_COVER, Q2_COVER, Q3_COVER, Q4_COVER])
        
    if "flexibility" in value:
        col_to_hide.extend([H1_FLEX, H2_FLEX, AVG_FLEX, Q1_FLEX, Q2_FLEX, Q3_FLEX, Q4_FLEX])
    
    if "workforce" in value:
        col_to_hide.extend([H1_WF, H2_WF, AVG_WF, Q1_WF, Q2_WF, Q3_WF, Q4_WF])
        
    if "gap" in value:
        col_to_hide.extend([H1_GAP, H2_GAP, AVG_GAP, Q1_GAP, Q2_GAP, Q3_GAP, Q4_GAP])

    for col in state:
        col['hide'] = (True and col['colId'] in col_to_hide)        
    
    return state

@app.callback(
    Output(id("modal"), "is_open"),
    [Input(id("graphic_button"), "n_clicks"), Input(id("close"), "n_clicks")],
    [State(id("modal"), "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output(id("modal_content"),"children"),
    Input(id("content_dropdown"),"value"),
    Input(id("content_checklist"),"value"),
    prevent_initial_call=True,
)
def update_modal_content(selected_services,selected_timeframe):
    content=[]
    if selected_services is None:
        return content
    
    if selected_timeframe is None:
        return content
    
    for service in selected_services:
        
        for timeframe in selected_timeframe:
            if timeframe=="full_year":
                
                code=df.loc[df[service_name] == service, service_code].iloc[0]
        
                workload=df.loc[df[service_name] == service, AVG_WL].iloc[0]
                workload=round(workload)
                
                workforce=df.loc[df[service_name] == service, AVG_WF].iloc[0]
                workforce=round(workforce)
                
                hc=df.loc[df[service_name] == service, AVG_HC].iloc[0]
                hc=round(hc)
                
                cont=df.loc[df[service_name] == service, AVG_CONT].iloc[0]
                cont=round(cont)
                
                
                cover = df.loc[df[service_name] == service, AVG_COVER].iloc[0]
                fig_cover = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = cover,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Coverage %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))
                
                fig_cover.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                flex = df.loc[df[service_name] == service, AVG_FLEX].iloc[0]
                fig_flex = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = flex,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Flexibility %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))       
            
                fig_flex.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                row= html.Div([
                    html.H3(f"{service}/{code} (average data for the year {dataframe.next_next_year}):",style={"marginTop":"20px"}),
                    dbc.Row([
                        dbc.Col([html.H4("Workload :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workload} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P("a",style={"fontSize":"large","opacity":0}), html.P("a",style={"fontSize":"large","opacity":0})],style={"textAlign":"center"}),
                        dbc.Col([html.H4("Workforce :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workforce} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P([f"- Headcounts:",html.B(f" {hc} FTEs")],style={"fontSize":"large"}), html.P([f"- Contractors:",html.B(f" {cont} FTEs")],style={"fontSize":"large"})],style={"textAlign":"center"}),
                        dbc.Col(dcc.Graph(figure=fig_cover)),
                        dbc.Col(dcc.Graph(figure=fig_flex)),
                    ],style={"alignItems": "center",'marginTop': '30px'}),
                    html.Hr(),
                ])
                content.append(row)
                
            if timeframe=="first_half":
                
                code=df.loc[df[service_name] == service, service_code].iloc[0]
                
                workload=df.loc[df[service_name] == service, H1_WL].iloc[0]
                workload=round(workload)
                
                workforce=df.loc[df[service_name] == service, H1_WF].iloc[0]
                workforce=round(workforce)
                
                hc=df.loc[df[service_name] == service, H1_HC].iloc[0]
                hc=round(hc)
                
                cont=df.loc[df[service_name] == service, H1_CONT].iloc[0]
                cont=round(cont)
                
                
                cover = df.loc[df[service_name] == service, H1_COVER].iloc[0]
                fig_cover = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = cover,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Coverage %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))
                
                fig_cover.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                flex = df.loc[df[service_name] == service, H1_FLEX].iloc[0]
                fig_flex = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = flex,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Flexibility %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))       
            
                fig_flex.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                row= html.Div([
                    html.H3(f"{service}/{code} (average data for the 1st half of {dataframe.next_next_year}):",style={"marginTop":"20px"}),
                    dbc.Row([
                        dbc.Col([html.H4("Workload :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workload} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P("a",style={"fontSize":"large","opacity":0}), html.P("a",style={"fontSize":"large","opacity":0})],style={"textAlign":"center"}),
                        dbc.Col([html.H4("Workforce :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workforce} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P([f"- Headcounts:",html.B(f" {hc} FTEs")],style={"fontSize":"large"}), html.P([f"- Contractors:",html.B(f" {cont} FTEs")],style={"fontSize":"large"})],style={"textAlign":"center"}),
                        dbc.Col(dcc.Graph(figure=fig_cover)),
                        dbc.Col(dcc.Graph(figure=fig_flex)),
                    ],style={"alignItems": "center",'marginTop': '30px'}),
                    html.Hr(),
                ])
                content.append(row)               
                
            if timeframe=="second_half":
                
                code=df.loc[df[service_name] == service, service_code].iloc[0]
                
                workload=df.loc[df[service_name] == service, H2_WL].iloc[0]
                workload=round(workload)
                
                workforce=df.loc[df[service_name] == service, H2_WF].iloc[0]
                workforce=round(workforce)
                
                hc=df.loc[df[service_name] == service, H2_HC].iloc[0]
                hc=round(hc)
                
                cont=df.loc[df[service_name] == service, H2_CONT].iloc[0]
                cont=round(cont)
                
                
                cover = df.loc[df[service_name] == service, H2_COVER].iloc[0]
                fig_cover = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = cover,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Coverage %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))
                
                fig_cover.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                flex = df.loc[df[service_name] == service, H2_FLEX].iloc[0]
                fig_flex = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = flex,
                    number={"suffix":"%"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Flexibility %"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#23004C"}}))       
            
                fig_flex.update_layout(
                    margin=dict(l=50, r=50, t=5, b=5),
                )
                
                row= html.Div([
                    html.H3(f"{service}/{code} (average data for the 2nd half of {dataframe.next_next_year}):",style={"marginTop":"20px"}),
                    dbc.Row([
                        dbc.Col([html.H4("Workload :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workload} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P("a",style={"fontSize":"large","opacity":0}), html.P("a",style={"fontSize":"large","opacity":0})],style={"textAlign":"center"}),
                        dbc.Col([html.H4("Workforce :",style={"fontWeight":"normal","fontSize":"xx-large"}), html.P(f"{workforce} FTEs",style={"fontWeight":"bold","fontSize":"x-large"}), html.P([f"- Headcounts:",html.B(f" {hc} FTEs")],style={"fontSize":"large"}), html.P([f"- Contractors:",html.B(f" {cont} FTEs")],style={"fontSize":"large"})],style={"textAlign":"center"}),
                        dbc.Col(dcc.Graph(figure=fig_cover)),
                        dbc.Col(dcc.Graph(figure=fig_flex)),
                    ],style={"alignItems": "center",'marginTop': '30px'}),
                    html.Hr(),
                ])
                content.append(row)                
                                
    return content
 

@app.callback(
    Output(id("dashboard-next-next-year"),"dashGridOptions",allow_duplicate=True),
    Input(id("dashboard-next-next-year"), "selectedRows"),
)
def row_pinning_bottom(selection):
    
    if selection is None or len(selection)<1:
        grid_option_patch = Patch()
        grid_option_patch["pinnedBottomRowData"] = []
        return grid_option_patch

    wl_q1=0
    wl_q2=0
    wl_q3=0
    wl_q4=0
    wl_h1=0
    wl_h2=0

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
        
        wl_q1+=s[Q1_WL]
        wl_q2+=s[Q2_WL]
        wl_q3+=s[Q3_WL]
        wl_q4+=s[Q4_WL]
        wl_h1+=s[H1_WL]
        wl_h2+=s[H2_WL]
        
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
    
    
    gap_q1=wf_q1-wl_q1
    gap_q2=wf_q2-wl_q2
    gap_q3=wf_q3-wl_q3
    gap_q4=wf_q4-wl_q4
    gap_h1=(gap_q1+gap_q2)/2
    gap_h2=(gap_q3+gap_q4)/2
    gap_avg=(gap_h1+gap_h2)/2

    cov_q1=0 if wl_q1 == 0 else wf_q1/wl_q1*100
    cov_q2=0 if wl_q2 == 0 else wf_q2/wl_q2*100
    cov_q3=0 if wl_q3 == 0 else wf_q3/wl_q3*100
    cov_q4=0 if wl_q4 == 0 else wf_q4/wl_q4*100
    cov_h1=(cov_q1+cov_q2)/2
    cov_h2=(cov_q3+cov_q4)/2
    cov_avg=(cov_h1+cov_h2)/2
    
    flex_q1=0 if wf_q1==0 else cont_q1/wf_q1*100
    flex_q2=0 if wf_q2==0 else cont_q2/wf_q2*100
    flex_q3=0 if wf_q3==0 else cont_q3/wf_q3*100
    flex_q4=0 if wf_q4==0 else cont_q4/wf_q4*100

    flex_h1=(flex_q1+flex_q2)/2
    flex_h2=(flex_q3+flex_q4)/2
    flex_avg=(flex_h1+flex_h2)/2
    
    wl_avg=(wl_h1+wl_h2)/2
    hc_avg=(hc_h1+hc_h2)/2
    A110_avg=(A110_h1+A110_h2)/2
    AD10_avg=(AD10_h1+AD10_h2)/2
    TOPS_avg=(TOPS_h1+TOPS_h2)/2
    cont_avg=(cont_h1+cont_h2)/2
    wf_avg=(wf_h1+wf_h2)/2
    
        
    grid_option_patch = Patch()
    grid_option_patch["pinnedBottomRowData"] = [{service_name: "Selected rows", role: selected_list,
                                                 Q1_WL: wl_q1, Q2_WL: wl_q2, Q3_WL: wl_q3, Q4_WL: wl_q4, H1_WL: wl_h1, H2_WL: wl_h2, AVG_WL: wl_avg,
                                                 Q1_HC: hc_q1, Q2_HC: hc_q2, Q3_HC: hc_q3, Q4_HC: hc_q4, H1_HC: hc_h1, H2_HC: hc_h2, AVG_HC: hc_avg,
                                                 Q1_110AC: A110_q1, Q2_110AC: A110_q2, Q3_110AC: A110_q3, Q4_110AC: A110_q4, H1_110AC: A110_h1, H2_110AC: A110_h2, AVG_110AC: A110_avg,
                                                 Q1_AD10C: AD10_q1, Q2_AD10C: AD10_q2, Q3_AD10C: AD10_q3, Q4_AD10C: AD10_q4, H1_AD10C: AD10_h1, H2_AD10C: AD10_h2, AVG_AD10C: AD10_avg,
                                                 Q1_TOPS: TOPS_q1, Q2_TOPS: TOPS_q2, Q3_TOPS: TOPS_q3, Q4_TOPS: TOPS_q4, H1_TOPS: TOPS_h1, H2_TOPS: TOPS_h2, AVG_TOPS: TOPS_avg,
                                                 Q1_CONT: cont_q1, Q2_CONT: cont_q2, Q3_CONT: cont_q3, Q4_CONT: cont_q4, H1_CONT: cont_h1, H2_CONT: cont_h2, AVG_CONT: cont_avg,
                                                 Q1_WF: wf_q1, Q2_WF: wf_q2, Q3_WF: wf_q3, Q4_WF: wf_q4, H1_WF: wf_h1, H2_WF: wf_h2, AVG_WF: wf_avg,
                                                 Q1_GAP: gap_q1, Q2_GAP: gap_q2, Q3_GAP: gap_q3, Q4_GAP: gap_q4, H1_GAP: gap_h1, H2_GAP: gap_h2, AVG_GAP: gap_avg,
                                                 Q1_COVER: cov_q1, Q2_COVER: cov_q2, Q3_COVER: cov_q3, Q4_COVER: cov_q4, H1_COVER: cov_h1, H2_COVER: cov_h2, AVG_COVER: cov_avg,
                                                 Q1_FLEX: flex_q1, Q2_FLEX: flex_q2, Q3_FLEX: flex_q3, Q4_FLEX: flex_q4, H1_FLEX: flex_h1, H2_FLEX: flex_h2, AVG_FLEX: flex_avg}]
    return grid_option_patch