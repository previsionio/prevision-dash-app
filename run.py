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


# Define the app Layout here
dashboard.title = 'Analytics Dashboard'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

panelling = html.Div([html.Main(children= "form"), html.Aside(children=    dcc.Graph(
        id='example-graph',
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