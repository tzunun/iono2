import numpy as np
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from mpl_toolkits.basemap import Basemap
from datetime import datetime as dt

columns = ["time_stamp", "latitud", "longitud", "tec_value"]
tec_file = "/home/antonio/Repos/iono2/tec_csv_esag/esag0010.10i.csv"
df = pd.read_csv(tec_file, names=columns)
initial_map = df["time_stamp"].unique()[0]   # Return the first map of that day


navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Link", href="#")),
            dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
                ],
            ),
        ],
        brand="Earthquake Precursor Project",
        brand_href="#",
        sticky="top",
    )


body = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                           html.H2("2-Hour Maps"),
                           html.P("""Choose a different time from the dropdown menu"""),
                           dcc.Dropdown(
                               id="dropdown",
                               #options=[{"label":i, "value": i} for i in df["time_stamp"].unique()],
                               options = [{"label":i, "value": i} for i in df["time_stamp"].unique()],
                               value = initial_map
                           )
                       ], style={'marginBottom':'2em'}
                    ), # End of Dropdown Col
                     dbc.Col(
                        [
                            html.H2("Daily TEC Maps"),
                            html.P("""Choose a different date from the dropdown menu"""),
                            dcc.DatePickerSingle(
                                id='date-picker',
                                with_full_screen_portal=True,
                                clearable=False,
                                min_date_allowed=dt(2000,1,1),
                                max_date_allowed=dt(2019,1,1),
                                calendar_orientation='vertical',
                                placeholder='Select a date',
                                date='2001-1-1'
                            ),
                        ], style={'marginBottom':'2em'}
                    ) # End of Dropdown Col
                ]), # End of Row
            dbc.Row(
                   [
                   html.H2("Ionospheric Anomalies"),
                   html.P("""
                       Detection of signals near earthquake areas, using various
                       sensing divices.
                   """
                   ),
                   dbc.Button("View details", color="secondary"),
                   ],
               ), # End of Heading Col           
            #dbc.Row(children = [ # Children inherit sizing from the parents
            #        dbc.Col(
            #            [
            #                html.H2("Graph"),
            #                dcc.Graph(id="map")
            #            ]
            #        )
            #        ]
            #    )
            dbc.Row(children=[
                dbc.Col(html.Div(dcc.Graph(id="map",style={'width':'95vw','height':'60vh'})), md=12, lg=12, sm=12)
            ], align="center" )  # Align the row center
        ], 
        fluid=True
        #className="mt-4",
)  # End of dbc.Container


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([navbar, body])

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

############### Update Graph ##########

def format_days(day):
    if len(day) == 1:
        return ''.join(['00',day, '0'])
    elif len(day) == 2:
        return ''.join(['0', day, '0'])
    elif len(day) == 3:
        return ''.join([day, '0'])

########### Update the date for the 2-hour dropdown ###########
@app.callback(
    Output("dropdown", "options"),
    [Input("date-picker", "date")]
    )
def update_value(date):
    global df
    start_date = dt.strptime((''.join([date[:4], "-1-1"])), '%Y-%m-%d')
    new_date = dt.strptime(date, '%Y-%m-%d')
    delta =  new_date - start_date
    day = format_days(str(delta.days + 1))
    tec_file = ''.join(["/home/antonio/Repos/iono2/tec_csv_esag/esag", day, ".", (str(new_date.year)[2:]), "i.csv"])
    df = pd.read_csv(tec_file, names=columns)
    #initial_map = df["time_stamp"].unique()[0]   # Return 0the first map of that day
    return [{"label":i, "value": i} for i in df["time_stamp"].unique()]

@app.callback(
    Output("map", "figure"),
    [Input("dropdown", "value")]
    )
def update_figure(dropdown_value):
    global df

    map_df = df[df["time_stamp"]==dropdown_value]
    lat = map_df["latitud"].values
    lon = map_df["longitud"].values
    tec_values = map_df["tec_value"].values

############### Basemap plot works ################

    trace1 = go.Contour(
        z = tec_values,
        x = lon,
        y = lat,
        colorscale="Jet",
        zauto=True,
        contours=dict(
            coloring="heatmap",
            showlabels=False,
            labelfont=dict(
                size=12,
                color="white"
            )
        ),
        colorbar=colorbar_dict
    )
    
    data = ([trace1] + traces_cc)
    

    layout = go.Layout(
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor='rgba(0,0,0,0)'
        #width=540,
        #height=300,
    )

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
        title=go.layout.Title(
            text="Total Electron Content",
            xref="paper",
            yref="paper",
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

if __name__ == "__main__":
    app.run_server(debug=True)
