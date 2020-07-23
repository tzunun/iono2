import numpy as np
import pandas as pd
from datetime import datetime as dt
import pathlib

import plotly.graph_objs as go
from mpl_toolkits.basemap import Basemap

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Current working directory, pwd in bash.
path = pathlib.Path('~/Repos/iono2')

earthquakes_columns = ["time_stamp", "latitude", "longitude", "depth", "magnitude"]
earthquakes_file = path / "earthquakes_csv/1999_2017_earthquakes.csv"
earthquakes_df = pd.read_csv(earthquakes_file, names=earthquakes_columns)
earthquakes_coords = []
earthquakes_date = '2015-05-03'

tec_columns = ["time_stamp", "latitude", "longitude", "tec_value"]
tec_file = path / "tec_csv_esag/esag1230.15i.csv"
tec_df = pd.read_csv(tec_file, names=tec_columns)
initial_map = tec_df["time_stamp"].unique()[0]   # Return the first map of that day
hours = tec_df["time_stamp"].unique()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

navbar = dbc.NavbarSimple(
        dbc.Nav(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("TEC", href="/tec-content")),
                    dbc.NavItem(dbc.NavLink("OLR", href="/olr-content")),
                    dbc.NavItem(dbc.NavLink("Temperature", href="#"))
                ],
                pills=True
        )
)


app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Home page')
])

calendar = dbc.Col(
    [
        html.P("""Explore Data"""),
        dcc.DatePickerSingle(
            id='date-picker',
            with_full_screen_portal=True,
            clearable=False,
            min_date_allowed=dt(1999,12,31),
            max_date_allowed=dt(2017,12,31),
            calendar_orientation='vertical',
            placeholder='Select a date',
            date='2015-05-03'
        ),
    ], style={'marginBottom':'2em'}
) # End of Dropdown Col

two_hour_dropdown = dbc.Col(
    [
       html.H2("2-Hour Maps"),
       html.P("""Choose a time from the dropdown menu"""),
       dcc.Dropdown(
           id="dropdown",
           #options=[{"label":i, "value": i} for i in tec_df["time_stamp"].unique()],
           options = [{"label":i, "value": i} for i in tec_df["time_stamp"].unique()],
           value = initial_map
       )
   ], style={'marginBottom':'2em'}
) # End of Dropdown Col



tec_layout = html.Div([
    html.H1('Total Electron Content Map'),
    calendar,
    two_hour_dropdown,
    html.Div(id='tec-content'),
    html.Br(),
    dcc.Link('OLR', href='/olr-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(dash.dependencies.Output('tec-content', 'children'),
              [dash.dependencies.Input('tec-content-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


olr_layout = html.Div([
    html.H1('Outgoing Long-Wave Radiation'),
    calendar,
    html.Div(id='olr-content'),
    html.Br(),
    dcc.Link('TEC', href='/tec-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('olr-content', 'children'),
              [dash.dependencies.Input('olr-content-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/tec-content':
        return tec_layout
    elif pathname == '/olr-content':
        return olr_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)