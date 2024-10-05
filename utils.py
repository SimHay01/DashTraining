# TODO : 8
#Maintenance variables. Modify the value of a variable here to modify it in the entire program.
service_name="Service Name"
service_code="Service Code"
role="Role"
region="Region"
info="Info"

Q1_WL="Q1_WL"
Q2_WL="Q2_WL"
Q3_WL="Q3_WL"
Q4_WL="Q4_WL"
H1_WL="1H_WL"
H2_WL="2H_WL"
AVG_WL="AVG_WL"

Q1_HC="Q1_HC"
Q2_HC="Q2_HC"
Q3_HC="Q3_HC"
Q4_HC="Q4_HC"
H1_HC="1H_HC"
H2_HC="2H_HC"
AVG_HC="AVG_HC"

Q1_HC_TOPS="Q1_HC"
Q2_HC_TOPS="Q2_HC"
Q3_HC_TOPS="Q3_HC"
Q4_HC_TOPS="Q4_HC"
H1_HC_TOPS="1H_HC"
H2_HC_TOPS="2H_HC"
AVG_HC_TOPS="AVG_HC"

Q1_110AC="Q1_110A"
Q2_110AC="Q2_110A"
Q3_110AC="Q3_110A"
Q4_110AC="Q4_110A"
H1_110AC="1H_110A"
H2_110AC="2H_110A"
AVG_110AC="AVG_110A"

Q1_AD10C="Q1_AD10"
Q2_AD10C="Q2_AD10"
Q3_AD10C="Q3_AD10"
Q4_AD10C="Q4_AD10"
H1_AD10C="1H_AD10"
H2_AD10C="2H_AD10"
AVG_AD10C="AVG_AD10"

Q1_TOPS="1Q_Tops"
Q2_TOPS="2Q_Tops"
Q3_TOPS="3Q_Tops"
Q4_TOPS="4Q_Tops"
H1_TOPS="1H_Tops"
H2_TOPS="2H_Tops"
AVG_TOPS="AVG_Tops"

Q1_TOPS_110A="1Q_Tops_110A"
Q2_TOPS_110A="2Q_Tops_110A"
Q3_TOPS_110A="3Q_Tops_110A"
Q4_TOPS_110A="4Q_Tops_110A"
H1_TOPS_110A="1H_Tops_110A"
H2_TOPS_110A="2H_Tops_110A"
AVG_TOPS_110A="AVG_Tops_110A"

Q1_TOPS_AD10="1Q_Tops_AD10"
Q2_TOPS_AD10="2Q_Tops_AD10"
Q3_TOPS_AD10="3Q_Tops_AD10"
Q4_TOPS_AD10="4Q_Tops_AD10"
H1_TOPS_AD10="1H_Tops_AD10"
H2_TOPS_AD10="2H_Tops_AD10"
AVG_TOPS_AD10="AVG_Tops_AD10"

Q1_CONT='1Q_CONT'
Q2_CONT='2Q_CONT'
Q3_CONT='3Q_CONT'
Q4_CONT='4Q_CONT'
H1_CONT='1H_CONT'
H2_CONT='2H_CONT'
AVG_CONT='AVG_CONT'

Q1_WF='1Q_WF'
Q2_WF='2Q_WF'
Q3_WF='3Q_WF'
Q4_WF='4Q_WF'
H1_WF='1H_WF'
H2_WF='2H_WF'
AVG_WF='AVG_WF'

Q1_COVER='1Q_COVER'
Q2_COVER='2Q_COVER'
Q3_COVER='3Q_COVER'
Q4_COVER='4Q_COVER'
H1_COVER='1H_COVER'
H2_COVER='2H_COVER'
AVG_COVER='AVG_COVER'

Q1_GAP='1Q_GAP'
Q2_GAP='2Q_GAP'
Q3_GAP='3Q_GAP'
Q4_GAP='4Q_GAP'
H1_GAP='1H_GAP'
H2_GAP='2H_GAP'
AVG_GAP='AVG_GAP'

Q1_FLEX='1Q_Flex'
Q2_FLEX='2Q_Flex'
Q3_FLEX='3Q_Flex'
Q4_FLEX='4Q_Flex'
H1_FLEX='1H_Flex'
H2_FLEX='2H_Flex'
AVG_FLEX='AVG_Flex'

#Function used to facilitate development and better manage component ids. Source: https://community.plotly.com/t/how-do-we-repeat-element-id-in-multi-page-apps/41339
def id_factory(page: str):
    def func(_id: str):
        """
        Dash pages require each component in the app to have a totally
        unique id for callbacks. This is easy for small apps, but harder for larger 
        apps where there is overlapping functionality on each page. 
        For example, each page might have a div that acts as a trigger for reloading;
        instead of typing "page1-trigger" every time, this function allows you to 
        just use id('trigger') on every page.
        
        How:
            prepends the page to every id passed to it
        Why:
            saves some typing and lowers mental effort
        **Example**
        # SETUP
        from system.utils.utils import id_factory
        id = id_factory('page1') # create the id function for that page
        
        # LAYOUT
        layout = html.Div(
            id=id('main-div')
        )
        # CALLBACKS
        @app.callback(
            Output(id('main-div'),'children'),
            Input(id('main-div'),'style')
        )
        def funct(this):
            ...
        """
        return f"{page}-{_id}"
    return func # Returns a function that appends the page name to the component ID, ensuring uniqueness across different pages.