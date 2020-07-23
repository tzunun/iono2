#Traces_cc data
import numpy as np
import pickle
import os
from os import path
from mpl_toolkits.basemap import Basemap
import plotly.graph_objects as go 

m = Basemap()

def make_scatter(x,y):
    return go.Scattergl(
        x=x,
        y=y,
        mode="lines",
        line=go.scattergl.Line(color="black"),
        name=" ",
        showlegend=False
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
    N_poly = 91  # use only the 91st biggest coastlines (i.e no rivers)
    return polygons_to_traces(poly_paths, N_poly)

# Function generating country lon/lat traces
def get_country_traces():
    poly_paths = m.drawcountries().get_paths()
    N_poly = len(poly_paths)
    return polygons_to_traces(poly_paths, N_poly)


def save_traces_cc():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    file = ''.join([dirname, '/traces_cc.data'])
    traces_cc = get_coastline_traces()+get_country_traces()

    if path.exists(file):
        print("File {} exists, will not create it!".format(file))
    else:
        # Save the traces_cc to traces_cc.data using pickle
        with open(file, 'wb') as filehandle:
            pickle.dump(traces_cc, filehandle)


if __name__=="__main__":
    save_traces_cc()