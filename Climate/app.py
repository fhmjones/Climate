# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.


from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

land_ocean_data = pd.read_csv("./land_ocean_filtered.csv")
climate_forcings_data = pd.read_csv("./climate_forcings_filtered.csv")
#averages_data = pd.read_csv("./averages.csv")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)


app.layout = html.Div([

    html.Div([
        dcc.Markdown('''
            ### Climate

            ----------
            '''),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

    html.Div([
        dcc.Markdown('''
            Natural Factors
            '''),
        dcc.Checklist(
            id='natural_factors',
            options=[
                {'label': 'Orbital Changes', 'value': 'OC'},
                {'label': 'Solar', 'value': 'S'},
                {'label': 'Volcanic', 'value': 'V'},
            ],
            value=[]
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

    html.Div([
        dcc.Markdown('''
            Human Factors
            '''),
        dcc.Checklist(
            id='human_factors',
            options=[
                {'label': 'Land Use', 'value': 'LU'},
                {'label': 'Ozone', 'value': 'O'},
                {'label': 'Aerosols', 'value': 'A'},
                {'label': 'Greenhouse Gases', 'value': 'GG'}
            ],
            value=[]
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

    html.Div([
        dcc.Graph(
            id='graph',
            config={
                'staticPlot': False,  # True, False
                'scrollZoom': True,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
            },
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),


], style={'width': '1000px'})



def update_factors(fig, factors):
    #colors: https://www.w3schools.com/cssref/css_colors.asp
    if 'OC' in factors:
        figOC = px.line(climate_forcings_data, x='Year', y='Orbital changes', title="Land Ocean", color_discrete_sequence=['deepskyblue'])
        fig.add_trace(figOC.data[0])
    if 'S' in factors:
        figS = px.line(climate_forcings_data, x='Year', y='Solar', title="Land Ocean", color_discrete_sequence=['orangered'])
        fig.add_trace(figS.data[0])
    if 'V' in factors:
        figV = px.line(climate_forcings_data, x='Year', y='Volcanic', title="Land Ocean", color_discrete_sequence=['red'])
        fig.add_trace(figV.data[0])
    if 'LU' in factors:
        figLU = px.line(climate_forcings_data, x='Year', y='Land use', title="Land Ocean", color_discrete_sequence=['khaki'])
        fig.add_trace(figLU.data[0])
    if 'O' in factors:
        figO = px.line(climate_forcings_data, x='Year', y='Ozone', title="Land Ocean", color_discrete_sequence=['cadetblue'])
        fig.add_trace(figO.data[0])
    if 'A' in factors:
        figA = px.line(climate_forcings_data, x='Year', y='Anthropogenic tropospheric aerosol', title="Land Ocean", color_discrete_sequence=['mediumslateblue'])
        fig.add_trace(figA.data[0])
    if 'GG' in factors:
        figGG = px.line(climate_forcings_data, x='Year', y='Greenhouse gases', title="Land Ocean", color_discrete_sequence=['seagreen'])
        fig.add_trace(figGG.data[0])
    return fig


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='natural_factors', component_property='value'),
    Input(component_id='human_factors', component_property='value'),
)
def update_plot(natural_factors, human_factors):
    factors = natural_factors + human_factors
    #fig = px.line(land_ocean_data, x='Year', y='Annual_Mean', title="Land Ocean")
    fig = px.line(land_ocean_data, x='Year', y='5-year_Mean', title="Graph", color_discrete_sequence=['black'])
    fig = update_factors(fig, factors)
    fig.add_hline(y=0, fillcolor='lightgrey')
    fig.update_yaxes(title='temperature (C)', range=[-1.2, 1.2])

    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
