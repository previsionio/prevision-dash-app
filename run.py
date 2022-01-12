import dash
import pandas as pd
import plotly.express as px

from dash import dcc
from dash import html

# Initialise the app 
dashboard = dash.Dash(__name__) 



# Define the app Layout here
dashboard.title = 'Analytics Dashboard'
dashboard.layout = html.Div() 

app = dashboard.server