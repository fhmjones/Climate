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
        dcc.RadioItems(
            id='graph_type',
            options=[
                {'label': 'Learn', 'value': 'learn'},
                {'label': 'Explore', 'value': 'explore'}
            ],
            value='learn'
        )
    ], style={'width': '80%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20} ),

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

    #styling the checklists/radiobuttons: https://community.plotly.com/t/dcc-radioitems-and-label-style/26358/2
    html.Div([
        dcc.Markdown('''
            **Natural Factors**
            ''',
             style={'font-size': '14px'},),
        dcc.Checklist(
            id='natural_checklist',
            options=[
                {'label': 'Orbital Changes', 'value': 'OC'},
                {'label': 'Solar', 'value': 'S'},
                {'label': 'Volcanic', 'value': 'V'}
            ],
            value=[],
            style={'display':'none'}
        ),
        dcc.RadioItems(
            id='natural_radiobuttons',
            options=[
                {'label': 'Orbital Changes', 'value': 'OC'},
                {'label': 'Solar', 'value': 'S'},
                {'label': 'Volcanic', 'value': 'V'}
            ],
        ),

        dcc.Markdown('''
            **Human Factors**
            '''),
        dcc.Checklist(
            id='human_checklist',
            options=[
                {'label': 'Land Use', 'value': 'LU'},
                {'label': 'Ozone', 'value': 'O'},
                {'label': 'Aerosols', 'value': 'A'},
                {'label': 'Greenhouse Gases', 'value': 'GG'},
            ],
            value=[],
            style={'display':'none'}
        ),
        dcc.RadioItems(
            id='human_radiobuttons',
            options=[
                {'label': 'Land Use', 'value': 'LU'},
                {'label': 'Ozone', 'value': 'O'},
                {'label': 'Aerosols', 'value': 'A'},
                {'label': 'Greenhouse Gases', 'value': 'GG'},
            ],
        ),

        dcc.Markdown('''
            **All Factors**
            '''),
        dcc.Checklist(
            id='all_checklist',
            options=[
                {'label': 'Natural', 'value': 'N'},
                {'label': 'Human', 'value': 'H'},
                {'label': 'All Forcings', 'value': 'ALL'}
            ],
            value=[],
            style={'display':'none'}
        ),
        dcc.RadioItems(
            id='all_radiobuttons',
            options=[
                {'label': 'Natural', 'value': 'N'},
                {'label': 'Human', 'value': 'H'},
                {'label': 'All Forcings', 'value': 'ALL'}
            ],
        ),

    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dcc.Markdown(
            children='''**Text**''',
            id='description',
            style={'font-size': '14px'},),
    ])


], style={'width': '1000px'})



@app.callback(
    Output(component_id='description', component_property='children'),
    Input(component_id='graph_type', component_property='value'),
    Input(component_id='natural_radiobuttons', component_property='value'),
    Input(component_id='human_radiobuttons', component_property='value'),
    Input(component_id='all_radiobuttons', component_property='value'),
)
def update_description(graph_type, natural, human, all):
    if graph_type == 'learn':
        output = ''''''
        if natural == 'OC':
            output += '''
            **The Earth's Orbit**:  
            The Earth wobbles on its axis, and its tilt and orbit change over many thousands of years, pushing the climate into and out of ice ages.  
            '''
        elif natural == 'S':
            output += '''
            **The Sun**:  
            The sun's temperature varies over decades and centuries.  
            '''
        elif natural == 'V':
            output += '''
            **Volcanoes**  
            '''

        if human == 'LU':
            output += '''
            **Deforestation**:  
            Humans have cut, plowed, and paved more than hald the Earth's land surface. Dark forests are yielding to lighter patches, which reflect more sunlight.  
            '''
        elif human == 'O':
            output += '''
            **Ozone Pollution**:  
            Natural ozone high in the atmosphere blocks harmful sunlight. Closer to the Earth, ozone is created by pollution and traps heat.  
            '''
        elif human == 'A':
            output += '''
            **Aerosol Polution**  
            '''
        elif human == 'GG':
            output += '''
            **Greenhouse Gases**  
            '''

        if all == 'N':
            output += '''
            **Natural**  
            '''
        elif all == 'H':
            output += '''
            **Human**  
            '''
        elif all == 'ALL':
            output += '''
            **All**  
            '''

        return [output]

for i in ['natural_checklist', 'human_checklist', 'all_checklist']:
    @app.callback(
        Output(component_id=i, component_property='style'),
        Input('graph_type', 'value'),
    )
    def update_graph_type(graph_type):
        if graph_type == 'learn':
            return {'display':'none'}
        elif graph_type == 'explore':
            return {'display':'inline'}
for i in ['natural_radiobuttons', 'human_radiobuttons', 'all_radiobuttons']:
    @app.callback(
        Output(component_id=i, component_property='style'),
        Input('graph_type', 'value'),
    )
    def update_graph_type(graph_type):
        if graph_type == 'learn':
            return {'display':'inline'}
        elif graph_type == 'explore':
            return {'display':'none'}

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
    Input(component_id='graph_type', component_property='value'),
    Input(component_id='natural_checklist', component_property='value'),
    Input(component_id='human_checklist', component_property='value'),
    Input(component_id='all_checklist', component_property='value'),
    Input(component_id='natural_radiobuttons', component_property='value'),
    Input(component_id='human_radiobuttons', component_property='value'),
    Input(component_id='all_radiobuttons', component_property='value'),
)
def update_plot(graph_type, natural_checklist, human_checklist, all_checklist, natural_radiobuttons, human_radiobuttons, all_radiobuttons):
    if graph_type == 'learn':
        factors = [natural_radiobuttons] + [human_radiobuttons] + [all_radiobuttons]
    elif graph_type == 'explore':
        factors = natural_checklist + human_checklist + all_checklist
    fig = px.line(land_ocean_data, x='Year', y='Annual_Mean', title="Graph", color_discrete_sequence=['black'])
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)', yaxis_zeroline=True, yaxis_zerolinecolor='gainsboro', yaxis_showline=True, yaxis_linecolor='gainsboro')
    fig = update_factors(fig, factors)
    fig.update_yaxes(title='Temperature (C)', range=[-1.2, 1.2])

    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
