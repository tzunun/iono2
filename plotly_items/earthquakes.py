import numpy as np
import pandas as pd
import pathlib
import plotly.graph_objects as go
from mpl_toolkits.basemap import Basemap


# Current working directory, pwd in bash.
path = pathlib.Path('~/Repos/iono2')

earthquakes_columns = ["time_stamp", "latitude", "longitude", "depth", "magnitude"]
earthquakes_file = path / "earthquakes_csv/1999_2017_eq.csv"
earthquakes_df = pd.read_csv(earthquakes_file, names=earthquakes_columns)
earthquakes_coords = []
earthquakes_date = '1999-12-31'

tec_columns = ["time_stamp", "latitude", "longitude", "tec_value"]
tec_file = path / "tec_csv_esag/esag3650.99i.csv"
tec_df = pd.read_csv(tec_file, names=tec_columns)

hours = tec_df['time_stamp'].unique()


######################### GIM TEC MAP ############################

#m = Basemap(projection="merc", area_thresh=0.1, resolution="i")
m = Basemap()
#m = Basemap(projection="mall", celestial=True, llcrnrlat=-87.5, urcrnrlat=87.5, llcrnrlon=-180, urcrnrlon=180, resolution="i")

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

font_dict = dict(
    family="Courier New, monospace",
    size=24,
    color="#7f7f7f"
)

colorbar_dict = dict(
    title="TEC",
    titleside="right",
    titlefont=font_dict
)

# Generate map traces once!
traces_cc = get_coastline_traces()+get_country_traces()

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
    day_indexes = ([i[:10] == date for i in earthquakes_df['time_stamp']])
    return earthquakes_df[day_indexes]


############### Update Graph ##########

# Update the date for the 2-hour dropdown #
def make_contour(hour):
    map_df = tec_df[tec_df['time_stamp'] == hour]
    tec_values = map_df['tec_value'].values
    longitude = map_df['longitude'].values
    latitude = map_df['latitude'].values

    trace1 = go.Contour(
        z = tec_values,
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
    updatemenus=[
    {
        "buttons": [
            {
                "args": [[None], {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 500}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]
    )

def make_frames():
    frames = []
    for hour in hours:
        frames.append(go.Frame(
             data=make_contour(hour)
         ))
    return frames
    
def make_graphs():
    x = 0
    for hour in hours:
        
       fig = go.Figure(
           data=make_contour(hour),
           layout=make_layout(),
           frames=make_frames()
       )

       fig.update_layout(
           title=go.layout.Title(
               text="Total Electron Content",
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
       fig.write_image(''.join(['/home/antonio/Repos/iono2/animations/', str(x), '.png']))
       x+=1

if __name__ == "__main__":
    make_graphs()
        