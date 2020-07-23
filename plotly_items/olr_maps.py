import pickle
import pathlib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from mpl_toolkits.basemap import Basemap

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output

# Current working directory, pwd in bash.
path = pathlib.Path('/home/antonio/Repos/iono2')

# Load traces_cc
traces_cc_file = path / 'plotly_items/traces_cc.data'
with open(traces_cc_file, 'rb') as filehandle:
    traces_cc = pickle.load(filehandle)

olr_columns = ["latitude", "longitude", "olr_value"]
olr_file = path / "/home/antonio/Repos/iono2/olr_csv/1999_1.csv"
olr_df = pd.read_csv(olr_file, names=olr_columns)
olr_coords = []

navbar = dbc.NavbarSimple(
        dbc.Nav(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="#")),
                    dbc.NavItem(dbc.NavLink("TEC", href="#")),
                    dbc.NavItem(dbc.NavLink("OLR", href="#")),
                    dbc.NavItem(dbc.NavLink("Temperature", href="#"))
                ],
                pills=True
        )
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([navbar])


########################## OLR MAP ############################

font_dict = dict(
    family="Courier New, monospace",
    size=24,
    color="#7f7f7f"
)

colorbar_dict = dict(
    #title=r"$\text{Irradiance } \frac{W}{m^2}$",
    title="Irradiance",
    titleside="right",
    titlefont=font_dict
)

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


############### Update Graph ##########

# Update the date for the 2-hour dropdown #
def make_contour():
    olr_values = olr_df['olr_value'].values
    longitude = olr_df['longitude'].values
    latitude = olr_df['latitude'].values

    trace1 = go.Contour(
        z = olr_values,
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
        colorbar=colorbar_dict
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


def make_frames():
    frames = []
    frames.append(go.Frame(
         data=make_contour()
    ))
    return frames

    
def make_graphs():
    fig = go.Figure(
        data=make_contour(),
        layout=make_layout(),
        frames=make_frames()
    )

    fig.update_layout(
        title=go.layout.Title(
            text="Outgoing Long-wave Radiation",
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

if __name__ == "__main__":
    make_graphs()
    #app.run_server(debug=True)