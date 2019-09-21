
import numpy as np
import random
import pandas as pd

#y = np.arange(90,-92.5,-2.5)

x = [np.arange(-180,185,5) for i in range(73)]
y = [np.arange(90,-92.5,-2.5) for i in range(71)]

data = pd.read_csv("/home/antonio/Repos/iono2/julia_scripts/depth.csv")
lon = np.asarray(x)
lat = np.asarray(y)
#depth = np.asarray(z)
depth = data[:5184]
depth = depth.values

# Transpose lat, lat.T
lat = lat.T

# Flatten the arrays
lon = lon.flatten()
lat = lat.flatten()
depth = depth.flatten()

X, Y = np.meshgrid(x,y)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from mpl_toolkits.basemap import Basemap

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    dcc.Graph(id='graph-with-slider')
])


quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')


######################### GIM TEC MAP ############################

m = Basemap(projection='merc', area_thresh=0.1, resolution='i')

def make_scatter(x,y):
    return go.Scattergl(
        x=x,
        y=y,
        mode='lines',
        line=go.scattergl.Line(color='black'),
        name=' '
    )


def polygons_to_traces(poly_paths, N_poly):
    traces = []
    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]
        coords_cc = np.array(
            [(vertex[0],vertex[1])
            for (vertex, code) in poly_path.iter_segments(simplify=False)]
        )
    
        lon_cc, lat_cc = m(coords_cc[:,0], coords_cc[:,1], inverse=True)
        traces.append(make_scatter(lon_cc, lat_cc))
    return traces

#Function generating coastline lon/lat traces
def get_coastline_traces():
    poly_paths = m.drawcoastlines().get_paths()
    N_poly = 91 
    return polygons_to_traces(poly_paths, N_poly)

# Function generating country lon/lat traces
def get_country_traces():
    poly_paths = m.drawcountries().get_paths()
    N_poly = len(poly_paths)
    return polygons_to_traces(poly_paths, N_poly)

font_dict = dict(
    family="Courier New, monospace",
    size=24,
    color="#7f7f7f"
)

colorbar_dict = dict(
    title='TEC',
    titleside='right',
    titlefont=font_dict
)


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):

#    ############################## Basemap plot works
    trace1 = go.Contour(
        z = depth,
        x = lon,
        y = lat,
        colorscale="Jet",
        zauto=True,
        contours=dict(
            coloring="heatmap",
            showlabels=True,
            labelfont=dict(
                size=12,
                color='white'
            )
        ),
        colorbar=colorbar_dict
        #zmin=0,
        #zmax=400
    )

    traces_cc = get_coastline_traces()+get_country_traces()
    data = ([trace1] + traces_cc)
    layout = go.Layout(
        autosize=True,
        width=1920,
        height=1080,
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        title=go.layout.Title(
            text="Total Electron Content",
            xref="paper",
            font=font_dict
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Longitud",
                font=font_dict
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Latitud",
                font=font_dict
            )
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
