import dash
import pandas as pd
import plotly.express as px

from dash import dcc
from dash import html

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

panelling = html.Div([html.Main(children= "form"), html.Aside(children=    dcc.Graph(
        id='barchart',
        figure=fig
    ),)], className='vertical-panelling')
content = html.Div([html.Header, panelling, html.Footer], id="container")

layout = html.Div([dcc.Location(id="url"), panelling, content]) 

dashboard.layout = html.Div(children=[
    html.Header(children=html.H1(children = 'Prevision.io')),
    panelling,
    html.Footer(children="Copyright")
], id="container")

app = dashboard.server