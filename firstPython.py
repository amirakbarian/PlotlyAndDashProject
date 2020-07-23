import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'MyAPP_Stock'

df = pd.read_csv('/Users/amirakbarian/Desktop/Python Excersice/MCDREO_timeSeries.csv')
df = df.groupby(['Country Name']).mean()
df.drop(['Unnamed: 19', 'Country Code'], axis=1, inplace=True)
df = df.T

options = []
for tic in df.columns:
    options.append({'label': '{}'.format(tic), 'value': tic})

app.layout = html.Div([
        html.H1('MCDREO',style = {'text-align': 'center'}),
        html.H3('Select Country:',style={'paddingRight':'30px'}),
         html.Div([
                 dcc.Dropdown(id='drop-down',
                              options=options,
                              value =['Algeria','Armenia'],
                              multi=True)

                 ],style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),

        html.H3('Select start and end year:'),
        html.Div([
                dcc.RangeSlider(id = 'Range-Slider',
                                min=2004,
                                max=2018,
                                marks={i:str(i) for i in range(2004, 2019)},
                                value=[2006, 2010])

                ]),
        html.Button(children ='Submit',id = 'Submit-button',n_clicks=0,style={'fontSize':18, 'marginLeft':'30px'}),
        html.Div([
                dcc.Graph(id = 'main-Graph',
        figure={
            'data': [
                {'x': [2005,2006], 'y': [13,15]}
            ]
        }
    )
                ])

        ])

@app.callback(Output('main-Graph','figure'),
              [Input('Submit-button','n_clicks')],
               [State('drop-down','value'),
                State('Range-Slider','value')
               ])

def update_graph(n_clicks,country_names,value):
    traces = []
    df2 = df[df.index >= str(value[0])]
    df2 = df2[df2.index <= str(value[1])]
    for c_name in country_names:
        traces.append(go.Scatter(x=df2.index,y=df2[c_name]/(1e9),name = c_name,mode='lines+markers'))

    return {'data' : traces , 'layout' : go.Layout(title = 'MCDREO',
                                                   xaxis = dict(dtick = 1,title='Year'),
                                                   yaxis = {'title' : 'Index' }
                                                   )}

if __name__ == '__main__':
    app.run_server(debug=True,port=3003)