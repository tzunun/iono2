import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go 
import numpy as np 

app = dash.Dash()

# Create DATA

np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

# Define graph1
graph1 = dcc.Graph(id='scatterplot',
                    figure = {'data':[
                        go.Scatter(
                            x=random_x,
                            y=random_y,
                            mode='markers',
                            marker = {
                                'size':12,
                                'color':'rgb(32,233,123',
                                'symbol':'triangle',
                                'line':{'width':2}
                            }

                        )],
                    'layout':go.Layout(title='My Scatterplot',
                            xaxis = {'title':'Some X title'}
                    
                    )
                    }

)

# Define graph2
graph2 = dcc.Graph(id='scatterplot2',
                    figure = {'data':[
                        go.Scatter(
                            x=random_x,
                            y=random_y,
                            mode='markers',
                            marker = {
                                'size':12,
                                'color':'rgb(132,133,134',
                                'symbol':'pentagon',
                                'line':{'width':2}
                            }

                        )],
                    'layout':go.Layout(title='My Second Scatterplot',
                            xaxis = {'title':'Some Second X title'}
                    
                    )
                    }

)

# Display graphs inside the Div
app.layout = html.Div([graph1, graph2])

if __name__ == "__main__":
    app.run_server()