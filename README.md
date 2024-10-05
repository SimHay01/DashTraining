https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

# Application overview

The Sourcing Table App is a web application created to view and manage resource data on the CSO platform. This application is intended for the CSO OPCM department. 

# Maintenance guide

The purpose of this README is to facilitate the maintenance of this application by describing the specific logic and procedure to be followed in the event of a change of the structure of the CSO or the scope of the application.

## Library management

Python 3.8.6 was used to develop this application.

The list of libraries used can be found in the requirements.txt file. Please do not update the versions used in order to guarantee the correct functioning of the application.

⚠ Dash Ag Grid version 2.4.0 is required to allow cells in the “Simulation” table to update according to user input⚠


## Recommendations to facilitate application maintenance

To easily find the different parts of the code to be modified during maintenance, these will be identified using numerated keywords (TODO, NOTE, FIXME, etc). To easily find these keywords and their location, I recommend using the ["Todo Tree"](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree) extension. You can then easily navigate to each keyword by clicking on them.


## What to do if the CSO's structure changes?

In the case of a change in the structure of the CSO or the renaming of a service, you must go to the "dataframe.py" file (located at the path pages/sourcing_table/dataframe.py) and modify the "service" dictionary (code below) identified by the TODO 1. Please keep services that are no longer relevant, do not delete them.

``` python
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
```
When adding or modifying a service group (e.g. DB13 or DB15), go to the new_baseline function (still in the "dataframe.py" file) and add your changes in the operational part (TODO 2) and/or in the functional part (TODO 3).

The logic to follow in both case is:

``` python

# **1st step:** We create a dataframe containing only the rows corresponding to the service group in question
db13= df_simu[df_simu[service_code].str.contains("DB13")]

# 2nd step: We rename the various identifying columns in each row with the same value. Service code will correspond to the number identifying the service group, service name to its name and we write “ALL” to role's value to indicate that the data will correspond to that of the service group, all roles combined.
db13[service_code]="DB13"
db13[service_name]="Operational Medical Dvpt & Clinical Doc"
db13[role]="ALL"

# 3rd step: We group all the lines to obtain the sum in a new dataframe. The result is the data for the service group (all roles combined) for each of its regions.
db13_all_region=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

# 4th step: We rename the value of region of each line with "ALL" and we group all the line to obtain the data for the service group all roles combined and all regions combined in a new dataframe.
db13[region]="ALL"
db13_all_all=db13.groupby([service_name,service_code,role,region,info]).sum().reset_index()

#[....]

# When all service groups have been defined in dataframes in this way, we concatenate the original dataframe (df_simu) with each dataframe created.
df_simu=pd.concat([df_simu,db13_all_region],ignore_index=True)

df_simu=pd.concat([df_simu,db13_all_all],ignore_index=True)

```
You also need to go to the get_dataframe_functional function (TODO 4) and the get_dataframe function (TODO 5) to add or modify the following lines:

``` python
#Adapt theses lines to your new service group
db13= df[df[service_code].str.contains("DB13")]
db13[service_code]="DB13"
db13[service_name]="Operational Medical Dvpt & Clinical Doc"
db13[role]="ALL"
db13[region]="ALL"
db13_all_all=db13.groupby([service_name,service_code,role,region]).sum().reset_index()

#[...]

df=pd.concat([df,db13_all_all],ignore_index=True)
```

It may be necessary to adapt the custom_sort_dashboard function (TODO 6, it can be found in the get_dataframe and get_dataframe_function functions) in order to keep a consistent display in the "Dashboards" tabs (We want to have the line corresponding to the service group, then the lines of the services making up this group below).

Since this function is based on the service code value to establish its order, it is necessary to change the value assigned when sorting the department groups. Indeed, they are represented by short codes (13 for DB13, 15 for DB15) while the services are represented by higher codes (1300 for DB1300 for example). DB15 would be then represented before DB13 for example and would not be grouped with DB1500.

To prevent this, change the part indicated by the comment in the custom_sort_dashboard function:

``` python

    def custom_sort_dashboard(row):
        
        value_service,value_role,value_region = row[service_code],row[role],row[region]
        
        #Management of the overall dashboard order
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
        
        # Service code management
        # CHANGE HERE BY ADDING A CONDITION TO TRANSFORM THE VALUE OF YOUR SERVICE GROUP INTO A HIGHER VALUE  
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
            
        # Region management
        if value_region == 'ALL':
            region_priority = (0,)  # "ALL" a la plus haute priorité
        elif value_region == ' ':
            region_priority = (2,)  # Les valeurs vides sont placées en dernier
        else:
            region_priority = (1, value_region)  # Autres régions triées alphabétiquement
        
        # Role management
        if value_role== "ALL":
            role_order =(0,)
        else:
            role_order=(1,value_role)
        

        return (primary_order, secondary)+ region_priority + role_order

```

Finally, we need to modify the "dagfuncs.valueGetter" function (TODO 7) in the "dashAgGridFunctions.js" file in the "assets" folder. This function enables the simulations tabs to correctly calculate, for service groups, the entries made by the user in the TOPs for each service making up the service group.

In the case of a rename, it is sufficient to change the value of the string contained in the condition `params.data['Service Name']== string` in the blocks corresponding to the service group in question (there are generally 2 blocks per service group, one for the DPT-GRP/ALL/Region combination, the other for DPT-GRP/ALL/ALL).

```js
    // Exemple for DB13

    // Case of DB13 / ALL / ALL
    else if ((params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){ // Change here the condition params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc" with the new value
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB13"))){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DB13 / ALL / Region
    else if ((params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc") && (params.data.Role == "ALL")){ // Change here the condition params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc" with the new value
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB13")) && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
```

In case of adding a service group, please add the following lines, adapting them with your values:

```js

    // Case of DPT-GRP / ALL / ALL
    else if ((params.data['Service Name']== "Your_New_Service_Name") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("Your_New_Service_Code"))){ // Adapt the condition according to the specificities characterizing your service group
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DPT-GRP / ALL / Region
    else if ((params.data['Service Name']=="Your_New_Service_Name") && (params.data.Role == "ALL")){ 
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("Your_New_Service_Code")) && (rowNode.data.Region == params.data.Region)){ // Adapt the condition according to the specificities characterizing your service group
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
```

The application should now correctly take into account new service groups.

## What to do in case of a change of scope?

### In case of a change of column names

If a column name changes, just change the value of the column in the utils.py file (TODO 8). All python files use these variables for column names, so the change will be reflected throughout the application.

⚠ Column names in the JavaScript File "dashAgGridFunctions.js" must be changed manually! The JavaScript file is not linked to the variables in the utils.py file ⚠

It may also be necessary to update the user guide with the appropriate new values.

# Cheat sheet

## Callback

### callback decorator
@callback(
    Output(component_id="first_output_2", component_property="children"),
    Input(component_id="button_2", component_property="n_clicks")
)

Will always have at least 1 output and 1 input
The input & output both have component id & property
The component id says what component we are referring to
The component property say what property of that component we are listening to

### callback function
Every input in the callback decorator has to be represented as an argument in the callback function and in the same order

### allow_duplicate property
The allow_duplicate property of an output function in a callback decorator allows you to have multiple callbacks that update the same output. This can be particularly useful when you need different callbacks to update the same component under different conditions.

## prevent_initial_call = True
Presents in callback decorators, to prevent callbacks from firing when their inputs initially appear in the layout of your Dash application

## dcc.Store component 
They are defined in the layout. Allows storing information in web browser memory without displaying it in the UI.
The storage_type property set to 'session' means data is cleared once the browser quits.

## State component 
Used to pass the current state of a component without triggering the callback.
Useful to access the value of a component without excecuting the callback every time the component's value changes.

## n_clicks
(number; default 0): An integer that represents the number of times that this element has been clicked on.

## id_factory
In Python Dash, the id_factory function is used to generate unique IDs for components, especially useful in multi-page applications where components might otherwise have overlapping IDs. This function helps ensure that each component has a unique identifier, which is crucial for the proper functioning of callbacks.
Returns a function that appends the page name to the component ID (ie. "page1-component1"), ensuring uniqueness across different pages.

## Dash AG Grid
### filterModel
The filterModel property represents the state of filters applied to the grid’s columns. This property is essential for capturing and manipulating the filter state within Dash callbacks. The filterModel is a dictionary where each key corresponds to a column ID, and the value is another dictionary specifying the filter type and criteria.
### columState
The columnState property is used to manage the state of the grid’s columns. This includes properties like column order, visibility, width, and sort state. The columnState can be retrieved and set, allowing for dynamic updates and persistence of the grid’s configuration.
### example of properties belonging to a column in AG Grid

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

#### valueFormatter
 This is a property used in grid configurations to define how the data in a specific column is formatted before being displayed.
 The expression "function": "params.value" indicates that the value of the cell should be directly displayed as it is, without any transformation. Essentially, it is returning the raw value of the cell without formatting it in any special way.

## dbc.Modal
To add dialogs to your app for lightboxes, user notifications, or completely custom content.

## Code optimization
dashboard_current_year, dashboard_next_year, dashboard_next_next_year are written with the same code
Only the year changes --> should be factorized in on sigle file.

## os library
The os library in Python provides a way to interact with the operating system in a portable manner. It includes functions for:

-File and Directory Operations: Creating, removing, and changing directories, as well as handling file paths.
-Environment Variables: Accessing and modifying environment variables.
-Process Management: Managing processes, including spawning new processes and retrieving process IDs.
-System Information: Fetching information about the operating system, such as the current working directory and user information.

## dataframe.py
Name of services are defined 4 times:
2 for ope & functional dashboards
+ in 2 functions get_dataframe_functional & get_dataframe#   S T _ a p p _ t r a i n i n g  
 