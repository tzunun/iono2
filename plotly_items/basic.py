import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Output, Input
import plotly.graph_objs as go 
import plotly.express as px
import numpy as np

gapminder = px.data.gapminder()

tips = px.data.tips()
col_options = [dict(label=x, value=x) for x in tips.columns]
dimensions = ["x", "y", "color", "facet_col", "facet_row"]


app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

# Create DATA

np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

# Display graphs inside the Div
#app.layout = html.Div([graph1, graph2])
#app.layout = html.Div([
#    dcc.Input(id='my-id', value='')
#])

app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
        dcc.Graph(id="graph2", style={"width": "75%", "display": "inline-block"}),
    ]
)

z = [[None, None, None, 12, 13, 14, 15, 16],
     [None, 1, None, 11, None, None, None, 17],
     [None, 2, 6, 7, None, None, None, 18],
     [None, 3, None, 8, None, None, None, 19],
     [5, 4, 10, 9, None, None, None, 20],
     [None, None, None, 27, None, None, None, 21],
     [None, None, None, 26, 25, 24, 23, 22]]

projection = 'orthographic'

import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure():
    fig = go.Figure()
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)