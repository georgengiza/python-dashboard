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


#data modeling
df = pd.read_excel("./DFNSD_data/RLA FS Trends.xlsx", sheet_name = 'District Food Insecurity')
del df['DistPCode']
years = list(df.columns)[1:]

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
                id='year-select',
                options=[{'label': i, 'value': i} for i in years],
                value='FS_2016-17'
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
                dbc.Col(dcc.Graph(id='indicator-graphic'), md=6)
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
                dbc.Col(dcc.Graph(id='household-graphic'), md=6)
            ],
            align="center",
        )
    ],
    fluid=True,
)




@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('year-select', 'value')
)  
def analysis_graph(year_value):
    if year_value == None:
        year_value = "FS_2016-17"
    top5_2016 = df.sort_values(by=year_value, ascending= False)
    bottom5 = df.sort_values(by=year_value, ascending= True)
    top5_2016 = top5_2016[:5][['District_Name',year_value]]
    bottom5 = bottom5[:5][['District_Name',year_value]]

    fig = px.bar(top5_2016, x=top5_2016["District_Name"], y=top5_2016[year_value],
             labels=dict(x="District_Name", y="Value"))
    fig.add_bar(x=bottom5["District_Name"], y=bottom5[year_value], name="Bottom5")
    fig.update_layout(title = {'text' : "Top 5 vs Bottom 5",'y' : 0.9,'x': 0.5,
            'xanchor': 'center','yanchor': 'top'},xaxis_title='District Name', yaxis_title='Insecurity',
            barmode='group',autosize = True,width = 700,height = 400)
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
    app.run_server(debug=True, port = 8052)