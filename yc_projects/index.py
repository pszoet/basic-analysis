from dash import html, dcc, Input, Output

# Connecting main app
from app import app
from app import server

# Import apps
from apps import chat_analysis, games


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Video Games | ', href='/apps/games'),
        dcc.Link('Multi Chart, All Dates', href='/apps/chat_analysis'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/games':
        return games.layout
    elif pathname == '/apps/chat_analysis':
        return chat_analysis.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)