
import numpy as np
import random

#y = np.arange(90,-92.5,-2.5)

x = [np.arange(-180,185,5) for i in range(73)]
y = [np.arange(90,-92.5,-2.5) for i in range(73)]
z = [random.randrange(400) for p in range(0,(len(x)*len(y)))] 

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

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


import pandas as pd
quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')


######################### GIM TEC MAP ############################

def create_matrix_z():
    z = []
    for i in range(73): 
        z.append(np.arange(0,73))
    return (np.asarray(z))

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

    


    import plotly.express as px
    mapbox_access_token = open(".mapbox_token").read()
    fig = go.Figure(go.Densitymapbox(lat=lat, lon=lon, z=depth,radius=10))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=-180)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
