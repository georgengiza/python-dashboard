import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
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
    ])

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'table':'#ff2400'
}

#title defination
def dashboard_title():
    return(html.H1(
        children='FOOD & NUTRITION DASHBOARD',

        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ))

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
    fig.update_layout(title = {'text' : "consumption by meals and year",'y' : 0.9,'x': 0.5,
            'xanchor': 'center','yanchor': 'top'},xaxis_title='YEAR', yaxis_title='No. OF DSTRICTS',
            barmode='group',autosize = True,width = 580,height = 400)

    return (dcc.Graph(
        id='consuption-graph',
        figure = fig
    ))

##################################################

def food_consumption_score_table():
    df = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'fcs')
    df = df.groupby(['Year','Province'])['Poor', 'Borderline','Acceptable'].sum()
    df = df.reset_index()
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Year, df.Province, df.Poor.round(), df.Borderline.round(), df.Acceptable.round()],
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
        width = 700,
        height = 400)
    return(dcc.Graph(
        id='fcs-table',
        figure = fig
    ))

#data modeling
df = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'fcs')
district = list(df['District'].drop_duplicates())

############
df1 = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'HDDS')
province = list(df1.province.drop_duplicates())
consuption_year = list(df1.columns)[3:]
#app layout 

app.layout = dbc.Jumbotron(
    [
        dashboard_title(),
        html.Hr(),
        dbc.Row(
            [
            dbc.Col( md=6),
            dbc.Col(html.Div([
                dcc.Dropdown(
                id='district-select',
                options=[{'label': i, 'value': i} for i in district],
                value='Gutu'
                )
                ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
                ), 
            md=2)
            

            ],
            align="center",
        )
        ,
        dbc.Row(
            [
                
                dbc.Col(consuption_graph(), md=6),
                dbc.Col(dcc.Graph(id='food_score-graphic'), md=6)
            ],
            align="center",
        ),

        html.Hr(),
        dbc.Row([
            
            dbc.Col(dcc.Dropdown(
                id='province-select',
                options=[{'label': i, 'value': i} for i in province],
                value="masvingo"
                ),
                 md=1),

            dbc.Col(dcc.Dropdown(
                id='consyear-select',
                options=[{'label': i, 'value': i} for i in consuption_year],
                value=2012
                ),
                 md=1)

            ],
            align="center",
        )
        ,
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='household-graphic'), md=6),
                dbc.Col(food_consumption_score_table(), md=6)
            ],
            align="center",
        )
    ],
    fluid=True,
)




@app.callback(
    Output('food_score-graphic', 'figure'),
    Input('district-select', 'value')
)  
def analysis_graph(district_value):
    df = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'fcs')
    if district_value == None:
        district_value = "Gutu"
    df = df[df['District']==district_value]
    cols = list(df.columns[3:6])
    df[cols] = df[cols].round()
    x = list(df['Year'])
    y1 = list(df['Poor'])
    y2 = list(df['Borderline'])
    y3 = list(df['Acceptable'])

    fig = go.Figure()
    for col in df.columns[3:-1]:
        fig.add_trace(go.Bar(x=df.Year, y=df[col].values,
                                 name = col))
    # format and show figure
    fig.update_layout(
        title = {
            'text' : f"<b>FOOD CONSUMPTION SCORE FOR {district_value} district</b>".upper(),
            'y' : 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_color="red",
        title_font_size=12,
        xaxis_title='Year',
        yaxis_title='Food Consumption Score',
        autosize = True,
        width = 620,
        height = 400)
    return fig


############################################################
#household_graph

@app.callback(
    Output('household-graphic', 'figure'),
    Input('province-select', 'value'),
    Input('consyear-select', 'value')
)  
def analysis_graph(province_value, consyear_value):
    df = pd.read_excel("./DFNSD_data/Household Coping Straregies.xlsx", sheet_name = 'HDDS')
    if province_value == None:
        province_value = "masvingo"
    if consyear_value == None:
        consyear_value = 2012
    df = df[df['province']==province_value]
    x = list(df['District_Name'])
    y = list(df[consyear_value].round())
    fig = px.bar( x=x,  y=y)
    fig.update_layout(
    title = {
        'text' : "HDDS Per Province "+str(consyear_value),
        'y' : 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title='District Name',
    yaxis_title='Score',
    autosize = True,
    width = 580,
    height = 400)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)