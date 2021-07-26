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
    ], style={'width': '80%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

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
    ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dcc.Markdown('''
            **Natural Factors**
            ''',
             style={'font-size': '14px'},),
        dcc.Checklist(
            id='orbital_changes',
            options=[
                {'label': 'Orbital Changes', 'value': 'OC'},
            ],
            value=[],
            style={'color': 'deepskyblue', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='solar',
            options=[
                {'label': 'Solar', 'value': 'S'},
            ],
            value=[],
            style={'color': 'orange', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='volcanic',
            options=[
                {'label': 'Volcanic', 'value': 'V'},
            ],
            value=[],
            style={'color': 'red', 'font-size': '14px', 'margin-bottom': '20px'},
        ),

        dcc.Markdown('''
            **Human Factors**
            '''),
        dcc.Checklist(
            id='land_use',
            options=[
                {'label': 'Land Use', 'value': 'LU'},
            ],
            value=[],
            style={'color': 'sienna', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='ozone',
            options=[
                {'label': 'Ozone', 'value': 'O'},
            ],
            value=[],
            style={'color': 'cadetblue', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='aerosols',
            options=[
                {'label': 'Aerosols', 'value': 'A'},
            ],
            value=[],
            style={'color': 'mediumslateblue', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='greenhouse_gases',
            options=[
                {'label': 'Greenhouse Gases', 'value': 'GG'}
            ],
            value=[],
            style={'color': 'seagreen', 'font-size': '14px', 'margin-bottom': '20px'},
        ),
        dcc.Markdown('''
            **All Factors**
            '''),
        dcc.Checklist(
            id='natural',
            options=[
                {'label': 'Natural', 'value': 'N'}
            ],
            value=[],
            style={'color': 'purple', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='human',
            options=[
                {'label': 'Human', 'value': 'H'}
            ],
            value=[],
            style={'color': 'purple', 'font-size': '14px'},
        ),
        dcc.Checklist(
            id='all',
            options=[
                {'label': 'All Forcings', 'value': 'ALL'}
            ],
            value=[],
            style={'color': 'purple', 'font-size': '14px'},
            #labelStyle={'color': 'white', 'font-size': '14px', 'background-color': 'purple'},
            #inputStyle={'color': 'purple', 'background-color': 'white'},
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'middle'}),


], style={'width': '1000px'})



def update_factors(fig, factors):
    #colors: https://www.w3schools.com/cssref/css_colors.asp
    if 'OC' in factors:
        figOC = px.line(climate_forcings_data, x='Year', y='Orbital changes', color_discrete_sequence=['deepskyblue'])
        fig.add_trace(figOC.data[0])
    if 'S' in factors:
        figS = px.line(climate_forcings_data, x='Year', y='Solar', color_discrete_sequence=['orange'])
        fig.add_trace(figS.data[0])
    if 'V' in factors:
        figV = px.line(climate_forcings_data, x='Year', y='Volcanic', color_discrete_sequence=['red'])
        fig.add_trace(figV.data[0])
    if 'LU' in factors:
        figLU = px.line(climate_forcings_data, x='Year', y='Land use', color_discrete_sequence=['sienna'])
        fig.add_trace(figLU.data[0])
    if 'O' in factors:
        figO = px.line(climate_forcings_data, x='Year', y='Ozone', color_discrete_sequence=['cadetblue'])
        fig.add_trace(figO.data[0])
    if 'A' in factors:
        figA = px.line(climate_forcings_data, x='Year', y='Anthropogenic tropospheric aerosol', color_discrete_sequence=['mediumslateblue'])
        fig.add_trace(figA.data[0])
    if 'GG' in factors:
        figGG = px.line(climate_forcings_data, x='Year', y='Greenhouse gases', color_discrete_sequence=['seagreen'])
        fig.add_trace(figGG.data[0])
    if 'N' in factors:
        figN = px.line(climate_forcings_data, x='Year', y='Natural', color_discrete_sequence=['purple'])
        fig.add_trace(figN.data[0])
    if 'H' in factors:
        figH = px.line(climate_forcings_data, x='Year', y='Human', color_discrete_sequence=['purple'])
        fig.add_trace(figH.data[0])
    if 'ALL' in factors:
        figALL = px.line(climate_forcings_data, x='Year', y='All forcings', color_discrete_sequence=['purple'])
        fig.add_trace(figALL.data[0])
    return fig


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='orbital_changes', component_property='value'),
    Input(component_id='solar', component_property='value'),
    Input(component_id='volcanic', component_property='value'),
    Input(component_id='land_use', component_property='value'),
    Input(component_id='ozone', component_property='value'),
    Input(component_id='aerosols', component_property='value'),
    Input(component_id='greenhouse_gases', component_property='value'),
    Input(component_id='human', component_property='value'),
    Input(component_id='natural', component_property='value'),
    Input(component_id='all', component_property='value'),
)
def update_plot(orbital_changes, solar, volcanic, land_use, ozone, aerosols, greenhouse_gases, human, natural, all):
    factors = orbital_changes+solar+volcanic+land_use+ozone+aerosols+greenhouse_gases+human+natural+all
    fig = px.line(land_ocean_data, x='Year', y='Annual_Mean', title="Graph", color_discrete_sequence=['black'])
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)', yaxis_zeroline=True, yaxis_zerolinecolor='gainsboro', yaxis_showline=True, yaxis_linecolor='gainsboro')
    fig = update_factors(fig, factors)
    fig.update_yaxes(title='Temperature (C)', range=[-1.2, 1.2])

    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
