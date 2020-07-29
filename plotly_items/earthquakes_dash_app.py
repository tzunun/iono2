import os
import pickle
import pathlib
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import date

import plotly.graph_objs as go

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Current working directory, pwd in bash.
path = pathlib.Path('~/Repos/iono2')

# Load traces_cc
traces_cc_file = '/home/antonio/Repos/iono2/plotly_items/traces_cc.data'
with open(traces_cc_file, 'rb') as filehandle:
    traces_cc = pickle.load(filehandle)

# Earthquake variables
earthquakes_columns = ["time_stamp", "latitude", "longitude", "depth", "magnitude"]
earthquakes_file = path / "earthquakes_csv/1999_2017_earthquakes.csv"
earthquakes_df = pd.read_csv(earthquakes_file, names=earthquakes_columns)
earthquakes_coords = []
earthquakes_date = '2015-05-03'

# TEC variables
tec_columns = ["time_stamp", "latitude", "longitude", "tec_value"]
tec_file = path / "tec_csv_esag/esag1230.15i.csv"
tec_df = pd.read_csv(tec_file, names=tec_columns)
initial_map = tec_df["time_stamp"].unique()[0]   # Return the first map of that day
hours = tec_df["time_stamp"].unique()

# OLR variables
olr_columns = ["latitude", "longitude", "olr_value"]
olr_file = "/home/antonio/Repos/iono2/olr_csv/2015_123.csv"
olr_df = pd.read_csv(olr_file, names=olr_columns)
olr_coords = []

########################## OLR MAP ############################

font_dict = dict(
    family="Courier New, monospace",
    size=24,
    color="#7f7f7f"
)

def create_colorbar_dict(measuring_unit):
    
    colorbar_dict = dict(
        #title=r"$\text{Irradiance } \frac{W}{m^2}$",
        title=measuring_unit,
        titleside="right",
        titlefont=font_dict
    )
    return colorbar_dict

# Helper functions for dealing with dates and coordinates
def format_days(day):
    if len(day) == 1:
        return ''.join(['00',day, '0'])
    elif len(day) == 2:
        return ''.join(['0', day, '0'])
    elif len(day) == 3:
        return ''.join([day, '0'])

def update_eq_coords(date):

    # List of boolean values from comparing the first 10 characters of the date string in 'i' and comparing it to 'date'
    day_indexes = ([i[:10] == date for i in olr_df['time_stamp']])
    return olr_df[day_indexes]

def make_contour(measuring_unit, depth, latitude, longitude):

    trace1 = go.Contour(
        z = depth,
        x = longitude,
        y = latitude,
        colorscale="Jet",
        zauto=True,
        contours=dict(
            coloring="heatmap",
            showlabels=False,
            labelfont=dict(
                size=12,
                color="black"
            )
        ),
        colorbar=create_colorbar_dict(measuring_unit)
    )
        
    data = ([trace1] + traces_cc)
    return data

def make_layout():
    return go.Layout(
    autosize=True,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor='rgba(0,0,0,0)',
    #width=1080,
    height=720,
    )


def make_frames(measuring_unit, depth, latitude, longitude):
    frames = []
    frames.append(go.Frame(
        data=make_contour(measuring_unit, depth, latitude, longitude)
    ))
    return frames

    
def make_graphs(graph_title, measuring_unit, depth, latitude, longitude):
    global tec_df, tec_columns, initial_map, earthquakes_coords, earthquakes_date, path
    fig = go.Figure(
        data=make_contour(measuring_unit, depth, latitude, longitude),
        layout=make_layout(),
        frames=make_frames(measuring_unit, depth, latitude, longitude)
    )

    #### Plot earthquakes for that day
    fig.add_trace(
        go.Scatter(
            x=earthquakes_coords['longitude'],
            y=earthquakes_coords['latitude'],
            mode='markers',
            marker=dict(
                color='White',
                opacity=0.999,
                size=12,
                line=dict(color='Magenta',
                width=2),
            ),
            showlegend=False,
            hovertext=earthquakes_coords['time_stamp']

        )
    )

    fig.update_layout(
        title=go.layout.Title(
            text=graph_title,
            xref="paper",
            yref="paper",
            font=font_dict
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Longitude",
                font=font_dict
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Latitude",
                font=font_dict
            )
        )
    )

    return fig


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

navbar = dbc.NavbarSimple(
        dbc.Nav(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("TEC", href="/tec-content")),
                    dbc.NavItem(dbc.NavLink("OLR", href="/olr-content")),
                    dbc.NavItem(dbc.NavLink("Temperature", href="temp-content"))
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

slider= dbc.Col([  
    html.Br(),
    html.H4("Choose the year for which you wish to explore the data"),
    dcc.Slider(id='year-slider',
        min=1999,
        max=2017,
        value=2015,
        step=1,
        marks={
            i: '{}'.format(i) for i in range(1999,2018)
        }
    )
])

calendar = dbc.Col(
    [
        html.Br(),
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

#graph_col =  dbc.Col(html.Div(dcc.Graph(id="map",style={'width':'100vw','height':'70vh'})), md=12, lg=8, sm=12)


tec_layout = html.Div([
    html.H1('Total Electron Content Map'),
    slider,
    calendar,
    two_hour_dropdown,
    html.Div(id='tec-content'),
    html.Br(),
])


def update_eq_coords(date):

    # List of boolean values from comparing the first 10 characters of the date string in 'i' and comparing it to 'date'
    day_indexes = ([i[:10] == date for i in earthquakes_df['time_stamp']])
    return earthquakes_df[day_indexes]


@app.callback(
    Output("date-picker", "date"),
    [Input("year-slider", "value")]
)
def update_calendar(year):
    return ''.join([str(year), '-05-23'])


# Update the date for the 2-hour dropdown #
@app.callback(
    Output("dropdown", "options"),
    [Input("date-picker", "date")]
    )
def update_value(date):
    global tec_df, tec_columns, initial_map, earthquakes_coords, earthquakes_date, path

    earthquakes_date = date
    earthquakes_coords = update_eq_coords(date)

    start_date = dt.strptime((''.join([date[:4], "-1-1"])), '%Y-%m-%d')
    new_date = dt.strptime(date, '%Y-%m-%d')
    delta =  new_date - start_date
    day = format_days(str(delta.days + 1))
    tec_file = path /''.join(["tec_csv_esag/esag", day, ".", (str(new_date.year)[2:]), "i.csv"])
    tec_df = pd.read_csv(tec_file, names=tec_columns)
    initial_map = tec_df["time_stamp"].unique()[0]   # Return 0the first map of that day
    return [{"label":i, "value": i} for i in tec_df["time_stamp"].unique()]

@app.callback(
    Output('tec-content', 'children')
, [Input("dropdown", "value")])
def update_tec_map(dropdown_value):
    tec_map_df = tec_df[tec_df['time_stamp'] == dropdown_value]

    graph_title = "Total Electron Content"
    measuring_unit = 'TEC'
    depth = tec_map_df['tec_value'].values
    longitude = tec_map_df['longitude'].values
    latitude = tec_map_df['latitude'].values

    return html.Div(dcc.Graph(id='tec_map', figure=make_graphs(graph_title, measuring_unit, depth, latitude, longitude)))

def olr_date(day,year):
    global earthquakes_coords, earthquakes_date
    earthquakes_date = day
    earthquakes_coords = update_eq_coords(day)

    
    if year != None:
        olr_file = ''.join(["/home/antonio/Repos/iono2/olr_csv/", str(year), "_123.csv"])
        return olr_file
    else:
        day = date.fromisoformat(day)
        d0 = date(day.year, 1, 1)
        delta = day - d0
        olr_file = ''.join(["/home/antonio/Repos/iono2/olr_csv/", str(day.year), "_", str(delta.days), ".csv"])
        return olr_file


@app.callback(
    Output('olr-content', 'children')
, [Input('date-picker', 'date'),
    Input("year-slider", "value")])
def update_olr_map(day, year):
    graph_title = "Outgoing Long-Wave Radiation"
    measuring_unit = 'Irradiance'

    # Not very pleased with this section

    olr_file = olr_date(day,year)
    olr_df = pd.read_csv(olr_file, names=olr_columns)

    depth = olr_df['olr_value'].values
    longitude = olr_df['longitude'].values
    latitude = olr_df['latitude'].values

    return html.Div(dcc.Graph(id='olr_map', figure=make_graphs(graph_title, measuring_unit, depth, latitude, longitude)))

olr_layout = html.Div([
    html.H1('Outgoing Long-Wave Radiation'),
    html.Br(),
    slider,
    calendar,
    html.Div(id='olr-content'),
    html.Br(),
    #dbc.Col(html.Div(dcc.Graph(id="olr_map",style={'width':'100vw','height':'70vh'})), md=12, lg=8, sm=12),
    html.Br()
])

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