
import numpy as np
import random

#y = np.arange(90,-92.5,-2.5)

x = [np.arange(-180,185,5) for i in range(73)]
y = [np.arange(90,-92.5,-2.5) for i in range(73)]
z = [random.randrange(30,50) for p in range(0,(len(x)*len(y)))] 

lon = np.asarray(x)
lat = np.asarray(y)
depth = np.asarray(z)

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

import pandas as pd
from plotly.tools import mpl_to_plotly
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from mpl_toolkits.basemap import Basemap
import plotly.express as px

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


import pandas as pd
quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')


######################### GIM TEC MAP ############################

m = Basemap(projection='merc', area_thresh=0.1)

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


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    #Z = create_matrix_z()
    #m = Basemap(projection='cyl',llcrnrlat=-87.5,urcrnrlat=87.5, llcrnrlon=-180,urcrnrlon=180,resolution='c') 
    #x, y = m(X, Y)    

    #fig = plt.figure() 
    ##fig = plt.figure(figsize=(15,7)) 
    ##m.fillcontinents(color='gray',lake_color='gray') 
    #m.drawcoastlines() 
    #m.drawparallels(np.arange(87.5,90,-2.5)) 
    #m.drawmeridians(np.arange(-180,185,5)) 
    #m.drawmapboundary(fill_color='white') 
    #cs = m.contourf(x,y,Z,73) 
    #plt.title('Monthly mean SAT')                                                                               

    #plotly_fig = mpl_to_plotly(fig)
    #df = pd.DataFrame(dict(x=lon, y=lat,z=depth))
    #trace1 = px.scatter_3d(df, x='x', y='y', z='z', color='z')
    trace1 = go.Contour(
        z = depth,
        x = lon,
        y = lat,
        colorscale="Jet",
        zauto=True,
        #zmin=0,
        #zmax=400
    )

    traces_cc = get_coastline_traces()+get_country_traces()
    data = ([trace1] + traces_cc)
    layout = go.Layout(
        autosize=True,
        width=1080,
        height=720,
    )
    fig = go.Figure(data=data, layout=layout)
    


    

    


    #import plotly.express as px
    #mapbox_access_token = open(".mapbox_token").read()
    #fig = go.Figure(go.Densitymapbox(lat=lat, lon=lon, z=depth,radius=10))
    #fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=-180)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
