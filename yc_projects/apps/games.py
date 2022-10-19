from turtle import color
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# Folder Pathing
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfps = pd.read_csv(DATA_PATH.joinpath("video_game_sales.csv"))
sales_list = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]

#Layout games page
layout = html.Div([
    html.H1('Game Sales', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='genre-dropdown', value='Strategy', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(dfps.Genre.astype(str).unique())]
        ), className='six columns'),

        html.Div(dcc.Dropdown(
            id='sales-dropdown', value='EU_Sales', clearable=False,
            persistence=True, persistence_type='memory',
            options=[{'label': x, 'value': x} for x in sales_list]
        ), className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-bar', figure={}),
])

# callbacks
@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)
def display_value(genre_chosen, sales_chosen):
    dfps_fltrd = dfps[dfps['Genre'] == genre_chosen]
    dfps_fltrd = dfps_fltrd.nlargest(15, sales_chosen)
    fig = px.bar(dfps_fltrd, x='Name', y=sales_chosen, color='Publisher')
    fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig