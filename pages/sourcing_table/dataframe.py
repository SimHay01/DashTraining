import numpy as np
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import utils
import re
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import base64
import io
import traceback
from datetime import datetime
import glob
import os
from dateutil.relativedelta import relativedelta
pd.options.mode.chained_assignment = None  # default='warn'


#================================================================================================
#Import from the file "utils" the name of the variables to have a better maintenancy
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

# TODO: 1
#If new or change in service, update the following dictionnary
service = {
    "DB1000":"MOF",
    "DB1001":"TPO",
    "DB1100":"CQCI",
    "DB1200":"CPM",
    "DB1201":"CPOEI",
    "DB1300":"CDOC",
    "DB1301":"OMD", #No longer relevant
    "DB1400":"EDO", #No longer relevant
    "DB1401":"EDCO",
    "DB1500":"TO", #No longer relevant
    "DB1501":"EDOO", #No longer relevant
    "DB1502":"CDMS", 
    "DB1503":"SPAR",
    "DB1600":"BP", #No longer relevant
    "DB1700":"GRSM",
    "DB1701":"CSU",
    "DB1800":"CSC",
    "BS1000":"STAT",
    "BS1001":"CMEI",
    "BS1002":"RWE",    
}

#================================================================================================
""""To define the directory where the .csv files will be stored, according the the DEV, UAT or PROD
"""
dev_mod=True
uat_mod=False # turn to True when working with the UAT directory in WISE, else will be the PROD diretory

# developing locally, the data directory will be in "cwd/data"
if dev_mod:
    # os.getcwd(): to get current working directory as a string
    # os.path.join(): to correctly join the cwd and the 'data' directory (with forward slashes) -> "cwd/data"
    base_path=os.path.join(os.getcwd(), 'data')
elif uat_mod:
    base_path = "/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/UAT_TEST/"
else:
    base_path = "/home/gnw_sourcingtableapp/wise/DEVOPS/DASH/APPS/SOURCING_TABLE_APP/EXPLO/DATA/"

#================================================================================================
# This part to define the 5 different dataframes that the app uses to run

""""To define the filename pattern of dashboard_ope - *
To define the corresponding dataframe
To find the date of the data present in the file
"""
filename_pattern = "dashboard_ope - *.csv"

# Find the file paths that match a specified pattern
# base_path = the start of the path (different whether it is in PROD, UAT or DEV mode)
# glob.glob(): returns a list of file paths that match the specified pattern
file_list = glob.glob(f"{base_path}/{filename_pattern}")
dashboard_ope=pd.read_csv(file_list[0],sep=';')

# Expression régulière pour trouver les motifs "Month YYYY", "DD Month YYYY" ou "YYYY"
# Regular expression (regex)
# \b: Word boundary, ensuring the match is at the start or end of a word.
# \d{1,2}: Matches one or two digits (representing the day of the month).
# \s: Matches a whitespace character (space).
# (?:January|February|...|December): Non-capturing group that matches any month name.
# \s: Matches another whitespace character (space).
# \d{4}: Matches exactly four digits (representing the year).
# \b: Word boundary, ensuring the match is at the start or end of a word
regex = re.compile(r'''
                   (
                   # Matches dates in the format “day month year” (e.g., “12 January 2023”)
                   \b\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b|
                   # Matches dates in the format “month year” (e.g., “January 2023”)
                   \b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b|
                   # Matches a four-digit year (e.g., “2023”)
                   \b\d{4}\b
                   )
                   ''',re.VERBOSE)

# re.search() : scans through a string, looking for any location where the regular expression pattern matches. 
# Returns a match object if a match is found, or None if no match is found.
match = re.search(regex, file_list[0])

if match:
    # extract the matched substring from a match object
    # group(0) returns the entire substring that was matched by the regular expression
    # The argument 0 refers to the entire match
    date = match.group(0)
else:
    date=""

"""To define the filename pattern of dashboard_func - *
To define the corresponding dataframe
"""
filename_pattern = "dashboard_func - *.csv"
file_list = glob.glob(f"{base_path}/{filename_pattern}")
dashboard_func=pd.read_csv(file_list[0],sep=';')

"""To define the filename pattern of simulation_ope - *
To define the corresponding dataframe
"""
filename_pattern = "simulation_ope - *.csv"
file_list = glob.glob(f"{base_path}/{filename_pattern}")
simu_ope=pd.read_csv(file_list[0],sep=';')

"""To define the filename pattern of simulation_func - *
To define the corresponding dataframe
"""
filename_pattern = "simulation_func - *.csv"
file_list = glob.glob(f"{base_path}/{filename_pattern}")
simu_func=pd.read_csv(file_list[0],sep=';')

"""To define the filename pattern of operational_rate.csv
To define the corresponding dataframe
"""
filename_pattern = "operational_rate.csv"
file_list = glob.glob(f"{base_path}/{filename_pattern}")
try:
    initial_rate=pd.read_csv(file_list[0],sep=';') # if an error occurs while trying the read the file, exception will be catched
except Exception as error:
    initial_rate=1

#================================================================================================
"""This list of funtions to get the date of the data, the year, year+1 & year+2 as global variables
"""        
def getDate():
    """To get the date of the set of 5 files used to run the app
    date is a global variable defined using the dashboard_ope - *.csv
    Returns a date
    """
    global date
    return date
    
def extract_unique_years(column_names):
    """To extract the unique years within the column names
    Returns a list of unique years in the iterable ascending order
    """
    years = set()
    #r": This is a raw string indicator in Python. 
    # It tells Python to treat the backslashes (\) in the string literally, not as escape characters.
    # \d: This is a regex metacharacter that represents any digit (0-9).
    # {4}: This specifies that the preceding element (\d) should appear exactly 4 times.
    # = to match exactly four consecutive digits (like 2024, 1234, 0001, etc.), which is the standard format of a year.
    pattern = r"\d{4}" 

    for name in column_names:
        found_years = re.findall(pattern, name)
        if found_years:
            years.update(found_years)
    return sorted(years)

# Define the unique list of years using dashboard_ope files columns
years_list=extract_unique_years(dashboard_ope.columns.tolist())

# Define the year
year=int(years_list[0])
# Define the year+1
next_year=int(years_list[1])
# Define the year+2
next_next_year=int(years_list[2])

def getYear():
    global year
    return year

def getNextYear():
    global next_year
    return next_year

def getYearTwo():
    global next_next_year
    return next_next_year

#================================================================================================
"""This list of functions to return a dataframe and a dashboard with a specific year
"""
def getDf(df):
    return df

def get_dashboard(year):
    """
    Return data under the shape of a dashboard for a specific year
    Useful for the dashboard pages

    Args:
        year (int): year of the data to keep


    Returns:
        columnDefs(Ag-Grid): definition of the different columns of the Ag-Grid
        defaultColDef (Ag-Grid): global parameters of the Ag-Grid columns
        defaultGetRowStyle (Ag-Grid): default style of row filling specifiques conditions (ex. row with global data)
    """

    #Transform the year from the format yyyy to the format yy
    year_yy= year % 100

    #Variables used to name the different columns
    H1 = f"1H {year_yy}"
    H2 = f"2H {year_yy}"
    AVG = f"Avg {year_yy}"
    Q1 = f"1Q {year_yy}"
    Q2 = f"2Q {year_yy}"
    Q3 = f"3Q {year_yy}"
    Q4 = f"4Q {year_yy}"

    # Definitions and parameters for each column in the ag grid. 
    # Documentation available here: https://www.ag-grid.com/archive/29.3.5/react-data-grid/column-properties/
    # 
    # Using AG Grid in Dash (with its back-end running thanks to Flask) is typically done using JSON (JavaScript Object Notation) 
    # or JSON-like structures
    # because AG Grid is a JavaScript library and it runs in the browser as part of the frontend
    # The frontend in a Dash or Flask web application (which renders HTML and JavaScript) needs to communicate 
    # with AG Grid in a format that the browser and AG Grid understand—this format is JSON.
    # JSON is the most commonly used format for data interchange between the backend (Python) and the frontend (JavaScript).
    #Writing the columnDefs in JSON ensures that the data structure can be seamlessly transferred from the Python backend to the JavaScript frontend where AG Grid will render it.
    columnDefs= [
        {
            "headerName": "Characteristics",
            "children":[
                {
                    "headerName":service_code,
                    "field": service_code,                  
                    "width":100,
                    "cellStyle":{"styleConditions":[{"condition": f"params.data.{role} != 'ALL'", "style":{"color":"rgb(174,174,174)"}}]}, 
                    'floatingFilter': True,
                    "filter": True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    
                },
                {
                    "headerName":service_name,
                    "field":service_name,  
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {"styleConditions":[{"condition": f"params.node.rowPinned === 'bottom'", "style":{"textDecoration":"underline",'borderLeft': '1px solid lightgrey'}}],"defaultStyle": {'borderLeft': '1px solid lightgrey'}}, 
                    "tooltipField": service_name,
                },
                {
                    "headerName":role,
                    "field":role,     
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {"styleConditions":[{"condition": f"params.node.rowPinned === 'bottom'", "style":{"color":"transparent",'borderLeft': '1px solid lightgrey'}}],"defaultStyle": {'borderLeft': '1px solid lightgrey'}}, 
                },
                {
                    "headerName":region,
                    "field":region,    
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":10,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                
            ]
        },

        {
            "headerName": "Workload FTE",
            "children": [
                {   
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field" : H1_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},     
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field" : H2_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field" : AVG_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field": Q1_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},  
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field": Q2_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field": Q3_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field": Q4_WL,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                },
            ]
        },
        {
            "headerName": "Headcounts FTE",
            "children": [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field" : H1_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},    
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field" : H2_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field" : AVG_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},   
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field": Q1_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},  
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field": Q2_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},   
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field": Q3_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field": Q4_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                },
            ]
        },
        {
            "headerName": "Insourcing Contractors FTE",
            "children":[
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field" : H1_CONT,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},   
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field" : H2_CONT,                 
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field" : AVG_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                "headerName": "Details",
                "columnGroupShow": "open",
                "children":[
                    {
                    "headerName": Q1,
                    "columnGroupShow": "closed",
                    "field" : Q1_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '3px solid black'}, 
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "closed",
                    "field" : Q2_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "closed",
                    "field" : Q3_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "closed",
                    "field" : Q4_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                    {
                "headerName": "110A Committed FTE",
                "columnGroupShow": "open",

                "children": [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field" : H1_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},    
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field" : H2_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field" : AVG_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},      
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field": Q1_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},    
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field": Q2_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field": Q3_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field": Q4_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                ]
                },
                {
                "headerName": "AD10 Committed FTE",
                "columnGroupShow": "open",    
                "children": [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field" : H1_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},         
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field" : H2_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},       
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field" : AVG_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field": Q1_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},  
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field": Q2_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field": Q3_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field": Q4_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                ]
                },
                {
                "headerName":"110A+AD10 Top Adjustements",
                "columnGroupShow":"open",
                "children":
                [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field": H1_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'}, 
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field": H2_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},  
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field": AVG_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field":Q1_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},     
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field":Q2_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field":Q3_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field":Q4_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'},     
                    },
                ]
                },
                ]
                },        
                
            ]
        },
        {
            "headerName":"Internal Workload Coverage %",
            "children":
            [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field": H1_COVER,
                    "width":82,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field":H2_COVER,
                    "width":82,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field":AVG_COVER,
                    "width":82,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field": Q1_COVER,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field":Q2_COVER,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field":Q3_COVER,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'},      
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field":Q4_COVER,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
            ]
        },
        {
            "headerName":"Internal Flexibility %",
            "children":
            [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field":H1_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '3px solid black'}, 
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field":H2_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field":AVG_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field":Q1_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field":Q2_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field":Q3_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field":Q4_FLEX,
                    "width":75,
                    "valueFormatter": {"function": "Math.round(params.value)+'%'"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
            ]
        },
        {
            "headerName":"In-House Workforce",
            "children":
            [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field":H1_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                        
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field":H2_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field":AVG_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field":Q1_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field":Q2_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field":Q3_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field":Q4_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
            ]
        },
        
        {
            "headerName":"Internal Workload Gap FTEs",
            "children":
            [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field":H1_GAP,
                    "width":77,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                    
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field":H2_GAP,
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field":AVG_GAP,
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey','borderRight': '2px solid black'}, 
                    
                    
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field":Q1_GAP,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field":Q2_GAP,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field":Q3_GAP,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field":Q4_GAP,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey','borderRight': '2px solid black'}, 
                    
                },
            ]
        },    
    ]
#================================================================================================

    defaultColDef = {"resizable": True, "filter": False,"wrapHeaderText": True,"suppressMovable": True, 
                     "valueFormatter": {"function": "Math.round(params.value)"},"tooltipComponent": "CustomTooltip"}
    
    
    
    #Default row style
    defaultGetRowStyle = {
        "styleConditions": [
            {
                "condition": "params.data['Service Code'] ==='Total Corporate'",
                "style": {"backgroundColor": "rgba(35,0,76,0.9)","color":"white"},
            },
            {
                "condition": "params.data['Service Code'] ==='Total CSUs'",
                "style": {"backgroundColor": "rgba(35,0,76,0.9)","color":"white"},
            },
            {
                "condition": "params.data['Service Code'] ==='Total CSO'",
                "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white"},
            },
            {
                "condition": "params.data['Service Code'] ==='Total CSO+EGDS'",
                "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white"},
            },
            {
                "condition": "params.data['Role'] ==='ALL' && params.data['Region'] !='ALL' && !params.data['Service Code'].includes('17')",
                "style": {"backgroundColor": "rgba(35,0,76,0.5)","color":"white"},
            },
            {
                "condition": "params.data['Role'] ==='ALL' && params.data['Region'] !='ALL' && params.data['Service Code'].includes('17')",
                "style": {"backgroundColor": "rgba(35,0,76,0.5)","color":"white"},
            },
            {
                "condition": "params.data['Role'] ==='ALL' && params.data['Region'] ==='ALL' && !params.data['Service Code'].includes('17')",
                "style": {"backgroundColor": "rgba(35,0,76,0.75)","color":"white"},
            },
            {
                "condition": "params.data['Role'] ==='ALL' && params.data['Region'] ==='ALL' && params.data['Service Code'].includes('17')",
                "style": {"backgroundColor": "rgba(35,0,76,0.75)","color":"white"},
            },
            {
                "condition": "params.node.rowPinned ==='bottom'",
                "style": {"backgroundColor": "slategray","color":"white"},
            },
            
            
        ],
    }

    return columnDefs, defaultColDef,defaultGetRowStyle


# Style de base pour dcc.Upload
base_style = {
    'width': '370px',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px',
    'color': '#888'
}

# Style lorsque le fichier est chargé
loaded_style = {
    'width': '370px',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '2px',
    'borderStyle': 'solid',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px',
    'color': 'green',
    'borderColor': 'green'
}


#layout du chargement des données lors d'une nouvelle baseline. 
# Penser à bien updater le lien du rapport Tableau si celui-ci change
layout=html.Div(
    [
        html.H2(f'New baseline',style={"textAlign":"center","color":"#23004C", "paddingTop":"10px"}),
        html.Hr(),
        html.P(["At present, the Datahub access request has still not been processed by the Digital department. Therefore, to load the data for a new baseline, you need to go to this ",dcc.Link("Tableau report",
                 href=r"https://tableau-emea.sanofi.com/#/site/RDPMBIReporting/views/ID365-CSO-Sourcingtableextract/Sourcingtableextract?:iid=1",target="_blank"),
                html.Span(" and download the excel files corresponding to the data. Then upload these files here in the corresponding sections below and click on the \"Import data\" button. The application will automatically update itself with the new data.")]),
        html.H4("Workload data",style={"textAlign":"center", "paddingTop":"10px"}),
        html.Div(
            [
                dcc.Upload(
                    id="upload_workload",
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."]
                    ),
                    style=base_style,
                    multiple=False,
                ),
            ],
            style={"display": "flex", "justifyContent": "center","width": "100%"},
        ),
        html.H4("Resources data",style={"textAlign":"center", "paddingTop":"10px"}),
        html.Div(
            [
                dcc.Upload(
                    id="upload_resource",
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."]
                    ),
                    style=base_style,
                    multiple=False,
                ),
            ],
            style={"display": "flex", "justifyContent": "center","width": "100%"},
        ),
        dcc.Loading(
            id="loading-1",
            type="circle",  # Types include 'graph', 'cube', 'circle', 'dot', etc.
            color="#7A00E6",
            children=[
                html.Div(
                    [
                        dbc.Alert(children=None, color="success", id='alert-upload', is_open=False, className='ms-4',duration=5000),
                        dbc.Button('Import data', id='import_button', n_clicks=0, className="me-2", disabled=True, style={"backgroundColor": "#7A00E6", "borderColor": "#7A00E6"})
                    ],
                    style={"textAlign": "center", "paddingTop": "20px", "width": "17rem", "margin": "0 auto"},
                )
            ]
        ),
        html.Div(
            dbc.Checklist(
                options=[
                    {"label": "Keep the TOPs from the last import", "value": True},
                ],
                id="keep_tops",
                switch=True,
                input_checked_style={
                    "backgroundColor": "#7A00E6",
                    "borderColor": "#7A00E6",
                },
                style={"transform": "scale(1.1)"}
            ), 
            style={"display": "flex", "justifyContent": "center", "paddingTop": "30px"}       
        ),

        html.Div(id='date_workload', style={'display': 'none'}),
        html.Div(id='date_resource', style={'display': 'none'}),
        
        
    ]
)

@app.callback(
    [Output('upload_resource', 'style'),
     Output('upload_resource', 'children')],
    Input('upload_resource', 'filename'),
    prevent_initial_call=True
)
def update_output_style(filename):
    if filename is not None:
        return loaded_style,filename
    return base_style,"Drag and drop or click to select a file to upload."

@app.callback(
    [Output('upload_workload', 'style'),
     Output('upload_workload', 'children')],
    Input('upload_workload', 'filename'),
    prevent_initial_call=True
)
def update_output_style(filename):
    if filename is not None:
        return loaded_style,filename
    return base_style,"Drag and drop or click to select a file to upload."

@app.callback(
    Output('import_button', 'disabled'),
    [Input('upload_workload', 'contents'), Input('upload_resource', 'contents')]
)
def enable_processing_button(contents1, contents2):
    if contents1 and contents2:
        return False
    return True

app.clientside_callback(
    """
    function(contents) {
        if (contents) {
            var uploadComponent = document.querySelector('#upload_workload input[type="file"]');
            
            if (uploadComponent && uploadComponent.files.length > 0) {
                var file = uploadComponent.files[0];
                return (file.lastModified);
            }
        }
    }
    """,
    Output('date_workload', 'children'),
    Input('upload_workload', 'contents')
)

app.clientside_callback(
    """
    function(contents) {
        if (contents) {
            var uploadComponent = document.querySelector('#upload_resource input[type="file"]');
    
            if (uploadComponent && uploadComponent.files.length > 0) {
                var file = uploadComponent.files[0];
                return (file.lastModified);
            }
        }
    }
    """,
    Output('date_resource', 'children'),
    Input('upload_resource', 'contents')
)

def process_content(content):
    if content:
        content_type, content_string = content.split(',', 1)
        decoded = base64.b64decode(content_string)
        if 'csv' in content_type:
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'excel' in content_type or 'spreadsheetml' in content_type:
            df = pd.read_excel(io.BytesIO(decoded),nrows=0)
            if any("Unnamed" in str(col) for col in df.columns):  
                df = pd.read_excel(io.BytesIO(decoded), header=[0, 1])
            else:
                df = pd.read_excel(io.BytesIO(decoded))
            return df
    return None


# Fonction pour extraire et formater la date selon le contenu de la chaîne
def extract_and_format_date(s,date_workload):
    if 'Live' in s:
        # Si "Live" est dans la chaîne, utiliser la date actuelle
        date_str = s.split('Live ')[-1]  # On prend la partie après "Live "
        date_workload = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B %Y')
        return date_workload
    elif 'Yearly' in s:
        # Si "Yearly" est présent mais sans mois spécifique, renvoyer juste l'année
        year_part = s.split(' - ')[0]
        return year_part.strip()
    else:
        # Extraire la date normalement pour les autres cas
        date_part = s.split(' - ')[0]
        date_datetime = pd.to_datetime(date_part, format='%Y-%m')
        return date_datetime.strftime('%B %Y')

class DateMismatchException(Exception):
    """Exception raised when the dates do not match."""
    def __init__(self, message="The dates in the resources data and workload data do not match."):
        self.message = message
        super().__init__(self.message)

@app.callback(
    [Output('alert-upload', 'children'),Output('alert-upload', 'color'),Output('alert-upload', 'is_open'),Output('data_date','children'),
     Output('ope_year','children'),Output('ope_next_year','children'),Output('ope_year_two','children'),
     Output('func_year','children'),Output('func_next_year','children'),Output('func_year_two','children')],
    Input('import_button',"n_clicks"),
    [State('upload_resource', 'contents'), State('upload_workload', 'contents'),State('date_workload', 'children'),State('date_resource', 'children'),State("keep_tops",'value')],
    prevent_initial_call=True
)
def update_output(n_clicks,resource, workload,date_workload,date_resource,keep_tops):
    if n_clicks==0 or not resource or not workload:
        return dash.no_update

    global date
    global dashboard_ope
    global dashboard_func
    global simu_ope
    global simu_func
    global initial_rate
    global tops_export
    global year
    global next_year
    global next_next_year
    
    old_date=date
    old_dashboard_ope=dashboard_ope
    old_dashboard_func=dashboard_func
    old_simu_ope=simu_ope
    old_simu_func=simu_func
    old_initial_rate=initial_rate
    old_tops_export=tops_export
    old_year=year
    old_next_year=next_year
    old_next_next_year=next_next_year

    try: 
        if keep_tops == [True]:
            checked=True
        else:
            checked=False
        
        
        df_resource = process_content(resource)
        df_workload = process_content(workload)

        date = extract_and_format_date(df_workload.loc[0, 'Bas Desc '],date_workload) #Laissez un espace qui est présent dans le rapport tableau pour la workload
        
        df_resource.columns = ['_'.join(col for col in col_tuple if not col.startswith('Unnamed')).strip()
            if isinstance(col_tuple, tuple) else col_tuple
            for col_tuple in df_resource.columns]

        date_resource=extract_and_format_date(df_resource.loc[0, 'Bas Desc'],date_resource)#Pas d'espace dans le rapport tableau pour la workforce
        
        if date!= date_resource:
            raise DateMismatchException(f"Dates from the two data sources are different! {date} =!= {date_resource}")
        
        new_baseline(df_resource,df_workload,date,checked)
        return "Data have been successfully imported!","success",True,getDate(),f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}",f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}"
    except DateMismatchException as e:
        date=old_date
        dashboard_ope=old_dashboard_ope
        dashboard_func=old_dashboard_func
        simu_ope=old_simu_ope
        simu_func=old_simu_func
        initial_rate=old_initial_rate
        tops_export=old_tops_export
        year=old_year
        next_year=old_next_year
        next_next_year=old_next_next_year
        
        simu_ope.to_csv(os.path.join(base_path, f"simulation_ope - {date}.csv"),index=False,sep=';')
        simu_func.to_csv(os.path.join(base_path, f"simulation_func - {date}.csv"),index=False,sep=';')
        dashboard_ope.to_csv(os.path.join(base_path, f"dashboard_ope - {date}.csv"),index=False,sep=';')
        dashboard_func.to_csv(os.path.join(base_path, f"dashboard_func - {date}.csv"),index=False,sep=';')
        tops_export.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')
        initial_rate.to_csv(os.path.join(base_path, f"operational_rate.csv"),index=False,sep=';')
        files_to_keep=[f"dashboard_func - {date}.csv",f"simulation_func - {date}.csv",f"dashboard_ope - {date}.csv",f"simulation_ope - {date}.csv","operational_rate.csv",f"CSO_Tops - {date}.csv"]
     
        for file in os.listdir(base_path):
            path= os.path.join(base_path,file) 
            
            if file not in files_to_keep and os.path.isfile(path):
                
                os.remove(path)
        print(e)
        traceback.print_exc()
        return "Error, data have not been imported! The dates of the two data sources are different, please check your files or re-download them via the Tableau report", "danger", True,getDate(),f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}",f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}"
    except Exception as error:
        date=old_date
        dashboard_ope=old_dashboard_ope
        dashboard_func=old_dashboard_func
        simu_ope=old_simu_ope
        simu_func=old_simu_func
        initial_rate=old_initial_rate
        tops_export=old_tops_export
        year=old_year
        next_year=old_next_year
        next_next_year=old_next_next_year
        
        simu_ope.to_csv(os.path.join(base_path, f"simulation_ope - {date}.csv"),index=False,sep=';')
        simu_func.to_csv(os.path.join(base_path, f"simulation_func - {date}.csv"),index=False,sep=';')
        dashboard_ope.to_csv(os.path.join(base_path, f"dashboard_ope - {date}.csv"),index=False,sep=';')
        dashboard_func.to_csv(os.path.join(base_path, f"dashboard_func - {date}.csv"),index=False,sep=';')
        tops_export.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')
        initial_rate.to_csv(os.path.join(base_path, f"operational_rate.csv"),index=False,sep=';')
        files_to_keep=[f"dashboard_func - {date}.csv",f"simulation_func - {date}.csv",f"dashboard_ope - {date}.csv",f"simulation_ope - {date}.csv","operational_rate.csv",f"CSO_Tops - {date}.csv"]
     
        for file in os.listdir(base_path):
            path= os.path.join(base_path,file) 
            
            if file not in files_to_keep and os.path.isfile(path):
                
                os.remove(path)
        
        print(error)
        traceback.print_exc()
        return "Error, data have not been imported! Check that you have uploaded the correct files", "danger", True,getDate(),f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}",f"Dashboard {getYear()}",f"Dashboard {getNextYear()}",f"Dashboard {getYearTwo()}"



def new_baseline(df_resource,df_workload,date,checked):
    global simu_ope
    global simu_func
    if checked:
        old_tops_ope=simu_ope[simu_ope[info].isin(["110A TOPs","AD10 TOPs"])]
        old_tops_func=simu_func[simu_func[info].isin(["110A TOPs","AD10 TOPs"])]
    
    # Filtrer le DataFrame pour exclure les lignes où la colonne 'row number' contient 'Grand total' (insensible à la casse)
    df_resource = df_resource[~df_resource['row number'].str.contains('Total', case=False, na=False)]
    
    # Filtrer le DataFrame pour exclure les lignes où la colonne 'row number' contient 'Grand total' (insensible à la casse)
    df_workload = df_workload[~df_workload['row number'].str.contains('Total', case=False, na=False)]
    
    df_resource=df_resource.drop(columns='Bas Desc')
    df_workload=df_workload.drop(columns='Bas Desc ')
    
    df_resource=df_resource.drop(columns='row number')
    df_workload=df_workload.drop(columns='row number')
    
    df_resource[service_name]=df_resource["Service Code"].map(service)
    df_workload[service_name]=df_workload["Service Code"].map(service)
    
    df_resource=df_resource.rename(columns={'Service Code': service_code})
    df_resource=df_resource.rename(columns={'Kpi Skill': role})
    df_resource=df_resource.rename(columns={'CSU Region': region})
    
    df_workload=df_workload.rename(columns={'Service Code': service_code},)
    df_workload=df_workload.rename(columns={'Kpi Skill': role})
    df_workload=df_workload.rename(columns={'CSU Region': region})
    
    
    df_workload = df_workload.query('`Kpi Int Out Resource` != "External"')
    df_workload=df_workload.drop(columns='Kpi Int Out Resource')
    df_workload=df_workload.drop(columns='Kpi Budget Decision')
    df_workload=df_workload.drop(columns='Kpi Prp')
    df_workload=df_workload.drop(columns='Kpi Res Team')
    df_workload=df_workload.drop(columns='Service Desc')
    df_workload=df_workload.drop(columns='Rol Rolename')
    
    df_workload[region]=df_workload[region].fillna(value='(blank)')
    df_workload=df_workload.fillna(value=0)
    df_workload=df_workload.groupby([service_code,service_name,role,region]).sum().reset_index()
    
    df_resource=df_resource.drop(columns='Rol Rolename')
    df_resource=df_resource.drop(columns='Service Desc')
    
    df_resource[region]=df_resource[region].fillna(value='(blank)')
    df_resource=df_resource.fillna(value=0)
    df_func=df_resource.query('Operationality == "Functional"')
    df_ope=df_resource.query('Operationality == "Operational"')
    
    df_func=df_func.drop(columns="Operationality")
    df_ope=df_ope.drop(columns="Operationality")
    
    columns_to_drop = [col for col in df_func.columns if "Available" in col]
    df_func.drop(columns=columns_to_drop, inplace=True)
    
    columns_to_drop = [col for col in df_ope.columns if "Headcount" in col]
    df_ope.drop(columns=columns_to_drop, inplace=True)
    
    
    # Fonction pour transformer les noms de colonnes
    def transform_column_name(col_name):
        if "_" in col_name:
            parts = col_name.split("_")
            year_quarter = parts[-1].split()
            return f"{year_quarter[0]} {year_quarter[1]}"
        else:
            return col_name
    
    # Appliquer la fonction de transformation et renommer les colonnes
    df_func=df_func.rename(columns={col: transform_column_name(col) for col in df_func.columns})
    # Appliquer la fonction de transformation et renommer les colonnes
    df_ope=df_ope.rename(columns={col: transform_column_name(col) for col in df_ope.columns})
    
    df_func=df_func.drop(columns="% Direct")
    
    df_ope_110a=df_ope.query('`Contract Type` == "CONTS"')
    df_ope_ad10=df_ope.query('`Contract Type` == "INTERIM"')
    df_ope_hc=df_ope.query('`Contract Type` != "CONTS" & `Contract Type` != "INTERIM"')
    
    df_func_110a=df_func.query('`Contract Type` == "CONTS"')
    df_func_ad10=df_func.query('`Contract Type` == "INTERIM"')
    df_func_hc=df_func.query('`Contract Type` != "CONTS" & `Contract Type` != "INTERIM"')    
    
    df_ope_110a=df_ope_110a.drop(columns="Contract Type")
    df_ope_ad10=df_ope_ad10.drop(columns="Contract Type")
    df_ope_hc=df_ope_hc.drop(columns="Contract Type")
    
    df_func_110a=df_func_110a.drop(columns="Contract Type")
    df_func_ad10=df_func_ad10.drop(columns="Contract Type")
    df_func_hc=df_func_hc.drop(columns="Contract Type")
    
    ope_top_a110=pd.DataFrame(columns=[service_name, service_code, role, region,'Couple'])
    ope_top_ad10=pd.DataFrame(columns=[service_name, service_code, role, region,'Couple'])
    
    func_top_a110=pd.DataFrame(columns=[service_name, service_code, role, region,'Couple'])
    func_top_ad10=pd.DataFrame(columns=[service_name, service_code, role, region,'Couple'])
      
    df_func_hc=df_func_hc.groupby([service_name,service_code,role,region]).sum().reset_index()
    df_func_110a=df_func_110a.groupby([service_name,service_code,role,region]).sum().reset_index()
    df_func_ad10=df_func_ad10.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    rate_oper_110a=df_ope_110a.groupby([service_name,service_code,role, region])['% Direct'].max().reset_index()
    rate_oper_ad10=df_ope_ad10.groupby([service_name,service_code, role, region])['% Direct'].max().reset_index()
    
    rate_oper_110a['Source_110A']="RDPM"
    rate_oper_ad10['Source_AD10']="RDPM"
    
    df_ope_hc=df_ope_hc.drop(columns='% Direct')
    df_ope_110a=df_ope_110a.drop(columns='% Direct')
    df_ope_ad10=df_ope_ad10.drop(columns='% Direct')
    
    df_ope_hc=df_ope_hc.groupby([service_name,service_code,role,region]).sum().reset_index()
    df_ope_110a=df_ope_110a.groupby([service_name,service_code,role,region]).sum().reset_index()
    df_ope_ad10=df_ope_ad10.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    
    def get_couple(row):
        return f"{row[service_name]}_{row[service_code]}_{row[role]}_{row[region]}"
    
    

    df_workload['Couple'] = df_workload.apply(get_couple, axis=1)
    df_ope_hc['Couple'] = df_ope_hc.apply(get_couple, axis=1)
    df_ope_110a['Couple'] = df_ope_110a.apply(get_couple, axis=1)
    df_ope_ad10['Couple'] = df_ope_ad10.apply(get_couple, axis=1)
    rate_oper_110a['Couple'] = rate_oper_110a.apply(get_couple, axis=1)
    rate_oper_ad10['Couple'] = rate_oper_ad10.apply(get_couple, axis=1)

    unique_couple= set()

    dataframes =[df_workload,df_ope_hc,df_ope_110a,df_ope_ad10]

    for df in dataframes:
        unique_couple.update(df['Couple'])

    dataframes =[df_workload,df_ope_hc,df_ope_110a,df_ope_ad10,ope_top_a110,ope_top_ad10,rate_oper_110a,rate_oper_ad10]

    for df in dataframes:
        for value in unique_couple:
            if value not in df['Couple'].values.tolist():
                elements= value.split('_')
                new_row={service_name: elements[0],service_code:elements[1], role :elements[2], region :elements[3]}
                df.loc[len(df)]=new_row

    df_func_hc['Couple'] = df_func_hc.apply(get_couple, axis=1)
    df_func_110a['Couple'] = df_func_110a.apply(get_couple, axis=1)
    df_func_ad10['Couple'] = df_func_ad10.apply(get_couple, axis=1)

    unique_couple= set()

    dataframes =[df_func_hc,df_func_110a,df_func_ad10]

    for df in dataframes:
        unique_couple.update(df['Couple'])

    dataframes =[df_func_hc,df_func_110a,df_func_ad10,func_top_a110,func_top_ad10]

    for df in dataframes:
        for value in unique_couple:
            if value not in df['Couple'].values.tolist():
                elements= value.split('_')
                new_row={service_name: elements[0],service_code:elements[1], role :elements[2], region :elements[3]}
                df.loc[len(df)]=new_row


    df_workload=df_workload.drop(columns='Couple')  
    df_ope_hc=df_ope_hc.drop(columns='Couple')
    df_ope_110a=df_ope_110a.drop(columns='Couple')
    df_ope_ad10=df_ope_ad10.drop(columns='Couple')
    ope_top_a110=ope_top_a110.drop(columns='Couple')
    ope_top_ad10=ope_top_ad10.drop(columns='Couple')
    rate_oper_110a=rate_oper_110a.drop(columns='Couple')
    rate_oper_ad10=rate_oper_ad10.drop(columns='Couple')
    
    
    df_func_hc=df_func_hc.drop(columns='Couple')
    df_func_110a=df_func_110a.drop(columns='Couple')
    df_func_ad10=df_func_ad10.drop(columns='Couple')
    func_top_a110=func_top_a110.drop(columns='Couple')
    func_top_ad10=func_top_ad10.drop(columns='Couple')
            

    #==============================================================================================================================================================================
    #   PARTIE SIMULATION OPERATIONNELLE
    
    
    #Sentences used in the column "Info" of the simulation tab
    df_workload[info]="In-House Workload - Total FTEs - after PRP & Approved+Not Approved"
    df_ope_hc[info]="Registered Headcount - FTEs"
    df_ope_110a[info]="110A - Committed - FTEs"
    df_ope_ad10[info]="AD10 - Committed - FTEs"
    ope_top_a110[info]="110A TOPs"
    ope_top_ad10[info]="AD10 TOPs"

    df_simu=pd.concat([df_workload,df_ope_hc,df_ope_110a,df_ope_ad10,ope_top_a110,ope_top_ad10],ignore_index=True)
    df_simu=df_simu.fillna(value=0)
    df_simu=df_simu.replace(to_replace='(blank)',value=' ')
    df_simu=df_simu.round(1)


    #########################################################################################################

    df_simu_copy=df_simu.copy()
    df_simu_copy[service_name]="CSO+EGDS"
    df_simu_copy[service_code]="CSO+EGDS"

    all_role_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()


    df_simu_copy[role]="ALL"
    all_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    all_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    

    df_simu_copy=df_simu.copy()
    df_simu_copy[service_name]="CSO+EGDS"
    df_simu_copy[service_code]="CSO+EGDS"
    df_simu_copy[region]="ALL"

    all_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()
    
    #########################################################################################################
    df_simu_copy=df_simu.copy()
    df_simu_copy= df_simu_copy[~df_simu_copy[service_code].str.contains("BS")]
    df_simu_copy[service_name]="CSO"
    df_simu_copy[service_code]="CSO"
    
    cso_all_role_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()


    df_simu_copy[role]="ALL"
    cso_all_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    cso_all_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    

    df_simu_copy=df_simu.copy()
    df_simu_copy= df_simu_copy[~df_simu_copy[service_code].str.contains("BS")]
    df_simu_copy[service_name]="CSO"
    df_simu_copy[service_code]="CSO"
    df_simu_copy[region]="ALL"

    cso_all_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()
    
    ##########################################################################
    # TODO: 2
    
    
    
    bs10= df_simu[df_simu[service_code].str.contains("BS10")]
    bs10[service_code]="BS10"
    bs10[service_name]="Evidence Generation and Decision Science"
    bs10[role]="ALL"

    bs10_all_region=bs10.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    bs10[region]="ALL"
    bs10_all_all=bs10.groupby([service_name,service_code,role,region,info]).sum().reset_index()    
    

    
    db13= df_simu[df_simu[service_code].str.contains("DB13")]
    db13[service_code]="DB13"
    db13[service_name]="Operational Medical Dvpt & Clinical Doc"
    db13[role]="ALL"

    db13_all_region=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    db13[region]="ALL"
    db13_all_all=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    trial_ops= df_simu[df_simu[service_code].str.contains("DB15")] ## was empty -> filter was not functionning
    trial_ops[service_code]="DB15"
    trial_ops[service_name]="Clinical Data & AI Processing"
    trial_ops[role]="ALL"

    trial_ops_all_region=trial_ops.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    trial_ops[region]="ALL"
    trial_ops_all_all=trial_ops.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    csu= df_simu[df_simu[service_code].str.contains("DB17")]
    csu[service_code]="Total"
    csu[service_name]="CSUs"
    csu[role]="ALL"

    csu_all_region=csu.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    csu[region]="ALL"
    csu_all_all=csu.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    corpo= df_simu[~df_simu[service_code].str.contains("DB17")]
    corpo= corpo[~corpo[service_code].str.contains("BS")]
    corpo[service_code]="Total"
    corpo[service_name]="Corporate Centers"
    corpo[role]="ALL"

    corpo_all_region=corpo.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    corpo[region]="ALL"

    corpo_all_all=corpo.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy=df_simu.copy()
    df_simu_copy[role]="ALL"

    dpt_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    dpt_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy=df_simu.copy()
    df_simu_copy[region]="ALL"
    dpt_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu=pd.concat([df_simu,all_role_region],ignore_index=True)

    df_simu=pd.concat([df_simu,all_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,all_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,all_role_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,cso_all_role_region],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_role_all],ignore_index=True)

    df_simu=pd.concat([df_simu,csu_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,csu_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,corpo_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,corpo_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_role_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,trial_ops_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,trial_ops_all_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db13_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db13_all_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,bs10_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,bs10_all_all],ignore_index=True)

    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order'] = df_simu[service_name].apply(
        lambda x: 0 if x == 'CSO+EGDS' else 
                (1 if x == 'CSO' else 
                (2 if x == 'CSUs' else 
                    (3 if x == 'Corporate Centers' else 4)))
    )

    # Trier d'abord selon la colonne 'custom_order', puis selon 'service_code', 'region', et 'role'
    df_simu = df_simu.sort_values(by=['custom_order', service_code, region, role])

    # Supprimer la colonne temporaire de tri si elle n'est plus nécessaire
    df_simu = df_simu.drop(columns=['custom_order'])


    df_filtered = df_simu.query('Info != "In-House Workload - Total FTEs - after PRP & Approved+Not Approved"')
    df_total=df_filtered.groupby([service_name, service_code, role, region], as_index=False).sum()
    df_total[info] = 'Total In-House Workforce - FTEs'
    df_simu=pd.concat([df_simu,df_total],ignore_index=True)

    df_total_tops=df_total.copy()
    df_total_tops[info]='Total In-House Workforce - FTEs with TOPs'
    df_simu=pd.concat([df_simu,df_total_tops],ignore_index=True)

    
    def calculate_gap(group):
        if len(group) == 2:
            # Vérifier que les deux lignes ont des valeurs différentes dans la colonne "Info"
            if group[info].nunique() == 2:
                # Sélectionner les colonnes numériques pour la soustraction
                numeric_columns = group.select_dtypes(include='number').columns
                # Soustraire la deuxième ligne de la première pour les colonnes numériques
                group[numeric_columns] = group.iloc[1][numeric_columns] - group.iloc[0][numeric_columns]
        # Retourner le groupe tel quel s'il ne répond pas aux conditions
        return group

    df_filtered= df_simu.query('Info == "In-House Workload - Total FTEs - after PRP & Approved+Not Approved" | Info == "Total In-House Workforce - FTEs" ')
    df_gap=df_filtered.groupby([service_name, service_code, role, region], as_index=False).apply(calculate_gap)

    
    df_gap[info] = 'Gap In-House - FTEs (Workforce vs Workload)'
    df_gap = df_gap.drop_duplicates()
    df_simu=pd.concat([df_simu,df_gap],ignore_index=True)



    df_gap_tops=df_gap.copy()
    df_gap_tops[info]='Gap In-House - FTEs  (Workforce vs Workload) with TOPS'
    df_simu=pd.concat([df_simu,df_gap_tops],ignore_index=True)


    df_filtered= df_simu.query('Info == "110A - Committed - FTEs" | Info == "AD10 - Committed - FTEs" ')
    df_tot=df_filtered.groupby([service_name, service_code, role, region], as_index=False).sum() 


    def calculate_flexibility(group):
        # Vérifier que le groupe contient exactement deux éléments distincts dans "Info"
        if len(group) == 2 and group['Info'].nunique() == 2:
            # Sélectionner les colonnes numériques pour la soustraction
            numeric_columns = group.select_dtypes(include='number').columns.tolist()
            
            # Créer une nouvelle ligne pour les résultats
            result_row = group.iloc[0].copy()  # Copier la première ligne pour conserver les autres colonnes
            
            # Vérifier si la valeur dans la première ligne est différente de zéro pour chaque colonne numérique
            for col in numeric_columns:
                if group.iloc[0][col] != 0:
                    result_row[col] = (group.iloc[1][col] / group.iloc[0][col]) * 100
                else:
                    result_row[col] = 0  # Mettre None ou 0 selon le besoin
            
            # Assigner le résultat à une nouvelle ligne plutôt que de modifier le groupe entier
            return result_row



    df_filtered= df_simu.query('Info == "Total In-House Workforce - FTEs"')
    df_filtered=pd.concat([df_filtered,df_tot],ignore_index=True)
    df_flex = df_filtered.groupby([service_name, service_code, role, region], as_index=False).apply(calculate_flexibility).reset_index(drop=True)
    df_flex[info]= "Flexibility %"
    df_flex = df_flex.drop_duplicates()
    df_flex=df_flex.round(1)
    
    def calculate_coverage(group):
        if len(group) == 2 and group['Info'].nunique() == 2:
            # Sélectionner les colonnes numériques pour la soustraction
            numeric_columns = group.select_dtypes(include='number').columns.tolist()
        # Créer une nouvelle ligne pour les résultats
            result_row = group.iloc[0].copy()  # Copier la première ligne pour conserver les autres colonnes
            
            # Vérifier si la valeur dans la première ligne est différente de zéro pour chaque colonne numérique
            for col in numeric_columns:
                if group.iloc[0][col] != 0:
                    result_row[col] = (group.iloc[1][col] / group.iloc[0][col]) * 100
                else:
                    result_row[col] = 0  # Mettre None ou 0 selon le besoin
            
            # Assigner le résultat à une nouvelle ligne plutôt que de modifier le groupe entier
            return result_row

    df_filtered= df_simu.query('Info == "In-House Workload - Total FTEs - after PRP & Approved+Not Approved" | Info == "Total In-House Workforce - FTEs" ')
    df_cov=df_filtered.groupby([service_name, service_code, role, region], as_index=False).apply(calculate_coverage)

    
    df_cov[info] = 'In House Coverage %'
    df_cov = df_cov.drop_duplicates()
    df_cov=df_cov.round(1)


    df_simu=df_simu.round(1)


    df_simu=pd.concat([df_simu,df_flex],ignore_index=True)
    df_simu=pd.concat([df_simu,df_cov],ignore_index=True)

    df_flex_tops=df_flex.copy()
    df_flex_tops[info] = 'Flexibility % with TOPS'

    df_cov_tops=df_cov.copy()
    df_cov_tops[info] = 'In House Coverage % with TOPS'

    df_simu=pd.concat([df_simu,df_flex_tops],ignore_index=True)
    df_simu=pd.concat([df_simu,df_cov_tops],ignore_index=True)

    def calculate_diff(group):
        if len(group) == 2:
            # Vérifier que les deux lignes ont des valeurs différentes dans la colonne "Info"
            if group["Info"].nunique() == 2:
                # Sélectionner les colonnes numériques pour la soustraction
                numeric_columns = group.select_dtypes(include='number').columns
                # Soustraire la deuxième ligne de la première pour les colonnes numériques
                group[numeric_columns] = group.iloc[1][numeric_columns] - group.iloc[0][numeric_columns]
        # Retourner le groupe tel quel s'il ne répond pas aux conditions
        return group


    df_filtered= df_simu.query('Info == "Registered Headcount - FTEs" | Info == "Total In-House Workforce - FTEs"')
    df_diff=df_filtered.groupby([service_name, service_code, role, region], as_index=False).apply(calculate_diff)

    df_diff["Info"]='Total Insourcing - FTEs'
    df_diff=df_diff.drop_duplicates()
    df_diff=df_diff.round(1)
    
    df_diff_tops=df_diff.copy()
    df_diff_tops["Info"]='Total Insourcing - FTEs with TOPs'
    df_simu=pd.concat([df_simu,df_diff],ignore_index=True)
    df_simu=pd.concat([df_simu,df_diff_tops],ignore_index=True)


    df_simu[info]=pd.Categorical(df_simu[info],ordered=True,
                                    categories=["In-House Workload - Total FTEs - after PRP & Approved+Not Approved","Registered Headcount - FTEs","110A - Committed - FTEs",
                                            "AD10 - Committed - FTEs",'Total In-House Workforce - FTEs','Total Insourcing - FTEs','Gap In-House - FTEs (Workforce vs Workload)','Flexibility %',
                                            "In House Coverage %",'110A TOPs','AD10 TOPs','Total In-House Workforce - FTEs with TOPs','Total Insourcing - FTEs with TOPs','Gap In-House - FTEs  (Workforce vs Workload) with TOPS',
                                            'Flexibility % with TOPS','In House Coverage % with TOPS'])
    
    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order'] = df_simu[service_name].apply(
        lambda x: 0 if x == 'CSO+EGDS' else 
                (1 if x == 'CSO' else 
                (2 if x == 'CSUs' else 
                    (3 if x == 'Corporate Centers' else 4)))
    )
    
    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order_role'] = df_simu[role].apply(
        lambda x: 0 if x == 'ALL' else 1
    )

    # Trier d'abord selon la colonne 'custom_order', puis selon 'service_code', 'region', et 'role'
    df_simu = df_simu.sort_values(by=['custom_order','custom_order_role', service_code, region, role,info])

    # Supprimer la colonne temporaire de tri si elle n'est plus nécessaire
    df_simu = df_simu.drop(columns=['custom_order'])
    
    df_simu = df_simu.drop(columns=['custom_order_role'])
    df_simu=df_simu.round(1)
    if checked:
        old_tops_ope.columns=df_simu.columns
        columns=[col for col in df_simu.columns if col not in [service_code, service_name,role,region,info]]
        df_simu=pd.merge(df_simu, old_tops_ope, on=[service_code, service_name,role,region,info], how='left', suffixes=('', '_old'))
        for col in columns:
            df_simu[col] = df_simu[col + '_old'].combine_first(df_simu[col])
            df_simu.drop(columns=[col + '_old'], inplace=True)
    
    df_simu=df_simu.dropna(subset=[service_code,service_name,role,region])
    df_simu.to_csv(os.path.join(base_path, f"simulation_ope - {date}.csv"),index=False,sep=';')

    simu_ope=df_simu

    
    df_workload=df_workload.drop(columns=info)
    df_ope_hc=df_ope_hc.drop(columns=info)
    df_ope_110a=df_ope_110a.drop(columns=info)
    df_ope_ad10=df_ope_ad10.drop(columns=info)

    df=df_workload.merge(df_ope_hc, on=[service_name, role,service_code,region],suffixes=('_WL','_HC'))
    df=df.merge(df_ope_110a, on=[service_name, role,service_code,region],suffixes=('_HC','_110A'))
    df=df.merge(df_ope_ad10, on=[service_name, role,service_code,region],suffixes=('_110A','_AD10'))


    df=df.fillna(value=0)
    df=df.replace(to_replace='(blank)',value=' ')

    years_list=extract_unique_years(df.columns.tolist())

    global year
    global next_year
    global next_next_year

    year=int(years_list[0])
    next_year=int(years_list[1])
    next_next_year=int(years_list[2])

    df[f"{str(year)} {Q1_TOPS_110A}"]=0
    df[f"{str(year)} {Q2_TOPS_110A}"]=0
    df[f"{str(year)} {Q3_TOPS_110A}"]=0
    df[f"{str(year)} {Q4_TOPS_110A}"]=0

    df[f"{str(year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(year)} {Q4_TOPS_AD10}"]=0

    df[f"{str(next_year)} {Q1_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q2_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q3_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q4_TOPS_110A}"]=0

    df[f"{str(next_year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q4_TOPS_AD10}"]=0

    df[f"{str(next_next_year)} {Q1_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q2_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q3_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q4_TOPS_110A}"]=0

    df[f"{str(next_next_year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q4_TOPS_AD10}"]=0
    
    rate=rate_oper_110a.merge(rate_oper_ad10, on=[service_name, role,service_code,region],suffixes=('_110A','_AD10'))
    rate=rate.replace(to_replace='(blank)',value=' ')

    
    global initial_rate
    
    def convert_str_to_int(x):
        if isinstance(x, str):  # Vérifier si x est une chaîne de caractères
            try:
                return int(x)  # Tenter de convertir en entier
            except ValueError:
                return x  # Si la conversion échoue, retourner l'original
        return x  # Si x n'est pas une chaîne, le retourner tel quel
    
    
    if isinstance(initial_rate, pd.DataFrame):
        rate_combined=initial_rate.merge(rate,on=[service_name,service_code,role,region], suffixes=('','_new'),how="outer")
        for col in ['% Direct_110A','% Direct_AD10','Source_110A','Source_AD10']:
            mask = ~rate_combined[f'{col}_new'].isna()  # Créer un masque où les nouvelles valeurs ne sont pas NaN
            rate_combined.loc[mask, col] = rate_combined.loc[mask, f'{col}_new']  # Appliquer les nouvelles valeurs
            
        rate_combined=rate_combined.drop(columns="% Direct_110A_new")
        rate_combined=rate_combined.drop(columns="% Direct_AD10_new")
        rate_combined=rate_combined.drop(columns="Source_110A_new")
        rate_combined=rate_combined.drop(columns="Source_AD10_new")
        rate_combined=rate_combined.sort_values(by=[service_code,region,role])
        rate_combined["Missing"]="False"
        rate_combined['% Direct_110A'] = rate_combined['% Direct_110A'].apply(convert_str_to_int)
        rate_combined['% Direct_AD10'] = rate_combined['% Direct_AD10'].apply(convert_str_to_int)
        
        rate_combined.to_csv(os.path.join(base_path, "operational_rate.csv"),index=False,sep=';')
        initial_rate=rate_combined
        
    else:
        rate=rate.sort_values(by=[service_code,region,role])
        rate["Missing"]="False"
        rate['% Direct_110A'] = rate['% Direct_110A'].apply(convert_str_to_int)
        rate['% Direct_AD10'] = rate['% Direct_AD10'].apply(convert_str_to_int)
        rate.to_csv(os.path.join(base_path, "operational_rate.csv"),index=False,sep=';')
        initial_rate=rate
    
    df.to_csv(os.path.join(base_path, f"dashboard_ope - {date}.csv"),index=False,sep=';')
    global dashboard_ope
    dashboard_ope=df
    
    #==============================================================================================================================================================================
    #PARTIE ROLE FONCTIONNEL
    

    #Sentences used in the column "Info" of the simulation tab
    df_func_hc[info]="Registered Headcount - Heads"
    df_func_110a[info]="110A - Committed - Heads"
    df_func_ad10[info]="AD10 - Committed - Heads"
    func_top_a110[info]="110A TOPs"
    func_top_ad10[info]="AD10 TOPs"

    df_simu=pd.concat([df_func_hc,df_func_110a,df_func_ad10,func_top_a110,func_top_ad10],ignore_index=True)
    df_simu=df_simu.fillna(value=0)
    df_simu=df_simu.replace(to_replace='(blank)',value=' ')
    df_simu=df_simu.round(1)

    df_simu_copy=df_simu.copy()
    df_simu_copy[service_name]="CSO+EGDS"
    df_simu_copy[service_code]="CSO+EGDS"
    
    all_role_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()


    df_simu_copy[role]="ALL"
    all_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    all_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    

    df_simu_copy=df_simu.copy()
    df_simu_copy[service_name]="CSO+EGDS"
    df_simu_copy[service_code]="CSO+EGDS"
    df_simu_copy[region]="ALL"

    all_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()
    

    
    df_simu_copy=df_simu.copy()
    df_simu_copy= df_simu_copy[~df_simu_copy[service_code].str.contains("BS")]
    df_simu_copy[service_name]="CSO"
    df_simu_copy[service_code]="CSO"
    
    cso_all_role_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()


    df_simu_copy[role]="ALL"
    cso_all_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    cso_all_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    

    df_simu_copy=df_simu.copy()
    df_simu_copy= df_simu_copy[~df_simu_copy[service_code].str.contains("BS")]
    df_simu_copy[service_name]="CSO"
    df_simu_copy[service_code]="CSO"
    df_simu_copy[region]="ALL"

    cso_all_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()
    
    #########################################################################################################    
    # TODO: 3
    
    db10= df_simu[df_simu[service_code].str.contains("DB1000|DB1001")]
    db10[service_code]="DB10"
    db10[service_name]="Management Office"
    db10[role]="ALL"

    db10_all_region=db10.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    db10[region]="ALL"
    db10_all_all=db10.groupby([service_name,service_code,role,region,info]).sum().reset_index()
    
    bs10= df_simu[df_simu[service_code].str.contains("BS10")]
    bs10[service_code]="BS10"
    bs10[service_name]="Evidence Generation and Decision Science"
    bs10[role]="ALL"

    bs10_all_region=bs10.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    bs10[region]="ALL"
    bs10_all_all=bs10.groupby([service_name,service_code,role,region,info]).sum().reset_index()   
    
    
    db13= df_simu[df_simu[service_code].str.contains("DB13")]
    db13[service_code]="DB13"
    db13[service_name]="Operational Medical Dvpt & Clinical Doc"
    db13[role]="ALL"

    db13_all_region=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    db13[region]="ALL"
    db13_all_all=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    trial_ops= df_simu[df_simu[service_code].str.contains("DB15")]
    trial_ops[service_code]="DB15"
    trial_ops[service_name]="Clinical Data & AI Processing"
    trial_ops[role]="ALL"

    trial_ops_all_region=trial_ops.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    trial_ops[region]="ALL"
    trial_ops_all_all=trial_ops.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    csu= df_simu[df_simu[service_code].str.contains("DB17")]
    csu[service_code]="Total"
    csu[service_name]="CSUs"
    csu[role]="ALL"

    csu_all_region=csu.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    csu[region]="ALL"
    csu_all_all=csu.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    corpo= df_simu[~df_simu[service_code].str.contains("DB17")]
    corpo= corpo[~corpo[service_code].str.contains("BS")]
    corpo[service_code]="Total"
    corpo[service_name]="Corporate Centers"
    corpo[role]="ALL"

    corpo_all_region=corpo.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    corpo[region]="ALL"

    corpo_all_all=corpo.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy=df_simu.copy()
    df_simu_copy[role]="ALL"

    dpt_all_region=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy[region]="ALL"
    dpt_all_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()

    df_simu_copy=df_simu.copy()
    df_simu_copy[region]="ALL"
    dpt_role_all=df_simu_copy.groupby([service_name,service_code,role,region,info]).sum().reset_index()


    df_simu=pd.concat([df_simu,all_role_region],ignore_index=True)

    df_simu=pd.concat([df_simu,all_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,all_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,all_role_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,cso_all_role_region],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,cso_all_role_all],ignore_index=True)    

    df_simu=pd.concat([df_simu,csu_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,csu_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,corpo_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,corpo_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_all_region],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_all_all],ignore_index=True)

    df_simu=pd.concat([df_simu,dpt_role_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,trial_ops_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,trial_ops_all_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db13_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db13_all_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,bs10_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,bs10_all_all],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db10_all_region],ignore_index=True)
    
    df_simu=pd.concat([df_simu,db10_all_all],ignore_index=True)

    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order'] = df_simu[service_name].apply(
        lambda x: 0 if x == 'CSO+EGDS' else 
                (1 if x == 'CSO' else 
                (2 if x == 'CSUs' else 
                    (3 if x == 'Corporate Centers' else 4)))
    )

    # Trier d'abord selon la colonne 'custom_order', puis selon 'service_code', 'region', et 'role'
    df_simu = df_simu.sort_values(by=['custom_order', service_code, region, role])

    # Supprimer la colonne temporaire de tri si elle n'est plus nécessaire
    df_simu = df_simu.drop(columns=['custom_order'])


    df_total=df_simu.groupby([service_name, service_code, role, region], as_index=False).sum()
    df_total[info] = 'Total In-House Workforce - Heads'
    df_simu=pd.concat([df_simu,df_total],ignore_index=True)

    df_total_tops=df_total.copy()
    df_total_tops[info]='Total In-House Workforce - Heads with TOPs'
    df_simu=pd.concat([df_simu,df_total_tops],ignore_index=True)

    df_simu=df_simu.round(1)
    
    def calculate_diff(group):
        if len(group) == 2:
            # Vérifier que les deux lignes ont des valeurs différentes dans la colonne "Info"
            if group["Info"].nunique() == 2:
                # Sélectionner les colonnes numériques pour la soustraction
                numeric_columns = group.select_dtypes(include='number').columns
                # Soustraire la deuxième ligne de la première pour les colonnes numériques
                group[numeric_columns] = group.iloc[1][numeric_columns] - group.iloc[0][numeric_columns]
        # Retourner le groupe tel quel s'il ne répond pas aux conditions
        return group


    df_filtered= df_simu.query('Info == "Registered Headcount - Heads" | Info == "Total In-House Workforce - Heads"')
    df_diff=df_filtered.groupby([service_name, service_code, role, region], as_index=False).apply(calculate_diff)

    df_diff["Info"]='Total Insourcing - Heads'
    df_diff=df_diff.drop_duplicates()
    df_diff=df_diff.round(1)
    
    df_diff_tops=df_diff.copy()
    df_diff_tops["Info"]='Total Insourcing - Heads with TOPs'
    df_simu=pd.concat([df_simu,df_diff],ignore_index=True)
    df_simu=pd.concat([df_simu,df_diff_tops],ignore_index=True)    
    
    

    df_simu[info]=pd.Categorical(df_simu[info],ordered=True,
                                   categories=['Total In-House Workforce - Heads','Total Insourcing - Heads',"Registered Headcount - Heads","110A - Committed - Heads",
                                                "AD10 - Committed - Heads",'110A TOPs','AD10 TOPs','Total In-House Workforce - Heads with TOPs','Total Insourcing - Heads with TOPs'])
    
    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order'] = df_simu[service_name].apply(
        lambda x: 0 if x == 'CSO+EGDS' else 
                (1 if x == 'CSO' else 
                (2 if x == 'CSUs' else 
                    (3 if x == 'Corporate Centers' else 4)))
    )

    # Créer une colonne temporaire pour le tri personnalisé
    df_simu['custom_order_role'] = df_simu[role].apply(
        lambda x: 0 if x == 'ALL' else 1
    )

    # Trier d'abord selon la colonne 'custom_order', puis selon 'service_code', 'region', et 'role'
    df_simu = df_simu.sort_values(by=['custom_order','custom_order_role', service_code, region, role,info])

    # Supprimer la colonne temporaire de tri si elle n'est plus nécessaire
    df_simu = df_simu.drop(columns=['custom_order'])
    
    df_simu = df_simu.drop(columns=['custom_order_role'])
    df_simu=df_simu.round(1)
    if checked:

        old_tops_func.columns=df_simu.columns
        columns=[col for col in df_simu.columns if col not in [service_code, service_name,role,region,info]]
        df_simu=pd.merge(df_simu, old_tops_func, on=[service_code, service_name,role,region,info], how='left', suffixes=('', '_old'))
        for col in columns:
            df_simu[col] = df_simu[col + '_old'].combine_first(df_simu[col])
            df_simu.drop(columns=[col + '_old'], inplace=True)
    

    df_simu.to_csv(os.path.join(base_path, f"simulation_func - {date}.csv"),index=False,sep=';')

    simu_func=df_simu




    
    df_func_hc=df_func_hc.drop(columns=info)
    df_func_110a=df_func_110a.drop(columns=info)
    df_func_ad10=df_func_ad10.drop(columns=info)
    
    
    
    suffix_110a = "_110A"
    df_func_110a = df_func_110a.rename(columns=lambda x: x + suffix_110a if x not in [service_name, role, service_code, region] else x)
    
    df=df_func_hc.merge(df_func_ad10, on=[service_name, role,service_code,region],suffixes=('_HC','_AD10'))
    df=df.merge(df_func_110a, on=[service_name, role,service_code,region])



    df=df.fillna(value=0)
    df=df.replace(to_replace='(blank)',value=' ')


    df[f"{str(year)} {Q1_TOPS_110A}"]=0
    df[f"{str(year)} {Q2_TOPS_110A}"]=0
    df[f"{str(year)} {Q3_TOPS_110A}"]=0
    df[f"{str(year)} {Q4_TOPS_110A}"]=0

    df[f"{str(year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(year)} {Q4_TOPS_AD10}"]=0

    df[f"{str(next_year)} {Q1_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q2_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q3_TOPS_110A}"]=0
    df[f"{str(next_year)} {Q4_TOPS_110A}"]=0

    df[f"{str(next_year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(next_year)} {Q4_TOPS_AD10}"]=0

    df[f"{str(next_next_year)} {Q1_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q2_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q3_TOPS_110A}"]=0
    df[f"{str(next_next_year)} {Q4_TOPS_110A}"]=0

    df[f"{str(next_next_year)} {Q1_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q2_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q3_TOPS_AD10}"]=0
    df[f"{str(next_next_year)} {Q4_TOPS_AD10}"]=0
    
    
    
    

    df.to_csv(os.path.join(base_path, f"dashboard_func - {date}.csv"), index=False,sep=';')
    global dashboard_func
    dashboard_func=df
    global tops_export
    tops_export=prepare_Tops(simu_ope,simu_func,initial_rate)
    
    files_to_keep=[f"dashboard_func - {date}.csv",f"simulation_func - {date}.csv",f"dashboard_ope - {date}.csv",f"simulation_ope - {date}.csv","operational_rate.csv",f"CSO_Tops - {date}.csv"]
     
    for file in os.listdir(base_path):
        path= os.path.join(base_path,file) 
        
        if file not in files_to_keep and os.path.isfile(path):
            
            os.remove(path)



def get_dashboard_functional(year):
    """
    Renvoie les données sous la forme d'un dashboard pour les pages dashboard

    Args:
        df (dataframe): Dataframe contenant les données
        year (int): Année des données à garder
        year_to_drop (int): Année des données à se débarasser
        year_to_drop_two (int): Année des données à se débarasser

    Returns:
        df (dataframe): Dataframe contenant les données traitées pour le dataframe
        columnDefs(Ag-Grid): définition des différentes colonnes composant l'Ag-Grid
        defaultColDef (Ag-Grid): paramètres globaux des colonnes de l'Ag-Grid
    """

    #Transform the year from the format yyyy to the format yy
    year_yy= year % 100

    #Variable used to name the different columns
    H1 = f"1H {year_yy}"
    H2 = f"2H {year_yy}"
    AVG = f"Avg {year_yy}"
    Q1 = f"1Q {year_yy}"
    Q2 = f"2Q {year_yy}"
    Q3 = f"3Q {year_yy}"
    Q4 = f"4Q {year_yy}"


    # Definitions and parameters for each column in the ag grid. Documentation available here: https://www.ag-grid.com/archive/29.3.5/react-data-grid/column-properties/
    columnDefs= [
        {
            "headerName": "Characteristics",
            "children":[
                {
                    "headerName":service_code,
                    "field": service_code,                  
                    "width":100,
                    "cellStyle":{"styleConditions":[{"condition": f"params.data.{role} != 'ALL'", "style":{"color":"rgb(174,174,174)"}}]}, 
                    'floatingFilter': True,
                    "filter": True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    
                },
                {
                    "headerName":service_name,
                    "field":service_name,  
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {"styleConditions":[{"condition": f"params.node.rowPinned === 'bottom'", "style":{"textDecoration":"underline",'borderLeft': '1px solid lightgrey'}}],"defaultStyle": {'borderLeft': '1px solid lightgrey'}}, 
                    "tooltipField": service_name,
                },
                {
                    "headerName":role,
                    "field":role,     
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":20,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {"styleConditions":[{"condition": f"params.node.rowPinned === 'bottom'", "style":{"color":"transparent",'borderLeft': '1px solid lightgrey'}}],"defaultStyle": {'borderLeft': '1px solid lightgrey'}}, 
                },
                {
                    "headerName":region,
                    "field":region,    
                    "width":100,
                    'floatingFilter': True,
                    "filter":True,
                    "filterParams":{"maxNumConditions":10,"defaultJoinOperator":"OR",'buttons': ['reset']},
                    "valueFormatter": {"function": "params.value"},
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                
            ]
        },
        {
            "headerName": "Headcounts (Heads)",
            
            
            "children": [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field" : H1_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                     
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field" : H2_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                     
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field" : AVG_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                     
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field": Q1_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field": Q2_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field": Q3_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field": Q4_HC,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
            ]
        },
        {
            "headerName": "Insourcing Contractors (Heads)",

            "children":[
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field" : H1_CONT,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field" : H2_CONT,                 
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field" : AVG_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                "headerName": "Details",
                "columnGroupShow": "open",
                "children":[
                    {
                    "headerName": Q1,
                    "columnGroupShow": "closed",
                    "field" : Q1_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '3px solid black'}, 
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "closed",
                    "field" : Q2_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "closed",
                    "field" : Q3_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "closed",
                    "field" : Q4_CONT,
                    "filter": "agNumberColumnFilter",
                    "width":77,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                },
                    {
                "headerName": "110A (Heads)",
                "columnGroupShow": "open",
                
                
                "children": [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field" : H1_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                         
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field" : H2_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                         
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field" : AVG_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                         
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field": Q1_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                        
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field": Q2_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field": Q3_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field": Q4_110AC,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                ]
                },
                {
                "headerName": "AD10 (Heads)",
                "columnGroupShow": "open",
                
                
                "children": [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field" : H1_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                         
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field" : H2_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                         
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field" : AVG_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                         
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field": Q1_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                        
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field": Q2_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field": Q3_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field": Q4_AD10C,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                        
                    },
                ]
                },
                {
                "headerName":"110A+AD10 Top Adjustements (Heads)",
                "columnGroupShow":"open",
                "children":
                [
                    {
                        "headerName": H1,
                        "columnGroupShow": "closed",
                        "field": H1_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                    },
                    {
                        "headerName": H2,
                        "columnGroupShow": "closed",
                        "field": H2_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                    },
                    {
                        "headerName": AVG,
                        "columnGroupShow": "closed",
                        "field": AVG_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                    },
                    {
                        "headerName": Q1,
                        "columnGroupShow": "open",
                        "field":Q1_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '3px solid black'},
                        
                    },
                    {
                        "headerName": Q2,
                        "columnGroupShow": "open",
                        "field":Q2_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                    },
                    {
                        "headerName": Q3,
                        "columnGroupShow": "open",
                        "field":Q3_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                    },
                    {
                        "headerName": Q4,
                        "columnGroupShow": "open",
                        "field":Q4_TOPS,
                        "width":75,
                        "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                        
                    },
                ]
                },
                ]
                },        
                
            ]
        },       
        {
            "headerName":"In-House Workforce (Heads)",
            "children":
            [
                {
                    "headerName": H1,
                    "columnGroupShow": "closed",
                    "field":H1_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                        
                },
                {
                    "headerName": H2,
                    "columnGroupShow": "closed",
                    "field":H2_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": AVG,
                    "columnGroupShow": "closed",
                    "field":AVG_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey','borderRight': '2px solid black'}, 
                    
                    
                },
                {
                    "headerName": Q1,
                    "columnGroupShow": "open",
                    "field":Q1_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '3px solid black'},
                    
                    
                },
                {
                    "headerName": Q2,
                    "columnGroupShow": "open",
                    "field":Q2_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q3,
                    "columnGroupShow": "open",
                    "field":Q3_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey'}, 
                    
                    
                },
                {
                    "headerName": Q4,
                    "columnGroupShow": "open",
                    "field":Q4_WF,
                    "width":75,
                    "cellStyle": {'borderLeft': '1px solid lightgrey','borderRight': '2px solid black'}, 
                    
                    
                },
            ]
        },  
    ]


    defaultColDef = {"resizable": True, "filter": False,"wrapHeaderText": True,"suppressMovable": True, 
                     "valueFormatter": {"function": "Math.round(params.value)"},"tooltipComponent": "CustomTooltip"}
    
    
    
    
    # A modifier pour trouver un style de couleur pratique pour Gemma. Champs éditables à mettre en évidence
    getRowStyle = {
        "styleConditions": [
        {
            "condition": "params.data['Service Code'] ==='Total Corporate'",
            "style": {"backgroundColor": "rgba(35,0,76,0.9)","color":"white"},
        },
        {
            "condition": "params.data['Service Code'] ==='Total CSUs'",
            "style": {"backgroundColor": "rgba(35,0,76,0.9)","color":"white"},
        },
        {
            "condition": "params.data['Service Code'] ==='Total CSO'",
            "style": {"backgroundColor": "rgba(35,0,76,1)","color":"white"},
        },
        {
            "condition": "params.data['Role'] ==='ALL' && params.data['Region'] !='ALL' && !params.data['Service Code'].includes('17')",
            "style": {"backgroundColor": "rgba(35,0,76,0.5)","color":"white"},
        },
        {
            "condition": "params.data['Role'] ==='ALL' && params.data['Region'] !='ALL' && params.data['Service Code'].includes('17')",
            "style": {"backgroundColor": "rgba(35,0,76,0.5)","color":"white"},
        },
        {
            "condition": "params.data['Role'] ==='ALL' && params.data['Region'] ==='ALL' && !params.data['Service Code'].includes('17')",
            "style": {"backgroundColor": "rgba(35,0,76,0.75)","color":"white"},
        },
        {
            "condition": "params.data['Role'] ==='ALL' && params.data['Region'] ==='ALL' && params.data['Service Code'].includes('17')",
            "style": {"backgroundColor": "rgba(35,0,76,0.75)","color":"white"},
        },
        {
            "condition": "params.node.rowPinned ==='bottom'",
            "style": {"backgroundColor": "rgba(35,0,76,0.75)","color":"white"},
        },
        
        
    ],
    }

    # df.info(memory_usage='deep')
    return columnDefs, defaultColDef,getRowStyle


def get_dataframe_functional(df,df_simu_func,year,year_to_drop,year_to_drop_two):
    """
    Renvoie les données sous la forme d'un dashboard pour les pages dashboard

    Args:
        df (dataframe): Dataframe contenant les données
        year (int): Année des données à garder
        year_to_drop (int): Année des données à se débarasser
        year_to_drop_two (int): Année des données à se débarasser

    Returns:
        df (dataframe): Dataframe contenant les données traitées pour le dataframe
        columnDefs(Ag-Grid): définition des différentes colonnes composant l'Ag-Grid
        defaultColDef (Ag-Grid): paramètres globaux des colonnes de l'Ag-Grid
    """

    #Drop the data from other year
    col_to_drop=df.filter(like=str(year_to_drop)).columns
    df=df.drop(columns=col_to_drop)

    col_to_drop=df.filter(like=str(year_to_drop_two)).columns
    df=df.drop(columns=col_to_drop)
    

    

    df=df.rename(columns={f'{str(year)} Q1_HC' : Q1_HC, f'{str(year)} Q2_HC' : Q2_HC, f'{str(year)} Q3_HC' : Q3_HC, f'{str(year)} Q4_HC' : Q4_HC,
                       f'{str(year)} Q1_110A' : Q1_110AC, f'{str(year)} Q2_110A' : Q2_110AC, f'{str(year)} Q3_110A' : Q3_110AC, f'{str(year)} Q4_110A' : Q4_110AC,
                       f'{str(year)} Q1_AD10' : Q1_AD10C, f'{str(year)} Q2_AD10' : Q2_AD10C, f'{str(year)} Q3_AD10' : Q3_AD10C, f'{str(year)} Q4_AD10' : Q4_AD10C,
                       f"{str(year)} 1Q_Tops_110A" : Q1_TOPS_110A, f"{str(year)} 2Q_Tops_110A" : Q2_TOPS_110A, f"{str(year)} 3Q_Tops_110A" : Q3_TOPS_110A, f"{str(year)} 4Q_Tops_110A" : Q4_TOPS_110A,
                       f"{str(year)} 1Q_Tops_AD10" : Q1_TOPS_AD10, f"{str(year)} 2Q_Tops_AD10" : Q2_TOPS_AD10, f"{str(year)} 3Q_Tops_AD10" : Q3_TOPS_AD10, f"{str(year)} 4Q_Tops_AD10" : Q4_TOPS_AD10  })


    # Retrieve the tops from the simulation tab
    df_110a_filtered = df_simu_func[df_simu_func[info] == "110A TOPs"]
    df_ad10_filtered = df_simu_func[df_simu_func[info] == "AD10 TOPs"]

    merged_df_110a = pd.merge(df, df_110a_filtered[[service_name, service_code, role, region, f"{year} Q1",f"{year} Q2",f"{year} Q3",f"{year} Q4"]], on=[service_name, service_code,role,region], how="left")
    merged_df_ad10 = pd.merge(df, df_ad10_filtered[[service_name, service_code, role, region, f"{year} Q1",f"{year} Q2",f"{year} Q3",f"{year} Q4"]], on=[service_name, service_code,role,region], how="left")

    df[Q1_TOPS_110A]=merged_df_110a[f"{year} Q1"]
    df[Q2_TOPS_110A]=merged_df_110a[f"{year} Q2"]
    df[Q3_TOPS_110A]=merged_df_110a[f"{year} Q3"]
    df[Q4_TOPS_110A]=merged_df_110a[f"{year} Q4"]

    df[Q1_TOPS_AD10]=merged_df_ad10[f"{year} Q1"]
    df[Q2_TOPS_AD10]=merged_df_ad10[f"{year} Q2"]
    df[Q3_TOPS_AD10]=merged_df_ad10[f"{year} Q3"]
    df[Q4_TOPS_AD10]=merged_df_ad10[f"{year} Q4"]


    
    
    #Groupe par Dpt / ALL / Region
    group=df.groupby([service_name,service_code,region]).agg({
                                                                    Q1_HC : 'sum', Q2_HC : 'sum', Q3_HC : 'sum', Q4_HC : 'sum',
                                                                    Q1_110AC : 'sum', Q2_110AC : 'sum', Q3_110AC : 'sum', Q4_110AC : 'sum',
                                                                    Q1_AD10C : 'sum', Q2_AD10C : 'sum', Q3_AD10C : 'sum', Q4_AD10C : 'sum',
                                                                    Q1_TOPS_110A : 'sum', Q2_TOPS_110A : 'sum', Q3_TOPS_110A : 'sum', Q4_TOPS_110A : 'sum',
                                                                    Q1_TOPS_AD10 : 'sum', Q2_TOPS_AD10 : 'sum', Q3_TOPS_AD10 : 'sum', Q4_TOPS_AD10 : 'sum'
                                                                     }).reset_index()


    somme=group.assign(Role='ALL')
    

    #On cherche à créer les lignes dpt_all_all uniquement pour les dpt ayant au moins 2 régions différentes (cas uniquement de la csu). On extrait donc que les données liées à la csu
    dpt_all_all= df[df[service_code].str.contains("17")]
    
    #Groupe par Dpt / ALL / ALL
    group2=dpt_all_all.groupby([service_code,service_name]).agg({ Q1_HC : 'sum', Q2_HC : 'sum', Q3_HC : 'sum', Q4_HC : 'sum',
                                                                Q1_110AC : 'sum', Q2_110AC : 'sum', Q3_110AC : 'sum', Q4_110AC : 'sum',
                                                                Q1_AD10C : 'sum', Q2_AD10C : 'sum', Q3_AD10C : 'sum', Q4_AD10C : 'sum',
                                                                Q1_TOPS_110A : 'sum', Q2_TOPS_110A : 'sum', Q3_TOPS_110A : 'sum', Q4_TOPS_110A : 'sum',
                                                                Q1_TOPS_AD10 : 'sum', Q2_TOPS_AD10 : 'sum', Q3_TOPS_AD10 : 'sum', Q4_TOPS_AD10 : 'sum'
                                                                    }).reset_index()
    
    somme2=group2.assign(Role='ALL')
    somme2=somme2.assign(Region='ALL')
    
    # TODO : 4
    
    
    bs10= df[df[service_code].str.contains("BS10")]
    bs10[service_code]="BS10"
    bs10[service_name]="Evidence Generation and Decision Science"
    bs10[role]="ALL"
    bs10[region]="ALL"
    bs10_all_all=bs10.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    
    db10= df[df[service_code].str.contains("DB1000|DB1001")]
    db10[service_code]="DB10"
    db10[service_name]="Management Office"
    db10[role]="ALL"
    db10[region]="ALL"
    db10_all_all=db10.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    
    db13= df[df[service_code].str.contains("DB13")]
    db13[service_code]="DB13"
    db13[service_name]="Operational Medical Dvpt & Clinical Doc"
    db13[role]="ALL"
    db13[region]="ALL"
    db13_all_all=db13.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    trial_ops= df[df[service_code].str.contains("DB15")]
    trial_ops[service_code]="DB15"
    trial_ops[service_name]="Clinical Data & AI Processing"
    trial_ops[role]="ALL"
    trial_ops[region]="ALL"
    trial_ops_all_all=trial_ops.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    
    csu= df[df[service_code].str.contains("DB17")]
    csu[service_code]="Total CSUs"
    csu[service_name]="CSUs"
    csu[role]="ALL"
    csu[region]="ALL"
    csu_all_all=csu.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    corpo= df[~df[service_code].str.contains("DB17")]
    corpo= corpo[~corpo[service_code].str.contains("BS")]
    corpo[service_code]="Total Corporate"
    corpo[service_name]="Corporate Centers"
    corpo[role]="ALL"
    corpo[region]="ALL"
    corpo_all_all=corpo.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    cso= df.copy()
    cso= cso[~cso[service_code].str.contains("BS")]
    cso[service_code]="Total CSO"
    cso[service_name]="CSO"
    cso[role]="ALL"
    cso[region]="ALL"
    cso=cso.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    cso_egds= df.copy()
    cso_egds[service_code]="Total CSO+EGDS"
    cso_egds[service_name]="CSO+EGDS"
    cso_egds[role]="ALL"
    cso_egds[region]="ALL"
    cso_egds=cso_egds.groupby([service_name,service_code,role,region]).sum().reset_index()


    df=pd.concat([df,somme],ignore_index=True)
    df=pd.concat([df,somme2],ignore_index=True)
    
    df=pd.concat([df,bs10_all_all],ignore_index=True)
    df=pd.concat([df,db10_all_all],ignore_index=True)
    df=pd.concat([df,db13_all_all],ignore_index=True)
    df=pd.concat([df,trial_ops_all_all],ignore_index=True)
    df=pd.concat([df,csu_all_all],ignore_index=True)
    df=pd.concat([df,corpo_all_all],ignore_index=True)
    df=pd.concat([df,cso],ignore_index=True)
    df=pd.concat([df,cso_egds],ignore_index=True)
    
    
    
    # TODO : 6
    def custom_sort_dashboard(row):
        
        value_service,value_role,value_region = row[service_code],row[role],row[region]
        
        if "DB" in value_service and "17" not in value_service:
            primary_order = 0
        elif value_service == "Total Corporate":
            primary_order =1
        elif "DB" in value_service and "17" in value_service:
            primary_order=2
        elif value_service == "Total CSUs":
            primary_order=3
        elif value_service=="Total CSO":
            primary_order=4
        elif "BS" in value_service:
            primary_order=5
        else:
            primary_order = 6
        
        # Extraire le numéro de Dpt si possible pour le tri secondaire    
        try:
            secondary=int(''.join(filter(str.isdigit,value_service)))
            if secondary==13:
                secondary=1299
            elif secondary==15:
                secondary=1499
            elif secondary==10:
                secondary=999
        except ValueError:
            secondary = 0
            
        # Gestion spéciale pour "Region"
        if value_region == 'ALL':
            region_priority = (0,)  # "ALL" a la plus haute priorité
        elif value_region == ' ':
            region_priority = (2,)  # Les valeurs vides sont placées en dernier
        else:
            region_priority = (1, value_region)  # Autres régions triées alphabétiquement
        
        

        
        if value_role== "ALL":
            role_order =(0,)
        else:
            role_order=(1,value_role)
        
          # Tuple de tri incluant la priorité de "ALL" et le tri par "Region"
        return (primary_order, secondary)+ region_priority + role_order
    
    # Appliquer la fonction de tri sur chaque ligne pour obtenir une colonne d'ordre de tri
    df['SortOrder'] = df.apply(custom_sort_dashboard, axis=1)
    
    # Trier le DataFrame selon l'ordre de tri personnalisé et supprimer la colonne d'ordre de tri
    df = df.sort_values(by='SortOrder').drop('SortOrder', axis=1)
    
    df=df.replace(to_replace=' ',value='')

    #HEADCOUNTS
    df[H1_HC]=(df[Q1_HC]+df[Q2_HC])/2
    df[H2_HC]=(df[Q3_HC]+df[Q4_HC])/2
    df[AVG_HC]=(df[H1_HC]+df[H2_HC])/2

    #110 A COMMITTED
    df[H1_110AC]=(df[Q1_110AC]+df[Q2_110AC])/2
    df[H2_110AC]=(df[Q3_110AC]+df[Q4_110AC])/2
    df[AVG_110AC]=(df[H1_110AC]+df[H2_110AC])/2

    # #AD10 COMMITED
    df[H1_AD10C]=(df[Q1_AD10C]+df[Q2_AD10C])/2
    df[H2_AD10C]=(df[Q3_AD10C]+df[Q4_AD10C])/2
    df[AVG_AD10C]=(df[H1_AD10C]+df[H2_AD10C])/2


    #TOPS
    df[Q1_TOPS]=df[Q1_TOPS_110A]+df[Q1_TOPS_AD10]
    df[Q2_TOPS]=df[Q2_TOPS_110A]+df[Q2_TOPS_AD10]
    df[Q3_TOPS]=df[Q3_TOPS_110A]+df[Q3_TOPS_AD10]
    df[Q4_TOPS]=df[Q4_TOPS_110A]+df[Q4_TOPS_AD10]

    df[H1_TOPS]=(df[Q1_TOPS]+df[Q2_TOPS])/2
    df[H2_TOPS]=(df[Q3_TOPS]+df[Q4_TOPS])/2
    df[AVG_TOPS]=(df[H1_TOPS]+df[H2_TOPS])/2

    #INSOURCING CONTRACTORS
    df[Q1_CONT]=df[Q1_110AC]+df[Q1_AD10C]+df[Q1_TOPS]
    df[Q2_CONT]=df[Q2_110AC]+df[Q2_AD10C]+df[Q2_TOPS]
    df[Q3_CONT]=df[Q3_110AC]+df[Q3_AD10C]+df[Q3_TOPS]
    df[Q4_CONT]=df[Q4_110AC]+df[Q4_AD10C]+df[Q4_TOPS]

    df[H1_CONT]=(df[Q1_CONT]+df[Q2_CONT])/2
    df[H2_CONT]=(df[Q3_CONT]+df[Q4_CONT])/2
    df[AVG_CONT]=(df[H1_CONT]+df[H2_CONT])/2



    #WORKFORCE
    df[Q1_WF]=df[Q1_CONT]+df[Q1_HC]
    df[Q2_WF]=df[Q2_CONT]+df[Q2_HC]
    df[Q3_WF]=df[Q3_CONT]+df[Q3_HC]
    df[Q4_WF]=df[Q4_CONT]+df[Q4_HC]

    df[H1_WF]=(df[Q1_WF]+df[Q2_WF])/2
    df[H2_WF]=(df[Q3_WF]+df[Q4_WF])/2
    df[AVG_WF]=(df[H1_WF]+df[H2_WF])/2
    
    return df


def get_dataframe(df,df_simu,year,year_to_drop,year_to_drop_two):
    """
    Renvoie les données sous la forme d'un dashboard pour les pages dashboard

    Args:
        df (dataframe): Dataframe contenant les données
        year (int): Année des données à garder
        year_to_drop (int): Année des données à se débarasser
        year_to_drop_two (int): Année des données à se débarasser

    Returns:
        df (dataframe): Dataframe contenant les données traitées pour le dataframe
        columnDefs(Ag-Grid): définition des différentes colonnes composant l'Ag-Grid
        defaultColDef (Ag-Grid): paramètres globaux des colonnes de l'Ag-Grid
    """

    #Drop the data from other year
    col_to_drop=df.filter(like=str(year_to_drop)).columns
    df=df.drop(columns=col_to_drop)

    col_to_drop=df.filter(like=str(year_to_drop_two)).columns
    df=df.drop(columns=col_to_drop)
    

    

    df=df.rename(columns={f'{str(year)} Q1_WL' : Q1_WL, f'{str(year)} Q2_WL' : Q2_WL, f'{str(year)} Q3_WL' : Q3_WL, f'{str(year)} Q4_WL' : Q4_WL,
                       f'{str(year)} Q1_HC' : Q1_HC, f'{str(year)} Q2_HC' : Q2_HC, f'{str(year)} Q3_HC' : Q3_HC, f'{str(year)} Q4_HC' : Q4_HC,
                       f'{str(year)} Q1_110A' : Q1_110AC, f'{str(year)} Q2_110A' : Q2_110AC, f'{str(year)} Q3_110A' : Q3_110AC, f'{str(year)} Q4_110A' : Q4_110AC,
                       f'{str(year)} Q1_AD10' : Q1_AD10C, f'{str(year)} Q2_AD10' : Q2_AD10C, f'{str(year)} Q3_AD10' : Q3_AD10C, f'{str(year)} Q4_AD10' : Q4_AD10C,
                       f"{str(year)} 1Q_Tops_110A" : Q1_TOPS_110A, f"{str(year)} 2Q_Tops_110A" : Q2_TOPS_110A, f"{str(year)} 3Q_Tops_110A" : Q3_TOPS_110A, f"{str(year)} 4Q_Tops_110A" : Q4_TOPS_110A,
                       f"{str(year)} 1Q_Tops_AD10" : Q1_TOPS_AD10, f"{str(year)} 2Q_Tops_AD10" : Q2_TOPS_AD10, f"{str(year)} 3Q_Tops_AD10" : Q3_TOPS_AD10, f"{str(year)} 4Q_Tops_AD10" : Q4_TOPS_AD10  })


    # Retrieve the tops from the simulation tab
    df_110a_filtered = df_simu[df_simu[info] == "110A TOPs"]
    df_ad10_filtered = df_simu[df_simu[info] == "AD10 TOPs"]

    merged_df_110a = pd.merge(df, df_110a_filtered[[service_name, service_code, role, region, f"{year} Q1",f"{year} Q2",f"{year} Q3",f"{year} Q4"]], on=[service_name, service_code,role,region], how="left")
    merged_df_ad10 = pd.merge(df, df_ad10_filtered[[service_name, service_code, role, region, f"{year} Q1",f"{year} Q2",f"{year} Q3",f"{year} Q4"]], on=[service_name, service_code,role,region], how="left")

    df[Q1_TOPS_110A]=merged_df_110a[f"{year} Q1"]
    df[Q2_TOPS_110A]=merged_df_110a[f"{year} Q2"]
    df[Q3_TOPS_110A]=merged_df_110a[f"{year} Q3"]
    df[Q4_TOPS_110A]=merged_df_110a[f"{year} Q4"]

    df[Q1_TOPS_AD10]=merged_df_ad10[f"{year} Q1"]
    df[Q2_TOPS_AD10]=merged_df_ad10[f"{year} Q2"]
    df[Q3_TOPS_AD10]=merged_df_ad10[f"{year} Q3"]
    df[Q4_TOPS_AD10]=merged_df_ad10[f"{year} Q4"]


    
    
    #Groupe par Dpt / ALL / Region
    group=df.groupby([service_name,service_code,region]).agg({Q1_WL : 'sum', Q2_WL : 'sum', Q3_WL : 'sum', Q4_WL : 'sum',
                                                                    Q1_HC : 'sum', Q2_HC : 'sum', Q3_HC : 'sum', Q4_HC : 'sum',
                                                                    Q1_110AC : 'sum', Q2_110AC : 'sum', Q3_110AC : 'sum', Q4_110AC : 'sum',
                                                                    Q1_AD10C : 'sum', Q2_AD10C : 'sum', Q3_AD10C : 'sum', Q4_AD10C : 'sum',
                                                                    Q1_TOPS_110A : 'sum', Q2_TOPS_110A : 'sum', Q3_TOPS_110A : 'sum', Q4_TOPS_110A : 'sum',
                                                                    Q1_TOPS_AD10 : 'sum', Q2_TOPS_AD10 : 'sum', Q3_TOPS_AD10 : 'sum', Q4_TOPS_AD10 : 'sum'
                                                                     }).reset_index()


    somme=group.assign(Role='ALL')
    

    #On cherche à créer les lignes dpt_all_all uniquement pour les dpt ayant au moins 2 régions différentes (cas uniquement de la csu). On extrait donc que les données liées à la csu
    dpt_all_all= df[df[service_code].str.contains("17")]
    
    #Groupe par Dpt / ALL / ALL
    group2=dpt_all_all.groupby([service_code,service_name]).agg({Q1_WL : 'sum', Q2_WL : 'sum', Q3_WL : 'sum', Q4_WL : 'sum',
                                                                    Q1_HC : 'sum', Q2_HC : 'sum', Q3_HC : 'sum', Q4_HC : 'sum',
                                                                    Q1_110AC : 'sum', Q2_110AC : 'sum', Q3_110AC : 'sum', Q4_110AC : 'sum',
                                                                    Q1_AD10C : 'sum', Q2_AD10C : 'sum', Q3_AD10C : 'sum', Q4_AD10C : 'sum',
                                                                    Q1_TOPS_110A : 'sum', Q2_TOPS_110A : 'sum', Q3_TOPS_110A : 'sum', Q4_TOPS_110A : 'sum',
                                                                    Q1_TOPS_AD10 : 'sum', Q2_TOPS_AD10 : 'sum', Q3_TOPS_AD10 : 'sum', Q4_TOPS_AD10 : 'sum'
                                                                     }).reset_index()
    
    somme2=group2.assign(Role='ALL')
    somme2=somme2.assign(Region='ALL')
 
 
    #TODO : 5
 
    bs10= df[df[service_code].str.contains("BS10")]
    bs10[service_code]="BS10"
    bs10[service_name]="Evidence Generation and Decision Science"
    bs10[role]="ALL"
    bs10[region]="ALL"
    bs10_all_all=bs10.groupby([service_name,service_code,role,region]).sum().reset_index()
 
    
    db13= df[df[service_code].str.contains("DB13")]
    db13[service_code]="DB13"
    db13[service_name]="Operational Medical Dvpt & Clinical Doc"
    db13[role]="ALL"
    db13[region]="ALL"
    db13_all_all=db13.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    trial_ops= df[df[service_code].str.contains("DB15")]
    trial_ops[service_code]="DB15"
    trial_ops[service_name]="Clinical Data & AI Processing"
    trial_ops[role]="ALL"
    trial_ops[region]="ALL"
    trial_ops_all_all=trial_ops.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    
    csu= df[df[service_code].str.contains("DB17")]
    csu[service_code]="Total CSUs"
    csu[service_name]="CSUs"
    csu[role]="ALL"
    csu[region]="ALL"
    csu_all_all=csu.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    corpo= df[~df[service_code].str.contains("DB17")]
    corpo= corpo[~corpo[service_code].str.contains("BS")]
    corpo[service_code]="Total Corporate"
    corpo[service_name]="Corporate Centers"
    corpo[role]="ALL"
    corpo[region]="ALL"
    corpo_all_all=corpo.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    cso= df.copy()
    cso= cso[~cso[service_code].str.contains("BS")]
    cso[service_code]="Total CSO"
    cso[service_name]="CSO"
    cso[role]="ALL"
    cso[region]="ALL"
    cso=cso.groupby([service_name,service_code,role,region]).sum().reset_index()
    
    cso_egds= df.copy()
    cso_egds[service_code]="Total CSO+EGDS"
    cso_egds[service_name]="CSO+EGDS"
    cso_egds[role]="ALL"
    cso_egds[region]="ALL"
    cso_egds=cso_egds.groupby([service_name,service_code,role,region]).sum().reset_index()

    df=pd.concat([df,somme],ignore_index=True)
    df=pd.concat([df,somme2],ignore_index=True)
    
    df=pd.concat([df,bs10_all_all],ignore_index=True)
    df=pd.concat([df,db13_all_all],ignore_index=True)
    df=pd.concat([df,trial_ops_all_all],ignore_index=True)
    df=pd.concat([df,csu_all_all],ignore_index=True)
    df=pd.concat([df,corpo_all_all],ignore_index=True)
    df=pd.concat([df,cso],ignore_index=True)
    df=pd.concat([df,cso_egds],ignore_index=True)
    
    # TODO : 6
    def custom_sort_dashboard(row):
        
        value_service,value_role,value_region = row[service_code],row[role],row[region]
        
        if "DB" in value_service and "17" not in value_service:
            primary_order = 0
        elif value_service == "Total Corporate":
            primary_order =1
        elif "DB" in value_service and "17" in value_service:
            primary_order=2
        elif value_service == "Total CSUs":
            primary_order=3
        elif value_service=="Total CSO":
            primary_order=4
        elif "BS" in value_service:
            primary_order=5
        else:
            primary_order = 6
        
        # Extraire le numéro de Dpt si possible pour le tri secondaire    
        try:
            secondary=int(''.join(filter(str.isdigit,value_service)))
            if secondary==13:
                secondary=1299
            elif secondary==15:
                secondary=1499
            elif secondary==10:
                secondary=999
        except ValueError:
            secondary = 0
            
        # Gestion spéciale pour "Region"
        if value_region == 'ALL':
            region_priority = (0,)  # "ALL" a la plus haute priorité
        elif value_region == ' ':
            region_priority = (2,)  # Les valeurs vides sont placées en dernier
        else:
            region_priority = (1, value_region)  # Autres régions triées alphabétiquement
        
        

        
        if value_role== "ALL":
            role_order =(0,)
        else:
            role_order=(1,value_role)
        
          # Tuple de tri incluant la priorité de "ALL" et le tri par "Region"
        return (primary_order, secondary)+ region_priority + role_order
    
    # Appliquer la fonction de tri sur chaque ligne pour obtenir une colonne d'ordre de tri
    df['SortOrder'] = df.apply(custom_sort_dashboard, axis=1)
    
    # Trier le DataFrame selon l'ordre de tri personnalisé et supprimer la colonne d'ordre de tri
    df = df.sort_values(by='SortOrder').drop('SortOrder', axis=1)
    
    df=df.replace(to_replace=' ',value='')

    #WORKLOAD
    df[H1_WL]=(df[Q1_WL]+df[Q2_WL])/2
    df[H2_WL]=(df[Q3_WL]+df[Q4_WL])/2
    df[AVG_WL]=(df[H1_WL]+df[H2_WL])/2

    #HEADCOUNTS
    df[H1_HC]=(df[Q1_HC]+df[Q2_HC])/2
    df[H2_HC]=(df[Q3_HC]+df[Q4_HC])/2
    df[AVG_HC]=(df[H1_HC]+df[H2_HC])/2

    #110 A COMMITTED
    df[H1_110AC]=(df[Q1_110AC]+df[Q2_110AC])/2
    df[H2_110AC]=(df[Q3_110AC]+df[Q4_110AC])/2
    df[AVG_110AC]=(df[H1_110AC]+df[H2_110AC])/2

    # #AD10 COMMITED
    df[H1_AD10C]=(df[Q1_AD10C]+df[Q2_AD10C])/2
    df[H2_AD10C]=(df[Q3_AD10C]+df[Q4_AD10C])/2
    df[AVG_AD10C]=(df[H1_AD10C]+df[H2_AD10C])/2


    #TOPS
    df[Q1_TOPS]=df[Q1_TOPS_110A]+df[Q1_TOPS_AD10]
    df[Q2_TOPS]=df[Q2_TOPS_110A]+df[Q2_TOPS_AD10]
    df[Q3_TOPS]=df[Q3_TOPS_110A]+df[Q3_TOPS_AD10]
    df[Q4_TOPS]=df[Q4_TOPS_110A]+df[Q4_TOPS_AD10]

    df[H1_TOPS]=(df[Q1_TOPS]+df[Q2_TOPS])/2
    df[H2_TOPS]=(df[Q3_TOPS]+df[Q4_TOPS])/2
    df[AVG_TOPS]=(df[H1_TOPS]+df[H2_TOPS])/2

    #INSOURCING CONTRACTORS
    df[Q1_CONT]=df[Q1_110AC]+df[Q1_AD10C]+df[Q1_TOPS]
    df[Q2_CONT]=df[Q2_110AC]+df[Q2_AD10C]+df[Q2_TOPS]
    df[Q3_CONT]=df[Q3_110AC]+df[Q3_AD10C]+df[Q3_TOPS]
    df[Q4_CONT]=df[Q4_110AC]+df[Q4_AD10C]+df[Q4_TOPS]

    df[H1_CONT]=(df[Q1_CONT]+df[Q2_CONT])/2
    df[H2_CONT]=(df[Q3_CONT]+df[Q4_CONT])/2
    df[AVG_CONT]=(df[H1_CONT]+df[H2_CONT])/2



    #WORKFORCE
    df[Q1_WF]=df[Q1_CONT]+df[Q1_HC]
    df[Q2_WF]=df[Q2_CONT]+df[Q2_HC]
    df[Q3_WF]=df[Q3_CONT]+df[Q3_HC]
    df[Q4_WF]=df[Q4_CONT]+df[Q4_HC]

    df[H1_WF]=(df[Q1_WF]+df[Q2_WF])/2
    df[H2_WF]=(df[Q3_WF]+df[Q4_WF])/2
    df[AVG_WF]=(df[H1_WF]+df[H2_WF])/2



    #INTERNAL WORKLOAD COVERAGE 
    df[Q1_COVER]=df[Q1_WF]/df[Q1_WL]*100
    df[Q2_COVER]=df[Q2_WF]/df[Q2_WL]*100
    df[Q3_COVER]=df[Q3_WF]/df[Q3_WL]*100
    df[Q4_COVER]=df[Q4_WF]/df[Q4_WL]*100

    df=df.replace([np.inf, -np.inf],0)
    df=df.fillna(value=0)

    df[H1_COVER]=(df[Q1_COVER]+df[Q2_COVER])/2
    df[H2_COVER]=(df[Q3_COVER]+df[Q4_COVER])/2
    df[AVG_COVER]=(df[H1_COVER]+df[H2_COVER])/2

    #INTERNAL WORKLOAD GAP FTEs
    df[Q1_GAP]=df[Q1_WF]-df[Q1_WL]
    df[Q2_GAP]=df[Q2_WF]-df[Q2_WL]
    df[Q3_GAP]=df[Q3_WF]-df[Q3_WL]
    df[Q4_GAP]=df[Q4_WF]-df[Q4_WL]

    df[H1_GAP]=(df[Q1_GAP]+df[Q2_GAP])/2
    df[H2_GAP]=(df[Q3_GAP]+df[Q4_GAP])/2
    df[AVG_GAP]=(df[H1_GAP]+df[H2_GAP])/2

    #FLEXIBILITY
    df[Q1_FLEX]=df[Q1_CONT]/df[Q1_WF]*100
    df[Q2_FLEX]=df[Q2_CONT]/df[Q2_WF]*100
    df[Q3_FLEX]=df[Q3_CONT]/df[Q3_WF]*100
    df[Q4_FLEX]=df[Q4_CONT]/df[Q4_WF]*100

    df=df.replace([np.inf, -np.inf],0)
    df=df.fillna(value=0)

    df[H1_FLEX]=(df[Q1_FLEX]+df[Q2_FLEX])/2
    df[H2_FLEX]=(df[Q3_FLEX]+df[Q4_FLEX])/2
    df[AVG_FLEX]=(df[H1_FLEX]+df[H2_FLEX])/2
    
    # df.info(memory_usage='deep')
    return df



# List of expected columns
list_columns = ['Name', 'Network ID', 'Primary skill', 'Default Operationality', 'Service Finance Code', 'Site',
                'Base Entity', 'Element of', 'Contract type', 'Quantity', '% Direct', '% Contract', '% Allocation',
                'Effective start date', 'Effective end date', 'Simulation?']


def heads(row):
    fte=row['Quantity']
    oper = row['% Direct']
    oper=oper/100
    heads=fte/oper
    return heads


#---- Quantity
# Roundup of Heads
def quantity(row):

    heads = row['Heads']
    
    if heads >= 0:
        new_heads = np.ceil(heads)
    else:
        new_heads = np.floor(heads) 
    
    return new_heads


# #---- % Contract
# # >- empty if Quantity equals to 0  
# # >- 100 if Default Operationality = Functional  
# # >- if Default Operationality = Operational  
# #     Quantity is rounded from Heads -> Integer expected into RDPM  
# #         Quantity * % Direct * % Contract * % Allocation (100%) = FTE  
# #         Heads = FTE / %Oper (into Sourcing Table), so FTE = Heads * %Oper
# #         % Direct = %Oper, then FTE = Heads * % Direct
# #         Then, Quantity * % Direct * % Contract * % Allocation (100%) = FTE = Heads * % Direct
# #         % Contract = (Heads * % Direct) / (Quantity * % Direct) = Heads / Quantity
# #             Validation : Quantity * % Direct * 1 * % Contract = FTE (into Sourcing Table)
# # >- empty else  
def pct_contract(row):
    
    quantity = row['Quantity']
    heads = row['Heads']
    default_oper = row['Default Operationality']
    
    if quantity==0:
        return np.nan
    else:
        if default_oper == 'Functional':
            return 100
        elif default_oper == 'Operational':
            return round(heads / quantity, 6) * 100
        else:
            return np.nan


map_site = {'AP': 'APU', 'EUR':'EURU', 'NAM':'NAMU', 'LAM':'LAMU', 'TBD':'ND', 'TOP':'ND', '':'ND', ' ':'ND'}

def map_sites(row):
    if row in list(map_site.keys()):
        return map_site[row]
    else:
        return row
    

#----- Base Entity
# 
# for CSU :
# DB17:  LAM -> USR1200207 , NAM -> USR1200207, EUR -> FRR2400126, AP = FRR2400126, ND -> FRR2400126
# 
# DB11 : AD10 -> CNR0101847 (CHINE), 110A -> FRR2400126 (FRANCE)  
# DB12 : AD10 -> **NOTHING**, 110A ->  **NOTHING**  
# DB13 : AD10 -> CNR0101847 (CHINE), 110A ->  FRR2400126 (FRANCE)  
# DB14 : AD10 -> **NOTHING**, 110A ->  FRR2400126 (FRANCE)  
# DB15 : AD10 -> CNR0101847 (CHINE), 110A -> FRR2400126 (FRANCE)  
# DB16 : AD10 -> CNR0101847 (CHINE), 110A -> FRR2400126 (FRANCE)  
# DB18 : AD10 -> FRR2400126 (FRANCE), 110A -> FRR2400126 (FRANCE)  
# 
# At the end, if empty, attrib FRR2400126 (FRANCE)
# 

def attrib_base_entity(row):
    
    nat = row['Contract type'].strip()
    dept = row['Service Finance Code'].strip()[0:4]
    site = row['Site'].strip()
    base_entity = ''
    
    if dept == 'DB17':
        if site in ['AP','EUR', 'ND']:
            base_entity = 'FRR2400126' 
        elif site[:3] in ['LAM','NAM']:
            base_entity = 'USR1200207'
    elif dept in ['DB11', 'DB13', 'DB15', 'DB16']:
        if nat == 'INTERIM':
            return 'CNR0101847'
        elif nat == 'CONTS':
            return 'FRR2400126'
    elif dept == 'DB18':
        return 'FRR2400126'
        
    if base_entity == '':
        base_entity = 'FRR2400126'
        
    return base_entity

quarters = ['Q1', 'Q2', 'Q3', 'Q4']
#---- Effective start date, Effective end date
# Effective start/end dates are derived from Year and quarters
map_quarter = dict(zip(quarters,[2,5,8,11]))

def first_last_days_of_quarter(row):

    year = int(row['Year'])
    month = int(map_quarter[row['Quarter']])
    
    current_date = datetime(year, month, 1)

    current_quarter = round((current_date.month - 1) / 3 + 1)
    
    first_date = datetime(current_date.year, 3 * current_quarter - 2, 1)
    last_date = first_date + relativedelta(months=3, days=-1)

    return pd.Series([first_date, last_date])
    
    
    
def prepare_Tops(tops_ope,tops_func,rate):
    
    global initial_rate
    # ===================================================PARTIE OPERATIONNEL======================================================
    tops_ope=tops_ope.query('Info == "110A TOPs" | Info == "AD10 TOPs"')
    tops_ope=tops_ope.query('Role != "ALL"')
    tops_ope=tops_ope.query('Region != "ALL"')
    tops_ope = tops_ope.query('`Service Name` != "ALL"')
    tops_ope['Default Operationality']="Operational"
    tops_ope=tops_ope.rename(columns={"Info": "Contract type"})
    
    # Utilisation de 'melt' pour restructurer le DataFrame en incluant toutes les colonnes identifiantes
    id_vars_list = [role, "Default Operationality",service_name, "Contract type", service_code,region ]
    tops_ope = tops_ope.melt(id_vars=id_vars_list, var_name='Quarter_Year', value_name='Quantity')
    
    # # Extraction du trimestre et de l'année
    tops_ope['Quarter'] = tops_ope['Quarter_Year'].apply(lambda x: x.split()[1])
    tops_ope['Year'] = tops_ope['Quarter_Year'].apply(lambda x: x.split()[0])

    # # Suppression de la colonne 'Quarter_Year' maintenant inutile
    tops_ope = tops_ope.drop('Quarter_Year', axis=1)
    tops_ope=tops_ope.query('Quantity != 0.0')

    # ===================================================PARTIE Fonctionnel======================================================

    tops_func=tops_func.query('Info == "110A TOPs" | Info == "AD10 TOPs"')
    tops_func=tops_func.query('Role != "ALL"')
    tops_func=tops_func.query('Region != "ALL"')
    tops_func = tops_func[tops_func['Service Name'] != "ALL"]
    tops_func['Default Operationality']="Functional"
    tops_func=tops_func.rename(columns={"Info": "Contract type"})


    # Utilisation de 'melt' pour restructurer le DataFrame en incluant toutes les colonnes identifiantes
    id_vars_list = [role, "Default Operationality",service_name, "Contract type", service_code,region ]  # Ajoutez ici toutes les colonnes identifiantes
    tops_func = tops_func.melt(id_vars=id_vars_list, var_name='Quarter_Year', value_name='Quantity')

    # # Extraction du trimestre et de l'année
    tops_func['Quarter'] = tops_func['Quarter_Year'].apply(lambda x: x.split()[1])
    tops_func['Year'] = tops_func['Quarter_Year'].apply(lambda x: x.split()[0])

    # # Suppression de la colonne 'Quarter_Year' maintenant inutile
    tops_func = tops_func.drop('Quarter_Year', axis=1)
    tops_func=tops_func.query('Quantity != 0.0')


    if tops_ope.empty:
        if tops_func.empty:
            tops=pd.DataFrame(columns=list_columns)
            tops.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')            
            return tops
            
        else:
            tops_func=tops_func.replace(["110A TOPs","AD10 TOPs"],["CONTS","INTERIM"])
            tops_func['% Allocation']=100.0
            tops_func['% Direct']=0.0
            tops_func['% Contract'] = 100.0

            tops_func = tops_func.rename(columns={role: 'Primary skill', service_code: 'Service Finance Code', service_name: 'Element of', region: 'Site'})

            tops_func['Site'] = tops_func['Site'].apply(lambda row: map_sites(row))

            tops_func['Base Entity'] = tops_func.apply(attrib_base_entity, axis=1)

            tops_func['Element of'] = tops_func['Element of'].apply(lambda row: 'TPO-TPO' if row == 'TPO' else row)

            # #----- Simulation?
            tops_func['Simulation?'] = 'YES'



            tops_func[['Effective start date','Effective end date']] = tops_func.apply(lambda row: first_last_days_of_quarter(row), axis=1)

            # # # Sort the dataframe by Record Type, Default Operationality, row Numbers, Effective start date and Effective end date
            tops_func = tops_func.sort_values(by=['Default Operationality', 'Contract type', 'Service Finance Code', 'Site', 'Primary skill', 'Effective start date', 'Effective end date'])
            
            #---- Name
            # 'Name' is a derived column by concanenating 'TOP_' prefix for name and a number value incrementing from 1 to n
            # examples : TOP_1, TOP_2, ...
            tops_func.reset_index(inplace=True)
            tops_func['Index'] = tops_func.index
            tops_func['Name'] = tops_func.apply(lambda row: 'TOP_' + str(row['Index']+1), axis=1)

            # #---- Network ID
            # # 'Network ID' is a derived column by concanenating 'TOP_' prefix and a number value incrementing from 1 to n  
            # # examples : TOP_1, TOP_2, ... 
            tops_func['Network ID'] = [f'TOP_{i+1}' for i in tops_func.index]

            # # Convert date variable as string value formatted as %d/%m/%Y
            tops_func['Effective start date'] = tops_func['Effective start date'].dt.strftime('%d/%m/%Y')
            tops_func['Effective end date'] = tops_func['Effective end date'].dt.strftime('%d/%m/%Y')

            tops = tops_func[list_columns]  
            tops.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')
            return tops

    else:
        if tops_func.empty:
            tops_ope=tops_ope.replace(["110A TOPs","AD10 TOPs"],["CONTS","INTERIM"])
            tops_ope=tops_ope.merge(rate,on=[service_name,service_code,role,region])
            tops_ope['% Direct']= np.where(tops_ope['Contract type'] == 'CONTS', tops_ope['% Direct_110A'], tops_ope['% Direct_AD10'])
            tops_ope['Missing']="False"
            tops_ope.loc[tops_ope['% Direct'].isna(), 'Missing'] = "True"
            rate['Missing']="False"
            rate=rate.merge(tops_ope[[service_name,service_code,role,region,"Missing"]], on=[service_name,service_code,role,region], how='left', suffixes=('', '_new'))
            # Grouper le DataFrame et aggréger
            rate = rate.groupby([service_name, service_code, role, region]).agg({
                '% Direct_110A': 'first',  # exemple d'agrégation, prenez la première valeur non nulle
                'Source_110A': 'first',    # même logique pour les autres colonnes si approprié
                '% Direct_AD10': 'first',
                'Source_AD10': 'first',
                'Missing': 'first',
                'Missing_new': 'max'       # max va prendre True si au moins une des valeurs est True
            }).reset_index(drop=False)
            rate=rate.sort_values(by=[service_code,region,role])
            rate=rate.reset_index(drop=True)
            rate['Missing']=rate['Missing_new'].combine_first(rate['Missing'])
            rate = rate.drop('Missing_new', axis=1)

            initial_rate=rate
            
            
            rate.to_csv(os.path.join(base_path, "operational_rate.csv"),index=False,sep=';')
                        
            tops_ope = tops_ope.drop('% Direct_110A', axis=1)
            tops_ope = tops_ope.drop('% Direct_AD10', axis=1)
            tops_ope = tops_ope.drop('Source_110A', axis=1)
            tops_ope = tops_ope.drop('Source_AD10', axis=1)
            tops_ope = tops_ope.drop('Missing', axis=1)

            tops_ope['Heads'] = tops_ope.apply(heads, axis=1)



            tops_ope['Quantity'] = tops_ope.apply(quantity, axis=1)
            tops_ope['% Allocation']=100.0


                    
                    
            tops_ope['% Contract'] = tops_ope.apply(pct_contract, axis=1)
            tops_ope['% Contract'] = tops_ope['% Contract'].round(4) 

        
            tops_ope = tops_ope.rename(columns={role: 'Primary skill', service_code: 'Service Finance Code', service_name: 'Element of', region: 'Site'})



            tops_ope['Site'] = tops_ope['Site'].apply(lambda row: map_sites(row))


                
            tops_ope['Base Entity'] = tops_ope.apply(attrib_base_entity, axis=1)

            tops_ope['Element of'] = tops_ope['Element of'].apply(lambda row: 'TPO-TPO' if row == 'TPO' else row)

            # #----- Simulation?
            tops_ope['Simulation?'] = 'YES'


            tops_ope[['Effective start date','Effective end date']] = tops_ope.apply(lambda row: first_last_days_of_quarter(row), axis=1)

            
            # # # Sort the dataframe by Record Type, Default Operationality, row Numbers, Effective start date and Effective end date
            tops_ope = tops_ope.sort_values(by=['Default Operationality', 'Contract type', 'Service Finance Code', 'Site', 'Primary skill', 'Effective start date', 'Effective end date'])  
            
            #---- Name
            # 'Name' is a derived column by concanenating 'TOP_' prefix for name and a number value incrementing from 1 to n
            # examples : TOP_1, TOP_2, ...
            tops_ope.reset_index(inplace=True)
            tops_ope['Index'] = tops_ope.index
            tops_ope['Name'] = tops_ope.apply(lambda row: 'TOP_' + str(row['Index']+1), axis=1)

            # #---- Network ID
            # # 'Network ID' is a derived column by concanenating 'TOP_' prefix and a number value incrementing from 1 to n  
            # # examples : TOP_1, TOP_2, ... 
            tops_ope['Network ID'] = [f'TOP_{i+1}' for i in tops_ope.index]

            # # Convert date variable as string value formatted as %d/%m/%Y
            tops_ope['Effective start date'] = tops_ope['Effective start date'].dt.strftime('%d/%m/%Y')
            tops_ope['Effective end date'] = tops_ope['Effective end date'].dt.strftime('%d/%m/%Y')

            tops = tops_ope[list_columns]  
            tops.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')
            return tops
        
        else:
            tops_ope=tops_ope.replace(["110A TOPs","AD10 TOPs"],["CONTS","INTERIM"])
            tops_ope=tops_ope.merge(rate,on=[service_name,service_code,role,region])
            tops_ope['% Direct']= np.where(tops_ope['Contract type'] == 'CONTS', tops_ope['% Direct_110A'], tops_ope['% Direct_AD10'])
            tops_ope['Missing']="False"
            tops_ope.loc[tops_ope['% Direct'].isna(), 'Missing'] = "True"
            rate['Missing']="False"
            rate=rate.merge(tops_ope[[service_name,service_code,role,region,"Missing"]], on=[service_name,service_code,role,region], how='left', suffixes=('', '_new'))
            # Grouper le DataFrame et aggréger
            rate = rate.groupby([service_name, service_code, role, region]).agg({
                '% Direct_110A': 'first',  # exemple d'agrégation, prenez la première valeur non nulle
                'Source_110A': 'first',    # même logique pour les autres colonnes si approprié
                '% Direct_AD10': 'first',
                'Source_AD10': 'first',
                'Missing': 'first',
                'Missing_new': 'max'       # max va prendre True si au moins une des valeurs est True
            }).reset_index()

            rate=rate.sort_values(by=[service_code,region,role])
            rate=rate.reset_index()

            rate['Missing']=rate['Missing_new'].combine_first(rate['Missing'])
            rate = rate.drop('Missing_new', axis=1)

            initial_rate=rate
            
            
            rate.to_csv(os.path.join(base_path, "operational_rate.csv"),index=False,sep=';')
                        
            tops_ope = tops_ope.drop('% Direct_110A', axis=1)
            tops_ope = tops_ope.drop('% Direct_AD10', axis=1)
            tops_ope = tops_ope.drop('Source_110A', axis=1)
            tops_ope = tops_ope.drop('Source_AD10', axis=1)
            tops_ope = tops_ope.drop('Missing', axis=1)

            tops_ope['Heads'] = tops_ope.apply(heads, axis=1)

            tops_ope['Quantity'] = tops_ope.apply(quantity, axis=1)
            tops_ope['% Allocation']=100.0

            tops_ope['% Contract'] = tops_ope.apply(pct_contract, axis=1)
            tops_ope['% Contract'] = tops_ope['% Contract'].round(4) 
        
            tops_func=tops_func.replace(["110A TOPs","AD10 TOPs"],["CONTS","INTERIM"])
            tops_func['% Allocation']=100.0
            tops_func['% Direct']=0.0
            tops_func['% Contract'] = 100.0


            tops = pd.concat([tops_ope, tops_func], ignore_index=True)

            # Renommer les colonnes 'Âge' et 'Service'
            tops = tops.rename(columns={role: 'Primary skill', service_code: 'Service Finance Code', service_name: 'Element of', region: 'Site'})

            tops['Site'] = tops['Site'].apply(lambda row: map_sites(row))


                
            tops['Base Entity'] = tops.apply(attrib_base_entity, axis=1)

            tops['Element of'] = tops['Element of'].apply(lambda row: 'TPO-TPO' if row == 'TPO' else row)

            # #----- Simulation?
            tops['Simulation?'] = 'YES'


            tops[['Effective start date','Effective end date']] = tops.apply(lambda row: first_last_days_of_quarter(row), axis=1)

            # # # Sort the dataframe by Record Type, Default Operationality, row Numbers, Effective start date and Effective end date
            tops = tops.sort_values(by=['Default Operationality', 'Contract type', 'Service Finance Code', 'Site', 'Primary skill', 'Effective start date', 'Effective end date'])   

            #---- Name
            # 'Name' is a derived column by concanenating 'TOP_' prefix for name and a number value incrementing from 1 to n
            # examples : TOP_1, TOP_2, ...
            tops.reset_index(inplace=True)
            tops['Index'] = tops.index
            tops['Name'] = tops.apply(lambda row: 'TOP_' + str(row['Index']+1), axis=1)

            # #---- Network ID
            # # 'Network ID' is a derived column by concanenating 'TOP_' prefix and a number value incrementing from 1 to n  
            # # examples : TOP_1, TOP_2, ... 
            tops['Network ID'] = [f'TOP_{i+1}' for i in tops.index]

            # # Convert date variable as string value formatted as %d/%m/%Y
            tops['Effective start date'] = tops['Effective start date'].dt.strftime('%d/%m/%Y')
            tops['Effective end date'] = tops['Effective end date'].dt.strftime('%d/%m/%Y')

            tops = tops[list_columns]  
            tops.to_csv(os.path.join(base_path, f"CSO_Tops - {date}.csv"),index=False,sep=';')
            return tops
        
 
try:
    tops_export=pd.read_csv(f"{base_path}/CSO_Tops - {date}.csv",sep=';')
except Exception as error:
    tops_export=prepare_Tops(simu_ope,simu_func,initial_rate)  
