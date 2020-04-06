
import pandas as pd
import numpy as np
from datetime import datetime as dt
import pathlib

import plotly.graph_objs as go
from mpl_toolkits.basemap import Basemap

url = "/home/antonio/Repos/iono2/tec_csv_esag/esag3650.99i.csv"
columns = ['hour', 'latitude', 'longitude', 'tec_value']
dataset = pd.read_csv(url, names=columns)

hours = dataset['hour'].unique()


# make list of tec_values
tec_values = []
for tec_value in dataset["tec_value"]:
    if tec_value not in tec_values:
        tec_values.append(tec_value)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["title"] = {"text": "Daily TEC Animation", "xref":"paper", "yref":"paper"}
fig_dict["layout"]["font"] = {"family": "Courier New, monospace", "size":24, "color":"#7f7f7f"}
fig_dict["layout"]["xaxis"] = {"range": [-181, 181], "title": "Longitude"}
fig_dict["layout"]["yaxis"] = {"range": [-91, 91],"title": "Latitude"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": str(hours[0]),
    "plotlycommand": "animate",
    "values": tec_values,
    "visible": True
}
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
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

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Hour:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
hour = 1952
for tec_value in tec_values:
    dataset_by_hour = dataset[dataset["hour"] == hour]
    dataset_by_hour_and_cont = dataset_by_hour[
        dataset_by_hour["tec_value"] == tec_value]

    data_dict = {
        "x": list(dataset_by_hour_and_cont["longitude"]),
        "y": list(dataset_by_hour_and_cont["latitude"]),
        "mode": "markers",
        "text": list(dataset_by_hour_and_cont["hour"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 200000,
            "size": list(dataset_by_hour_and_cont["tec_value"])
        },
        "name": tec_value
    }
    fig_dict["data"].append(data_dict)

# make frames
for hour in hours:
    frame = {"data": [], "name": str(hour)}
    for tec_value in tec_values:
        dataset_by_hour = dataset[dataset["hour"] == hour]
        dataset_by_hour_and_cont = dataset_by_hour[
            dataset_by_hour["tec_value"] == tec_value]

        data_dict = {
            "x": list(dataset_by_hour_and_cont["longitude"]),
            "y": list(dataset_by_hour_and_cont["latitude"]),
            "mode": "markers",
            "text": list(dataset_by_hour_and_cont["hour"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_hour_and_cont["tec_value"])
            },
            "name": tec_value
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [hour],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": hour,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


#fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()