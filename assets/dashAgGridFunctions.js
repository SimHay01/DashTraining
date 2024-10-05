// Following the documentation found at this link (https://dash.plotly.com/dash-ag-grid/javascript-and-the-grid), 
// we can define custom functions and components in JavaScript/React for an Ag Grid used in a Dash application.
// In this file, you will find at first the "dagfuncs" part which define the custom functions
// and then you will find the "dagcomponentfuncs" which define the custom components


// "Dagfuncs" part, define the custom functions used by a Dash Ag-Grid
var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};


// Display % after value for percentage data (i.e. Flexibility and Coverage)
dagfuncs.valuePercentage = function (params) {
  if (params.data.Info === 'Flexibility %' || params.data.Info === 'Flexibility % with TOPS' || params.data.Info === 'In House Coverage %' || params.data.Info === 'In House Coverage % with TOPS') {
    return params.value + "%";
  }
}

// Display an editing icon for editable lines.
// This icon can be found in the "dagcomponentfuncs" part of this file
dagfuncs.cellRendererSelector = function (params) {
  var dagcomponentfuncs = window.dashAgGridComponentFunctions
           const editableIcon = {
              component: dagcomponentfuncs.editableIcon,
            };
            if ((params.data.Info == "110A TOPs") || (params.data.Info == "AD10 TOPs")) {return editableIcon};
            return undefined;
}

// Exclude global data (i.e. with an ALL value) from the sum of TOPs.
function excludeGlobalData(rowNode,params) {
  if ((rowNode.data.Info === params.data.Info) && ((rowNode.data["Service Name"] !== "CSO") && (rowNode.data["Service Name"] !== "CSO+EGDS") && (rowNode.data.Role !== "ALL") && (rowNode.data.Region !== "ALL"))) {
    return true;
  }
  else {
    return false;
  }
}

dagfuncs.valueGetterDirect110A= function (params){
  if (params.data["% Direct_110A"] == null){
    return "";
  };
  return params.data["Source_110A"]
};
dagfuncs.valueGetterDirectAD10= function (params){
  if (params.data["% Direct_AD10"] == null){
    return "";
  };
  return params.data["Source_AD10"]
};

// Permet d'avoir un fonctionnement par ligne et non par colonne pour l'Ag Grid. 
// En gros, va parcourir à la saisie d'une valeur par l'utilisateur l'ensemble des données correspondantes
// (via a fonction de l'api forEachNode ou forEachNodeAfterFilter) et va recalculer la nouvelle valeur correcte 
// et va la retourner pour l'afficher.
// Pour les différentes données globales, il a fallu à chaque énoncer dans les conditions 
// ce qui caractérisait cette donnée globale. Cette logique est à suivre dans le cas ou vous souhaitez rajouter de 
// nouvelles données globales comme un nouveau Département composé de sous-départements (ex: db13 ou db15)
// Prend comme paramètre params (classique), l'année ainsi que le trimestre afin d'aller chercher les données dans 
// la bonne colonne. 
dagfuncs.valueGetter = function (params,year,quarter) {
  var fieldName = year + " Q" + quarter;

  if ((params.data.Info == "110A TOPs") || (params.data.Info == "AD10 TOPs")) {
    let sum = 0;
    // Case of CSO+EGDS / ALL / ALL
    if((params.data['Service Name']== "CSO+EGDS") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (excludeGlobalData(rowNode,params)){
          sum+=rowNode.data[fieldName];
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO+EGDS / ALL / Region
    else if ((params.data['Service Name']== "CSO+EGDS") && (params.data.Role == "ALL")) {
      params.api.forEachNode(function(rowNode) {
        if (params.data.Region==rowNode.data.Region){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO+EGDS / Role / ALL
    else if ((params.data['Service Name']== "CSO+EGDS") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (params.data.Role == rowNode.data.Role){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO+EGDS /role / Region
    else if (params.data['Service Name']== "CSO+EGDS") {
      params.api.forEachNode(function(rowNode) {
        if ((params.data.Role == rowNode.data.Role) && (params.data.Region == rowNode.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of ALL / ALL / ALL
    if((params.data['Service Name']== "ALL") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (excludeGlobalData(rowNode,params)){
          sum+=rowNode.data[fieldName];
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of ALL / ALL / Region
    else if ((params.data['Service Name']== "ALL") && (params.data.Role == "ALL")) {
      params.api.forEachNode(function(rowNode) {
        if (params.data.Region==rowNode.data.Region){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of ALL / Role / ALL
    else if ((params.data['Service Name']== "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (params.data.Role == rowNode.data.Role){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of ALL /role / Region
    else if (params.data['Service Name']== "ALL") {
      params.api.forEachNode(function(rowNode) {
        if ((params.data.Role == rowNode.data.Role) && (params.data.Region == rowNode.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }     
    // Case of CSO / ALL / ALL
    else if((params.data['Service Name']== "CSO") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("BS"))){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO / ALL / Region
    else if ((params.data['Service Name']== "CSO") && (params.data.Role == "ALL")) {
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("BS")) && params.data.Region==rowNode.data.Region){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO / Role / ALL
    else if ((params.data['Service Name']== "CSO") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("BS")) && params.data.Role == rowNode.data.Role){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSO /role / Region
    else if (params.data['Service Name']== "CSO") {
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("BS")) && (params.data.Role == rowNode.data.Role) && (params.data.Region == rowNode.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSU / ALL / ALL
    else if ((params.data['Service Name']=="CSUs") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (rowNode.data["Service Code"].includes("DB17")){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of CSU / ALL / Region
    else if ((params.data['Service Name']=="CSUs") && (params.data.Role == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB17")) && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of Corpo / ALL / ALL
    else if ((params.data['Service Name']=="Corporate Centers") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("DB17")) && !(rowNode.data["Service Code"].includes("BS"))){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of Corpo / ALL / Region
    else if ((params.data['Service Name']=="Corporate Centers") && (params.data.Role == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (!(rowNode.data["Service Code"].includes("DB17")) && !(rowNode.data["Service Code"].includes("BS"))  && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // TODO : 7

    // Case of DB10 / ALL / ALL
    else if ((params.data['Service Name']=="Management Office") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB1000")) || (rowNode.data["Service Code"].includes("DB1001"))){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DB10 / ALL / Region
    else if ((params.data['Service Name']=="Management Office") && (params.data.Role == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (((rowNode.data["Service Code"].includes("DB1000")) || (rowNode.data["Service Code"].includes("DB1001"))) && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
        // Case of BS10 / ALL / ALL
        else if ((params.data['Service Name']=="Evidence Generation and Decision Science") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
          params.api.forEachNode(function(rowNode) {
            if ((rowNode.data["Service Code"].includes("BS10"))){
              if (excludeGlobalData(rowNode,params)){
                sum+=rowNode.data[fieldName];
              }
            }
          });
          params.data[fieldName]=Math.round(sum*10)/10;
          return params.data[fieldName];
        }
        // Case of BS10 / ALL / Region
        else if ((params.data['Service Name']=="Evidence Generation and Decision Science") && (params.data.Role == "ALL")){
          params.api.forEachNode(function(rowNode) {
            if (((rowNode.data["Service Code"].includes("BS10"))) && (rowNode.data.Region == params.data.Region)){
              if (excludeGlobalData(rowNode,params)){
                sum+=rowNode.data[fieldName];
              }
            }
          });
          params.data[fieldName]=Math.round(sum*10)/10;
          return params.data[fieldName];
        }
    // Case of DB13 / ALL / ALL
    else if ((params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
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
    else if ((params.data['Service Name']=="Operational Medical Dvpt & Clinical Doc") && (params.data.Role == "ALL")){
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
    // Case of DB15 / ALL / ALL
    else if ((params.data['Service Name']=="Total Trial Operations") || (params.data['Service Name']=="Clinical Data Management Services") && (params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB15"))){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DB15 / ALL / Region
    else if ((params.data['Service Name']=="Total Trial Operations") || (params.data['Service Name']=="Clinical Data Management Services") && (params.data.Role == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Code"].includes("DB15")) && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of Dpt / All / All
    else if ((params.data.Role == "ALL") && (params.data.Region == "ALL")){
      params.api.forEachNode(function(rowNode) {
        if (rowNode.data["Service Name"] == params.data["Service Name"]){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DPT / ALL / Region
    else if (params.data.Role == "ALL"){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Name"] == params.data["Service Name"]) && (rowNode.data.Region == params.data.Region)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
    }
    // Case of DPT / Role / All
    else if (params.data.Region == "ALL"){
      params.api.forEachNode(function(rowNode) {
        if ((rowNode.data["Service Name"] == params.data["Service Name"]) && (rowNode.data.Role == params.data.Role)){
          if (excludeGlobalData(rowNode,params)){
            sum+=rowNode.data[fieldName];
          }
        }
      });
      params.data[fieldName]=Math.round(sum*10)/10;
      return params.data[fieldName];
      }
  }  

  if (params.data.Info === "Total In-House Workforce - FTEs with TOPs") {   
    let sum = 0; 
    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Total In-House Workforce - FTEs" || rowNode.data.Info === "110A TOPs" || rowNode.data.Info === "AD10 TOPs"){
          sum += rowNode.data[fieldName];          
        }
      }
      
    });
    params.data[fieldName]=Math.round(sum*10)/10;
    return params.data[fieldName];
  } 

  if (params.data.Info === "Total In-House Workforce - Heads with TOPs") {   
    let sum = 0; 
    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Total In-House Workforce - Heads" || rowNode.data.Info === "110A TOPs" || rowNode.data.Info === "AD10 TOPs"){
          sum += rowNode.data[fieldName];          
        }
      }
      
    });
    params.data[fieldName]=Math.round(sum*10)/10;
    return params.data[fieldName];
  } 

  if (params.data.Info === "Total Insourcing - FTEs with TOPs") {   
    let sum = 0; 
    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Total Insourcing - FTEs" || rowNode.data.Info === "110A TOPs" || rowNode.data.Info === "AD10 TOPs"){
          sum += rowNode.data[fieldName];          
        }
      }
      
    });
    params.data[fieldName]=Math.round(sum*10)/10;
    return params.data[fieldName];
  } 

  if (params.data.Info === "Total Insourcing - Heads with TOPs") {   
    let sum = 0; 
    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Total Insourcing - Heads" || rowNode.data.Info === "110A TOPs" || rowNode.data.Info === "AD10 TOPs"){
          sum += rowNode.data[fieldName];          
        }
      }
      
    });
    params.data[fieldName]=Math.round(sum*10)/10;
    return params.data[fieldName];
  } 

  if (params.data.Info === "Gap In-House - FTEs  (Workforce vs Workload) with TOPS") {
    let sum_gap = 0;
    let sum_top = 0;

    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Gap In-House - FTEs (Workforce vs Workload)"){
          sum_gap = rowNode.data[fieldName];
        }
        else if ((rowNode.data.Info == "110A TOPs") || (rowNode.data.Info == "AD10 TOPs")){
          sum_top += rowNode.data[fieldName];
        }
      }       
    });
    params.data[fieldName]=Math.round((sum_gap+sum_top)*10)/10;
    return params.data[fieldName];
  }
  
  if (params.data.Info === "Flexibility % with TOPS"){
    let sum_hc = 0;
    let sum_wf = 0;

    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "Registered Headcount - FTEs"){
          sum_hc += rowNode.data[fieldName];
        }
        else if ((rowNode.data.Info === "Total In-House Workforce - FTEs") || (rowNode.data.Info == "110A TOPs") || (rowNode.data.Info == "AD10 TOPs")){
          sum_wf += rowNode.data[fieldName];            
        }
      }
    })
    if (sum_wf <= 0) {
      params.data[fieldName]=0;
      return params.data[fieldName];
    } else {
      params.data[fieldName]=Math.round(((sum_wf-sum_hc)/sum_wf*100)*10)/10;
      if (params.data[fieldName]<0){
        params.data[fieldName]=0;
      }
      return params.data[fieldName];
    }   
  }

  if (params.data.Info === "In House Coverage % with TOPS"){
    let wl;
    let wf;
    params.api.forEachNodeAfterFilter(function(rowNode) {
      if ((rowNode.data['Service Name']==params.data['Service Name']) && (rowNode.data.Region == params.data.Region) && (rowNode.data.Role == params.data.Role)){
        if (rowNode.data.Info === "In-House Workload - Total FTEs - after PRP & Approved+Not Approved"){
          wl= rowNode.data[fieldName];
        }
        if (rowNode.data.Info === "Total In-House Workforce - FTEs with TOPs") {
          wf= rowNode.data[fieldName];
        }
      }    
    });
    if (wl <= 0){
      params.data[fieldName]=0;
      return params.data[fieldName];
    } else {
      params.data[fieldName]=Math.round((wf/wl*100)*10)/10;
      if (params.data[fieldName]<0){
        params.data[fieldName]=0;
      }
      return params.data[fieldName];
    }
  }
  
  else {
    if (params.data[fieldName]==null){
      params.data[fieldName]= 0;
    }
    return params.data[fieldName];
  }
}


// Creates a custom cell editor allowing the user to enter numbers only (source: https://community.plotly.com/t/use-d3-format-in-java-script-for-dash-ag-grid/74552)

dagfuncs.NumberInput = class {
    // gets called once before the renderer is used
  init(params) {
    // create the cell
    this.eInput = document.createElement('input');
    this.eInput.value = params.value;
    this.eInput.style.height = 'var(--ag-row-height)';
    this.eInput.style.fontSize = 'calc(var(--ag-font-size) + 1px)';
    this.eInput.style.borderWidth = 0;
    this.eInput.style.width = '95%';
    this.eInput.type = "number";
    this.eInput.min = params.min;
    this.eInput.max = params.max;
    this.eInput.step = params.step || "any";
    this.eInput.required =  params.required;
    this.eInput.placeholder =  params.placeholder || "";
    this.eInput.name = params.name;
    this.eInput.disabled = params.disabled;
    this.eInput.title = params.title || ""
  }

  // gets called once when grid ready to insert the element
  getGui() {
    return this.eInput;
  }

  // focus and select can be done after the gui is attached
  afterGuiAttached() {
    this.eInput.focus();
    this.eInput.select();
  }

  // returns the new value after editing
  getValue() {
    return Number(this.eInput.value);
  }

}

// Creates a custom cell editor allowing the user to enter numbers only (source: https://community.plotly.com/t/use-d3-format-in-java-script-for-dash-ag-grid/74552)

dagfuncs.DirectInput = class {
  // gets called once before the renderer is used
  init(params) {
    // create the cell
    this.eInput = document.createElement('input');
    this.eInput.value = params.value;
    this.eInput.style.height = 'var(--ag-row-height)';
    this.eInput.style.fontSize = 'calc(var(--ag-font-size) + 1px)';
    this.eInput.style.borderWidth = 0;
    this.eInput.style.width = '95%';
    this.eInput.type = "text"; // changed to text to handle empty/null values
    this.eInput.setAttribute("pattern", "\\d*"); // only allows number input
    this.eInput.min = 1;
    this.eInput.max = 100;
    this.eInput.step = params.step || "any";
    this.eInput.required = params.required;
    this.eInput.placeholder = params.placeholder || "";
    this.eInput.name = params.name;
    this.eInput.disabled = params.disabled;
    this.eInput.title = params.title || ""
  }

  // gets called once when grid ready to insert the element
  getGui() {
    return this.eInput;
  }

  // focus and select can be done after the gui is attached
  afterGuiAttached() {
    this.eInput.focus();
    this.eInput.select();
  }

  // returns the new value after editing
  getValue() {
    const value = this.eInput.value;
    if (value === '') {
      return null; // return null if input is empty or string
    }

    const number = Number(value);
    if (number < 1) {
      return 1;
    }
    if (number > 100) {
      return 100;
    }
    if (isNaN(number)) {
      return null;
    }

    return number;
  }
}



var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};




dagcomponentfuncs.editableIcon= function(props){
  const url = `https://static.thenounproject.com/png/687044-200.png`;
  return React.createElement('span', {key:"test"}, [
    React.createElement(
      'span',
      {
          style: {},
          key:'oui'
      },
      props.value
  ),
    React.createElement(
        'img',
        {
            style: {height: '15px',paddingLeft: '4px',verticalAlign: 'text-top'},
            src: url,
            key:'non'
        },

    ),
    
  ]);
}

//Composant personnalisé correspondant à la ligne épinglée des dashboards lors de l'aggrégat des données sélectionnées
dagcomponentfuncs.CustomTooltip = function (props) {
    if (props.node.rowPinned === 'bottom') {
      const roleElements = props.data.Role.map((role, index) => 
          React.createElement('div', { key: index }, role)
      );
      
      const info = [
          React.createElement('h5', {}, "Selected rows: "),
          ...roleElements, // Utilisez l'opérateur de décomposition pour inclure tous les éléments de roleElements
      ];
      
      return React.createElement(
          'div',
          {
              style: {
                  border: '2pt solid white',
                  backgroundColor: props.color || 'white',
                  padding: 10,
              },
          },
          info
      );
    };

    return " "; // 
};

