import dash
from dash import Dash, dcc, Output, Input, html, State, MATCH
from datetime import datetime as dt
from datetime import date
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np  
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# improt data
df = pd.read_excel(DATA_PATH.joinpath("chat_analyze.xlsx"))
df = df.dropna()


mytitle = dcc.Markdown(children = '# Team Analysis')
mygraph = dcc.Graph(figure={})

df['Date'] = pd.to_datetime(df['Date'])

# date_picker = dcc.DatePickerRange(id='my_date_picker',
#                                   start_date=df['Date'].min(),
#                                   end_date=df['Date'].max() ,
#                                   start_date_placeholder_text="Start Period",
#                                   end_date_placeholder_text="End Perdiod",
#                                   calendar_orientation='horizontal',
#                                   clearable=False,
#                                   min_date_allowed=dt(2022, 1, 1),
#                                   initial_visible_month=df['Date'].min(),
#                                   minimum_nights=0,
#                                   persistence=True,
#                                   persisted_props=['start_date', 'end_date'],
#                                   persistence_type='local',
#                                   updatemode='bothdates')

layout = html.Div([
    mytitle,
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    html.Div(id='container', children=[])
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': '# Topics', 'value': 'bar'},
                         {'label': '# Questions', 'value': 'line'},
                         {'label': '% Team', 'value': 'pie'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df['Team'].unique())],
                multi=True,
                value=["Samuela", "Chris"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['Category']],
                value='Category',
                clearable=False
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                options=[{'label': 'All Employees', 'value': 'All'}] + [{'label': n, 'value': n} for n in df['Employee'].unique()],
                value='All',
                clearable=True,
                searchable=True,
                placeholder="Select Employee"
            ),
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-s', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(s_value, ctg_value, num_value, chart_choice):
    print(s_value)
    dff = df[df['Team'].isin(s_value)]
    if chart_choice == 'bar':
        if num_value == "All":
            fig = px.bar(dff, x= dff['Category'].unique(), y= dff['Category'].value_counts(), title="Amount of questions per Category")
        else:
            dff = dff[dff['Employee'] == num_value]
            fig = px.bar(dff, x= dff['Category'].unique(), y= dff['Category'].value_counts(), title="Amount of questions per Category")
        
        return fig
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            date_count = dff['Date'].value_counts().sort_index()
            date_unique = dff['Date'].unique()
            print(date_count)
            fig = px.line(dff, x= date_unique, y= date_count, title="Questions per day overview")
            return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff, names=dff['Team'].unique(), values=dff['Team'].value_counts(), hole=0.4, title="Percent of Questions compared in Teams")
        return fig
