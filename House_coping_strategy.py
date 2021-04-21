import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],suppress_callback_exceptions=True, title = 'Food & Nutrition Dashboard')



server = app.server

# @server.route('/favicon.ico')
# def favicon():
#     return flask.send_from_directory(os.path.join(server.root_path, 'static'),
#                                      'favicon.ico')



#importing all the sheets
hdds = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'HDDS')
fcs = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'fcs')
fcs_detailed =  pd.read_excel("./DFNSD_data/RLA FS Trends.xlsx", sheet_name = 'District Food Insecurity')
pfi = pd.read_excel("./DFNSD_data/RLA FS Trends.xlsx", sheet_name = 'summary')
dfi = pd.read_excel("./DFNSD_data/RLA FS Trends.xlsx", sheet_name = 'DFI')
cattle = pd.read_excel("./DFNSD_data/Livestock ownership.xlsx", sheet_name = 'livestock')



# province = list(hdds.province.drop_duplicates())
# consuption_year = list(hdds.columns)[3:]
# district = list(fcs['District'].drop_duplicates())




#nav header
dashboard_header = html.Div(
            id="header",
            children=[
        dbc.NavbarSimple(
            children=[
                # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                html.Div(
                    children=[
                        html.H3(
                            id="header_text",
                            children="FOOD & NUTRITION COUNCIL DASHBOARD",
                            style={'color':'#808000', 'display': 'inline-block','textAlign': 'center'}
                        )
                    ]
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("OPTIONS", header=True),
                        dbc.DropdownMenuItem("Change Password", href="#"),
                        dbc.DropdownMenuItem("Settings", href="#"),
                        dbc.DropdownMenuItem("FNC Logout", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Options",
                ),
            ],
            # brand="FOOD & NUTRITION COUNCIL DASHBOARD",
            brand_href="#",
            color="dark",
            dark=True,
            sticky="top",
            className="font-weight-bold"
        )],
        )

#my tabs
def my_tabs():
    return (
        html.Div(
        id="my_tab",
        children=[
               dbc.Tabs(
                   [
                       dbc.Tab(label="Household Coping Straregies", tab_id="tab_1"),
                       dbc.Tab(label="Food Insecurity Score", tab_id="tab_2"),
                       dbc.Tab(label="Livestock Ownership", tab_id="tab_3"),
                   ],
                   id="tabs",
                   active_tab="tab_1",
               ),
               html.Div(id="tab-content", className="p-4"),
        ]
        )
    )



###########################################
def consuption_graph():
    df = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'Consumpt')
    df['Meals']= df['Meals'].round()
    SUMARY = df.groupby(['YEAR'])['Meals'].value_counts()

    SUMARY= SUMARY.unstack('Meals')
    SUMARY= SUMARY.reset_index()
    SUMARY.columns = ['year', 'meal2', 'meal3']

    SUMARY= SUMARY.sort_values(by= ['year'], ascending = False)
    SUMARY= SUMARY[:5]
    x = SUMARY['year']
    y1 = list(SUMARY.meal2)
    y2 = list(SUMARY.meal3)

    fig = go.Figure(data=[go.Bar(name='2 meals', x=x, y=y1),
        go.Bar(name='3 meals', x=x, y=y2)
        ])
        # Change the bar mode
    fig.update_layout(
        title={
                'text' : f"<b>consumption by meals and year</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,
        barmode='group',

        xaxis=dict(title='<b>Year</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>No. OF DSTRICTS</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )

    return (dcc.Graph(
        id='consuption-graph',
        figure = fig
    ))

##################################################

def food_consumption_score_table():
    df = fcs_detailed
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.DistPCode, df.District_Name, df['FS_2016-17'], df['FS_2017-18'], df['FS_2018-19'], df['FS_2019-20'],df['FS_2020-21'], df['Province']],
               fill_color='lavender',
               align='left'))
    ])
    fig.update_layout(
        title = {
            'text' : "<b>FOOD CONSUMPTION SCORE TABLE</b>",
            'y' : 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_color="red",
        title_font_size=12,
        xaxis_title='Year',
        yaxis_title='Food Consumption Score',
        autosize = True,
        width = 1000,
        height = 450)

    return(dcc.Graph(
        id='fcs_detailed_table',
        figure = fig
    ))

###################
#district food inseurity
def district_food_insecurty_summary_graph(df):
    fig = px.line(df, x="Year", y='Insecurity', title='Summary of National Food Insecurity', color = 'Province_Name')
    fig.update_layout(
        title={
                'text' : f"<b>Summary of National Food Insecurity</b>".upper(),
                # 'text' : f"<b>FOOD CONSUMPTION SCORE {fsc_districts} district</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='closest',
        
        autosize = True,
        width = 700,
        height = 450,

        xaxis=dict(title='<b>Year</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>Food Insecurity Score</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.01,
                         y=1.14,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=9,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return(dcc.Graph(
        id='pfi_summary_graph',
        figure = fig
    ))

#first tab
#first tab
def first_tab():
    return (dbc.CardBody(
            children=[

                #first main row for top graphs
                dbc.Row(
                    id="top_outer_row",
                    children=[
                        # first column with consumption
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_div",
                                    children=[
                                        dbc.Col(consuption_graph(), md=6)
                                    ],

                                )
                            ]
                        ),
                        # second column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_score_div",
                                    children=[
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='fsc_districts_input',
                                                options=[{'label': i, 'value': i} for i in list(fcs['District'].drop_duplicates())],
                                                value='Gutu'
                                            ),
                                            width="4",
                                            className="mydropdown"
                                        ),
                                        dbc.Col(dcc.Graph(id='fcs_graph'), md=6)


                                    ]
                                )
                            ]
                        ),
                    ]
                ),

                html.Hr(),

                #second main row for top graphs
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #row for the dropdowns
                                        dbc.Row([
                                            # dropdown 1
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(
                                                        id='hdds_province_input',
                                                        multi=False,
                                                        clearable=True,
                                                        value="masvingo",
                                                        placeholder='Select Province',
                                                        options=[{'label': i, 'value': i} for i in list(hdds.province.drop_duplicates())],
                                                        
                                                    ),
                                                ]
                                            ),
                                            # dropdown 2
                                             dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[

                                                    dcc.Dropdown(
                                                        id='hdds_year_input',
                                                        multi=False,
                                                        clearable=True,
                                                        value=2012,
                                                        placeholder='Select Year',
                                                        options=[{'label': i, 'value': i} for i in list(hdds.columns)[3:]],
                                                        
                                                    )
                                                ]
                                            ),
                                        ]
                                        ),

                                    ],
                                    style={'width': '75%', 'float': 'right', 'display': 'inline-block'}
                                )
                            ]
                        ),
                        
                    ]
                ),
                ################
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="hdds_div1",
                                    children=[
                                    #row for the dropdowns

                                    #the graph
                                    dbc.Col(dcc.Graph(id='household_score_graph'), md=6),

                                    ]
                                )
                            ]
                        ),
                        #fourth column
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="hdds_div1",
                                    children=[
                                        dbc.Col(dcc.Graph(id='hdds_pie_chart'), md=6)
                                    ]

                                )
                            ]
                        )
                    ]
                )

            ]
        ))

###############


# div for 2nd tab
food_insecurity_tab = html.Div(
    children=[
        html.Div(
            children=[
            #first row
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #row for the dropdowns
                                        dbc.Row([
                                            # dropdown 1
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(id='pfi_province_input',
                                                           multi=False,
                                                           clearable=True,
                                                           value='Manicaland',
                                                           placeholder='Select Province',
                                                           options=[{'label': c, 'value': c} for c in (pfi['Province_Name'].unique())]
                                                           ),
                                                ]
                                            ),
                                            # dropdown 2
                                        ]
                                        ),

                                    ],
                                    style={'width': '50%', 'float': 'right', 'display': 'inline-block'}
                                )
                            ]
                        ),
                        
                    ]
                ),

            #second row 
                dbc.Row(
                    children=[
                        # 1st column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_score_div",
                                    children=[
                                        dbc.Col(district_food_insecurty_summary_graph(pfi), md=6)
                                    ],

                                )
                            ]
                        ),
                        #2nd
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_score_div",
                                    children=[

                                        dbc.Col(dcc.Graph(id='pfi_summary_graph'), md=6)

                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                html.Hr(),
                #third main row for top graphs
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #row for the dropdowns
                                        dbc.Row([
                                            # dropdown 1
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(id='dfi_province_input',
                                                                     multi=False,
                                                                     clearable=True,
                                                                     value='Manicaland',
                                                                     placeholder='Select Province',
                                                                     options=[{'label': c, 'value': c} for c in (dfi['Province'].unique())]
                                                                ),
                                                ]
                                            ),
                                            # dropdown 2
                                        ]
                                        ),

                                    ],
                                    style={'width': '65%', 'float': 'right', 'display': 'inline-block'}
                                )
                            ]
                        ),
                        
                    ]
                ),

                #third row
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #the graph
                                    dbc.Col(dcc.Graph(id='dfi_bar_graph'), md=6),

                                    ]
                                )
                            ]
                        ),
                        #fourth column
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="dfi_line_div",
                                    children=[
                                        dbc.Col(dcc.Graph(id='dfi_line_graph'), md=6)
                                    ]

                                )
                            ]
                        )
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    children=[
                        #2nd
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="detailed_table_div",
                                    children=[

                                        dbc.Col(food_consumption_score_table(), md=6)

                                    ]
                                )
                            ]
                        ),
                    ]
                ),

            ]
        )
    ]

)


###############
# div for 3rd tab
livestock_ownership_tab = html.Div(
    children=[
        html.Div(
            children=[
            #first row
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #row for the dropdowns
                                        dbc.Row([
                                            # dropdown 1 
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(id='livestock_type_input',
                                                         multi=False,
                                                         clearable=True,
                                                         value='Cattle',
                                                         placeholder='Livestock Type',
                                                         options=[{'label': c, 'value': c} for c in (cattle['Type'].unique())]
                                                         ),
                                                ]
                                            ),
                                            #second drop down
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(id='cattle_district_input',
                                                         multi=False,
                                                         clearable=True,
                                                         value='Buhera',
                                                         placeholder='Select District',
                                                         options=[{'label': c, 'value': c} for c in (cattle['District'].unique())]
                                                         ),
                                                ]
                                            ),
                                            # dropdown 2
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(id='range_cattle_input',
                                                         multi=False,
                                                         clearable=True,
                                                         value='Zero',
                                                         placeholder='Select Category',
                                                         options=[{'label': c, 'value': c} for c in (list(cattle.columns)[2:])]
                                                         ),
                                                ]
                                            )
                                        ]
                                        ),

                                    ],
                                    style={'width': '90%', 'float': 'left', 'display': 'inline-block'}
                                )
                            ]
                        ),
                        
                    ]
                ),

                #second row
                dbc.Row(
                    children=[
                        # 1st column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_score_div",
                                    children=[
                                        
                                        dbc.Col(dcc.Graph(id='cattle_district_graph'), md=6)
                                    ]
                                )
                            ]
                        ),

                        #2nd
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="consumption_score_div",
                                    children=[
                                        dbc.Col(dcc.Graph(id='cattle_pie_chart'), md=6)
                                    ],

                                )
                            ]
                        ),
                    ]
                ),

                #third main row for top graphs
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-12",
                            children=[
                                html.Div(
                                    id="dfi_div1",
                                    children=[
                                    #row for the dropdowns
                                        dbc.Row([
                                            # dropdown 1
                                            dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[
                                                    dcc.Dropdown(
                                                        id='livestock_type',
                                                        multi=False,
                                                        clearable=True,
                                                        value="Cattle",
                                                        placeholder='livestock type',
                                                        options=[{'label': i, 'value': i} for i in list(cattle['Type'].unique())],
                                                        
                                                    ),
                                                ]
                                            ),
                                            # dropdown 2
                                             dbc.Col(
                                                className="mydropdown",
                                                width="4",
                                                children=[

                                                    dcc.Dropdown(
                                                        id='livestock_year_input',
                                                        multi=False,
                                                        clearable=True,
                                                        value=2012,
                                                        placeholder='Select Year',
                                                        options=[{'label': i, 'value': i} for i in list(cattle['Year'].unique())],
                                                        
                                                    )
                                                ]
                                            ),
                                        ]
                                        ),

                                    ],
                                    style={'width': '75%', 'float': 'right', 'display': 'inline-block'}
                                )
                            ]
                        ),
                        
                    ]
                ),
                ################
                dbc.Row(
                    id="top_outer_second_row",
                    children=[
                    # third column with food consumption score
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="hdds_div1",
                                    children=[
                                    #row for the dropdowns

                                    #the graph
                                    dbc.Col(dcc.Graph(id='national_livestock_pie_chart'), md=6),

                                    ]
                                )
                            ]
                        ),
                        #fourth column
                        dbc.Col(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    id="hdds_div1",
                                    children=[
                                        dbc.Col(dcc.Graph(id='hdds_pie_chart'), md=6)
                                    ]

                                )
                            ]
                        )
                    ]
                ),
                
            ]
        )
    ]

)

#app layout
app.layout =html.Div(
    children=[
        dashboard_header,
        my_tabs(),
    ],
)



@app.callback(
    Output('fcs_graph', 'figure'),
    Input('fsc_districts_input', 'value')
)  
def update_fsc_district_graph(fsc_districts_input):
    if fsc_districts_input == None:
        fsc_districts_input = "Gutu"
    df = fcs[fcs['District']==fsc_districts_input]
 
    fig = go.Figure()
    color =['rgb(112, 123, 14)','rgb(112, 123, 124)', 'rgb(214, 137, 16)']
    i = 0 
    for col in df.columns[3:-1]:
        fig.add_trace(go.Bar(x=df.Year, y=df[col].values,
                                 name = col,marker=dict(color=color[i])))
        i+=1
    # format and show figure
    fig.update_layout(
        title={
                'text' : f"<b>FOOD CONSUMPTION SCORE FOR {fsc_districts_input} district</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,

        xaxis=dict(title='<b>Year</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>Food Consumption Score</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig


############################################################
#household_graph

@app.callback(
    Output('household_score_graph', 'figure'),
    Input('hdds_province_input', 'value'),
    Input('hdds_year_input', 'value')
)  
def update_hdds_graph(province_value, consyear_value):
    df = hdds
    if province_value == None:
        province_value = "masvingo"
    if consyear_value == None:
        consyear_value = 2012
    df = df[df['province']==province_value]
    x = list(df['District_Name'])
    y = list(df[consyear_value].round())
    fig = px.bar( x=x,  y=y, text = y)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto', marker_color='rgb(123, 192, 67)')

    fig.update_layout(
        title={
                'text' : f"<b>{str(consyear_value)} HDDS for {province_value} Province.</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,

        xaxis=dict(title='<b>District</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>Food Consumption Score</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig


#############################################
#HDDS PIE CHART
@app.callback(
    Output('hdds_pie_chart', 'figure'),
    Input('hdds_province_input', 'value'),
    Input('hdds_year_input', 'value')
)  
def hdds_pie_chart(province_value, consyear_value):
    df = hdds
    if province_value == None:
        province_value = "masvingo"
    if consyear_value == None:
        consyear_value = 2012
    df = df[df['province']==province_value]
    x = list(df['District_Name'])
    y = list(df[consyear_value].round())
    
    fig = px.pie(df, values=y, names=x,
                     title='District Score Summary'
                     )

    fig.update_layout(
        title={
                'text' : f"<b>{str(consyear_value)} HDDS Pie Chart for {province_value} Province.</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         # hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,
 
        legend=dict(title='',
                         x=0.1,
                         y=1.18,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig

#Food Insecurity by Province
@app.callback(
    Output('pfi_summary_graph', 'figure'),
    Input('pfi_province_input', 'value')
)  
def consumption_Province_summary_graph_bar(pfi_province_input):
    if pfi_province_input == None:
        pfi_province_input = "Manicaland"
    insec_province=pfi[pfi["Province_Name"]==pfi_province_input]
    fig = px.bar(insec_province, x="Year", y="Insecurity", title='Summary of National Food Insecurity', text="Insecurity")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout( uniformtext_minsize=8, uniformtext_mode='hide')
    fig.add_trace(go.Scatter(x=insec_province.Year, y=insec_province.Insecurity, name= 'FIS', marker_color='rgb(104, 204, 104)'))
    # # format and show figure
    fig.update_layout(
            title={
                    'text' : f"<b>{pfi_province_input} Food Insecurity Per Year by District</b>".upper(),
                    # 'text' : f"<b>FOOD CONSUMPTION SCORE {fsc_districts} district</b>".upper(),
                    'y': 0.93,
                    'x': 0.43,
                    'xanchor': 'center',
                    'yanchor': 'top'},
            titlefont={'family': 'Oswald',
                            'color': 'rgb(230, 34, 144)',
                            'size': 12},

             hovermode='closest',

            autosize = True,
            width = 700,
            height = 450,

            xaxis=dict(title='<b>Year</b>',
                            color='rgb(230, 34, 144)',
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(104, 204, 104)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(17, 37, 239)'
                            )

                    ),

            yaxis=dict(title='<b>Food Insecurity Score</b>',
                            color='rgb(230, 34, 144)',
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(104, 204, 104)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                               family='Arial',
                               size=12,
                               color='rgb(17, 37, 239)'
                            )

                    ),
            legend=dict(title='',
                             x=0.01,
                             y=1.14,
                             orientation='h',
                             bgcolor='rgba(255, 255, 255, 0)',
                             traceorder="normal",
                             font=dict(
                                  family="sans-serif",
                                  size=9,
                                  color='#000000')),

                             legend_title_font_color="green",
                             uniformtext_minsize=12,
                             uniformtext_mode='hide',


                     )
    return fig




#District food insecurity bar graph
@app.callback(
    Output('dfi_bar_graph', 'figure'),
    Input('dfi_province_input', 'value'),
)  
def district_food_insecurity_Bargraph(dfi_province_input):
    if dfi_province_input == None:
        dfi_province_input = "Mash west"
    df=dfi[dfi["Province"]==dfi_province_input]
    fig = px.bar(df, x="Year", y="Insecurity", color = 'District_Name', barmode='group')
    fig.update_layout(
            title={
                    'text' : f"<b>{dfi_province_input} Food Insecurity</b>".upper(),
                    'y': 0.98,
                    'x': 0.43,
                    'xanchor': 'center',
                    'yanchor': 'top'},
            titlefont={'family': 'Oswald',
                            'color': 'rgb(230, 34, 144)',
                            'size': 12},

             hovermode='closest',

            autosize = True,
            width = 700,
            height = 450,

            xaxis=dict(title='<b>Year</b>',
                            color='rgb(230, 34, 144)',
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(104, 204, 104)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(17, 37, 239)'
                            )

                    ),

            yaxis=dict(title='<b>Food Insecurity Score</b>',
                            color='rgb(230, 34, 144)',
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='rgb(104, 204, 104)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                               family='Arial',
                               size=12,
                               color='rgb(17, 37, 239)'
                            )

                    ),
            legend=dict(title='',
                             x=0.01,
                             y=1.11,
                             orientation='h',
                             bgcolor='rgba(255, 255, 255, 0)',
                             traceorder="normal",
                             font=dict(
                                  family="sans-serif",
                                  size=9,
                                  color='#000000')),

                             legend_title_font_color="green",
                             uniformtext_minsize=12,
                             uniformtext_mode='hide'

                     )
    return fig


################################
#District food insecurity line graph

@app.callback(
    Output('dfi_line_graph', 'figure'),
    Input('dfi_province_input', 'value'),
)  
def district_food_insecurity_Linegraph(dfi_province_input):
    if dfi_province_input == None:
        dfi_province_input = "Mash west"
    df=dfi[dfi["Province"]==dfi_province_input]
    fig = px.line(df, x="Year", y="Insecurity", title='Summary of National Food Insecurity', color = 'District_Name')
    fig.update_layout(
        title={
                'text' : f"<b>{dfi_province_input} Food Insecurity</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='closest',
        
        autosize = True,
        width = 700,
        height = 450,

        xaxis=dict(title='<b>Year</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>Food Insecurity Score</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.01,
                         y=1.14,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=9,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig

#############################
#Livestock Ownership
@app.callback(
    Output('cattle_district_graph', 'figure'),
    Input('livestock_type_input', 'value'),
    Input('cattle_district_input', 'value'),
    Input('range_cattle_input', 'value'),
)
def cattle_graph(livestock_type_input,cattle_district_input, range_cattle_input):
    if cattle_district_input == None:
        cattle_district_input = "Buhera"
    if range_cattle_input == None:
        range_cattle_input = "Zero"
    if livestock_type_input == None:
        livestock_type_input = "Cattle"
    livestock_type= cattle[cattle['Type']==livestock_type_input]
    df=livestock_type[livestock_type["District"]==cattle_district_input]
    fig = px.bar(df, x="Year", y=range_cattle_input)
    fig.add_trace(go.Scatter(x=df.Year, y=df[range_cattle_input], name= 'LSC', marker_color='rgb(200, 204, 20)'))

    fig.update_layout(
        title={
                'text' : f"<b>{livestock_type_input} Ownership {cattle_district_input} District with {range_cattle_input} Per Year</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='closest',
        
        autosize = True,
        width = 700,
        height = 450,

        xaxis=dict(title='<b>Year</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

        yaxis=dict(title='<b>Number of households</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
        legend=dict(title='',
                         x=0.01,
                         y=1.05,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=9,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig

#cattle Pie chat
@app.callback(
    Output('cattle_pie_chart', 'figure'),
    Input('livestock_type_input', 'value'),
    Input('cattle_district_input', 'value'),
    Input('range_cattle_input', 'value')
)
def cattle_pie_chart(livestock_type_input,cattle_district_input, range_cattle_input):
    if cattle_district_input == None:
        cattle_district_input = "Buhera"
    if range_cattle_input == None:
        range_cattle_input = "Zero"
    if livestock_type_input == None:
        livestock_type_input = "Cattle"
    livestock_type= cattle[cattle['Type']==livestock_type_input]
    df=livestock_type[livestock_type["District"]==cattle_district_input]
    x = list(df.Year)
    y = list(df[range_cattle_input])
    
    fig = px.pie(df, values=y, names=x,
                     title='Cattle groups comparison'
                     )

    fig.update_layout(
        title={
                'text' : f"<b>{livestock_type_input} Ownership {cattle_district_input} District with {range_cattle_input} Per Year</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,
 
        legend=dict(title='',
                         x=0.1,
                         y=1.18,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig

#national livestock pie chart
@app.callback(
    Output('national_livestock_pie_chart', 'figure'),
    Input('livestock_type', 'value'),
    Input('livestock_year_input', 'value')
)
def livestock_district_pie_chart(livestock_type,  livestock_year_input):
    if livestock_type == None:
        livestock_type = "Cattle"
    if livestock_year_input == None:
        livestock_year_input = 2012
    df = cattle.groupby(['Year','Type'])['Zero', 'One_to_two', 'Three_to_five', 'More_than_five'].sum()
    df = df.reset_index()
    
    df = df[df['Year']==livestock_year_input]
    df = df[df['Type']==livestock_type]
    
    y = list(df.values[0][2:])
    x = list(df.columns[2:])
    fig = go.Figure(data=[go.Pie(labels=x, values=y, hole=.3, title='livestock groups comparison')])
    # fig = px.pie(df, values=y, names=x,
    #                  title='livestock groups comparison'
    #                  )

    fig.update_layout(
        title={
                'text' : f"<b>{livestock_year_input} {livestock_type} national comparison.</b>".upper(),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
        titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 12},

         hovermode='x',
        
        autosize = True,
        width = 700,
        height = 450,
 
        legend=dict(title='',
                         x=0.1,
                         y=1.18,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide'

                 )
    return fig

#tabs switch case
@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab_1":
        return first_tab()
    elif at == "tab_2":
        return food_insecurity_tab
    elif at == "tab_3":
        return livestock_ownership_tab



if __name__ == '__main__':
    app.run_server(debug=True, port = 8053)