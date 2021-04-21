import plotly
plotly.__version__
#----------------------------------------------------------------------------------#
#Library Imports
import os, pathlib, statistics;
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#----------------------------------------------------------------------------------#
#Dash Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#----------------------------------------------------------------------------------#
#Start App

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
#-----------------------------------*API Function*-----------------------------------------------#
#File Imports

directory = os.getcwd()
p = pathlib.Path(directory)
parentDir= str(p.parents[0])

filepath = parentDir + "/DataFiles/" 
csvName = "UTD_LP_File_1.csv"
pickleName = "UTD_LP_File_1.pkl"
#df_csv = pd.read_csv(filepath + csvName) 
df = pd.read_pickle(filepath + pickleName) 
#---------------------------------------*API Function*-------------------------------------------#

splice_option_list = list(['PAE','Gain','gammaTuple'])

plot_option_lst = list([])

#------------------------------------------------------------------------------------------------#
'''
    
        
	dcc.Dropdown(id="slct-plot",
				 options=[{"label":x, 'value': x} for x in plot_option_lst],
				 value='-',
				 className='plot_selector'),
'''


#App Layout
app.layout = html.Div([
    html.H1("LoadPull Analysis Dashboard", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct-harm",
                 options=[
                 	{"label":"1", "value": 1},
                    {"label":"2", "value": 2},
                    {"label":"3", "value": 3}],
                 multi=False,
                 value=1,
                 style={'width':"40%", 'verticalAlign':"middle"},
                 className='plot_selector'),

    dcc.Dropdown(id="slct-splice",
    			 options=[{"label":x, 'value': x} for x in splice_option_list],
    			 multi=False,
    			 value='-', 
    			 className='plot_selector'),


    html.Div(id='splicing'),

    html.Br(),

    html.Div(id='output_container'),
    
    
    dcc.Graph(id='surface', figure={}) #set proper ID
])
#----------------------------------------------------------------------------------#
@app.callback(
	[Output(component_id='splicing', component_property='children'),
	Input(component_id='slct-harm', component_property='options'),
	Input(component_id='slct-splice', component_property='options')
	])
#----------------------------------------------------------------------------------#
def change_DF(option_harm, option_splice):
	#print(option_harm, option_splice, option_plot)
	print(type(option_harm))
	print(option_splice)


	container = "Harmonic chosen by user is: {}".format(option_harm)

	#---------------------------------*API Function Call*-------------------------------------------------#
	print(df["harmonic"])
	df_harm1 = df[(df["harmonic"]==option_harm)]
	df_harm1 = df_harm1[['gammaTuple', 'power', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff', 'r', 'x']].copy()
	df.set_index(keys=['gammaTuple'], drop=False,inplace=True)
	uniqGammas=df['gammaTuple'].unique().tolist()

	listGamDf = []

	for gam in uniqGammas:
	    gamDf = df_harm1.loc[df_harm1.gammaTuple==gam]
	    gamDf.index = range(len(gamDf))
	    listGamDf.append(gamDf)
	#----------------------------------------------------------------------------------#



	return container#, fig
'''
@app.callback([
	Output(component_id='output_container', component_property='children'),
	Output(component_id='surface', component_property='figure'),
	Input(component_id='slct-splice', component_property='options')
	#Input(component_id='slct-plot', component_property='options', classname='plot_selector')
	])
def update_graph(option_splice):
	print(option_Splice)
	contaner


def spliced():
	return 0
'''

#----------------------------------------------------------------------------------#

if __name__ == '__main__':
	app.run_server(debug=True)
