import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly 
import plotly.graph_objs as go
import serial


#Initiate parameters for graph1
Y = [3,1,2]
X = [1,2,3]

data = 0

arduino = serial.Serial('COM7', 9600, timeout=.1)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Elevator State',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Display the current state of three cars of The elevator', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
                'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                    },
                'xaxis': dict(range=[0,4]),
                'yaxis': dict(range=[0,4]),
                }}),
            dcc.Interval(
            id='graph-update',
            interval=500
            )
])
            
            
@app.callback(Output('example-graph-2', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    datastr = arduino.read(3).decode('utf-8')
    print(datastr)
    if len(datastr)>1:
        data = int(datastr)
        level = data % 10
        elevator = data / 10
        Y[elevator] = level
        print(data)
    
    data = plotly.graph_objs.Scatter(
            x = X,
            y = Y,
            type =  'bar',
            name = 'Elevator'
            )

    return {'data': [data], 'layout':go.Layout(xaxis=dict(range=[0,4]),
            yaxis = dict(range = [0,5]),
            plot_bgcolor = colors['background'],
            paper_bgcolor = colors['background'],
            font ={
                    'color': colors['text']
                    })}

if __name__ == '__main__':
    app.run_server()