import dash
import pandas as pd
import plotly.express as px

from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from services import model 

# Initialise the app 
dashboard = dash.Dash(__name__) 

# just  a test

res = model.predict_query("some text")
print(res)

df = pd.DataFrame({
    "Candidates": [candidate["name"] for candidate in res["predictions"]],
    "Similarity": [candidate["similarity"] for candidate in res["predictions"]],

})

# Define the app Layout here
dashboard.title = 'Analytics Dashboard'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


fig = px.bar(df, x="Candidates", y="Similarity", barmode="group")

form = html.Div([
    html.H3("Texte prononcé"),
    html.Div([
        "Texte: ",
        dcc.Textarea(id='my-input', value="J'aime la France")
    ]),
    html.Button('Submit', id='submit-val', n_clicks=0)    

])

panelling = html.Div([html.Main(children= [form]), html.Aside(children=    dcc.Graph(
        id='barchart',
        figure=fig
    ),)], className='vertical-panelling')




dashboard.layout = html.Div(children=[
    html.Header(children=html.H1(children = 'Prevision.io')),
    panelling,
    html.Footer(children="Copyright")
], id="container")

def init_callbacks(dash_app):
    @dashboard.callback(
    Output('barchart', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('my-input', 'value')    
    )
    def update_graph(n_clicks, value):
        res = model.predict_query(value)
        df = pd.DataFrame({
            "Candidates": [candidate["name"] for candidate in res["predictions"]],
            "Similarity": [candidate["similarity"] for candidate in res["predictions"]],

        })
        fig = px.bar(df, x="Candidates", y="Similarity")
        fig.update_layout(transition_duration=500)
        return fig


init_callbacks(dashboard)
app = dashboard.server



