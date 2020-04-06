#import plotly.graph_objects as go
#import numpy as np
#import pandas as pd
#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from IPython.display import HTML
#
#tec_columns = ["time_stamp", "latitude", "longitude", "tec_value"]
#tec_file = "~/Repos/iono2/tec_csv_esag/esag3650.09i.csv"
#tec_df = pd.read_csv(tec_file, names=tec_columns)
#hours = tec_df["time_stamp"].unique()
#
#m = Basemap()
#
#def make_scatter(x,y):
#    return go.Scattergl(
#        x=x,
#        y=y,
#        mode="lines",
#        line=go.scattergl.Line(color="black"),
#        name=" ",
#        showlegend=False
#    )
#
#def polygons_to_traces(poly_paths, N_poly):
#    traces = []
#    for i_poly in range(N_poly):
#        poly_path = poly_paths[i_poly]
#        coords_cc = np.array(
#            [(vertex[0],vertex[1])
#            for (vertex, code) in poly_path.iter_segments(simplify=False)]
#        )
#    
#        lon_cc, lat_cc = m(coords_cc[:,0], coords_cc[:,1], inverse=True)
#        traces.append(make_scatter(lon_cc, lat_cc))
#    return traces
#
##Function generating coastline lon/lat traces
#def get_coastline_traces():
#    poly_paths = m.drawcoastlines().get_paths()
#    N_poly = 91  # use only the 91st biggest coastlines (i.e no rivers)
#    return polygons_to_traces(poly_paths, N_poly)
#
## Function generating country lon/lat traces
#def get_country_traces():
#    poly_paths = m.drawcountries().get_paths()
#    N_poly = len(poly_paths)
#    return polygons_to_traces(poly_paths, N_poly)
#
#font_dict = dict(
#    family="Courier New, monospace",
#    size=24,
#    color="#7f7f7f"
#)
#
#colorbar_dict = dict(
#    title="TEC",
#    titleside="right",
#    titlefont=font_dict
#)
#
## Generate map traces once!
#traces_cc = get_coastline_traces()+get_country_traces()
#
#def make_contour(hour):
#    map_df = tec_df[tec_df['time_stamp'] == hour]
#    tec_values = map_df['tec_value'].values
#    longitude = map_df['longitude'].values
#    latitude = map_df['latitude'].values
#
#    trace1 = go.Contour(
#        z = tec_values,
#        x = longitude,
#        y = latitude,
#        colorscale="Jet",
#        zauto=True,
#        contours=dict(
#            coloring="heatmap",
#            showlabels=False,
#            labelfont=dict(
#                size=12,
#                color="black"
#            )
#        ),
#        colorbar=colorbar_dict
#    )
#        
#    data = ([trace1] + traces_cc)
#    return data
#
#
#    
#
#
##    frames=[go.Frame(data=make_contour(hours[0])),
##            go.Frame(data=make_contour(hours[2])),
##            go.Frame(data=make_contour(hours[4])),
##            go.Frame(data=make_contour(hours[6])),
##            go.Frame(data=make_contour(hours[8])),
##            go.Frame(data=make_contour(hours[10])),
##            ]
#
#
##fig.show()
#
#
#    #=========================================
#    # Create Fake Images using Numpy 
#    # You don't need this in your code as you have your own imageList.
#    # This is used as an example.
#
#imageList = []
#
#def make_graphs():
#
#    for hour in hours:
#        fig = go.Figure(
#            data=make_contour(hour),
#
#            layout=go.Layout(
#                xaxis=dict(range=[-180, 180], autorange=False),
#                yaxis=dict(range=[-90, 90], autorange=False),
#                title="TEC Map",
#                updatemenus=[dict(
#                    type="buttons",
#                    showactive=False,
#                    buttons=[dict(label="Play",
#                                  method="animate",
#                                  args=[None,
#                                        dict(frame=dict(duration=100, redraw=True),
#                                        transition=dict(duration=0),
#                                        fromcurrent=True,
#                                        mode='immediate')])])]
#            )
#        )
#        imageList.append(fig)
##=========================================
## Animate Fake Images (in Jupyt
#def getImageFromList(x):
#    return imageList
#fig = plt.figure()
#ims = []
#for i in range(len(imageList)):
#    im = plt.imshow(getImageFromList(i), animated=True)
#    ims.append([im])
#ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
#plt.close()
## Show the animation
#HTML(ani.to_html5_video())
##=========================================
## Save animation as video (if required)
#ani.save('dynamic_images.mp4')
from keras.preprocessing.image import load_img, img_to_array
from matplotlib import animation
import matplotlib.pyplot as plt
from IPython.display import HTML
import glob

#%matplotlib inline
directory=r"/home/antonio/Repos/iono2/animations/"

def plot_images(img_list):
  def init():
    img.set_data(img_list[0])
    return (img,)

  def animate(i):
    img.set_data(img_list[i])
    return (img,)

  fig = plt.figure()
  ax = fig.gca()
  img = ax.imshow(img_list[0])
  anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=len(img_list), interval=20, blit=True)
  return anim

imgs = [img_to_array(load_img(i)) for i in glob.glob(directory + '*.png')]

HTML(plot_images(imgs).to_html5_video())