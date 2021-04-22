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
import dash, base64, datetime;
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

#----------------------------------------------------------------------------------#
#Start App

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
#-----------------------------------*API Function*-----------------------------------------------#
#File Imports

directory = os.getcwd()
filepath = directory + "/DataFiles/" 
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


app.layout = html.Div(className="d-flex flex-column", children=[
html.Header(),
html.Div(className="container-fluid flex-fill", children = [
	

	html.Div([
	    html.H1("LoadPull Analysis Dashboard", 
	    		style={'text-align': 'center', 'font-size':'60px'})
	    ]),
	    html.Br(),

		html.Div(className = "jumbotron",children = [
			html.H1("Welcome!", className="display-3",),
			html.P("This is a dashboard app to help visualize and analyze Loadpull Data upon input of an MDF File.", className="lead"),
			html.Hr(className="my-4"),
			html.P("It uses utility classes for typography and spacing to space content out within the larger container."),
			html.P(className="leaad" , children = [
				html.A("Learn More.", className="btn btn-primary btn-lg", href="https://www.qorvo.com", target="_blank", role="button")
				])
			]),

		html.Div([
			dcc.Upload(
			        id='upload-data',
			        children=html.Div([
			            'Drag and Drop or ',
			            html.A('Select Files')
			        ]),
			        style={
			            'width': '20%',
			            'height': '60px',
			            'lineHeight': '60px',
			            'borderWidth': '1px',
			            'borderStyle': 'dashed',
			            'borderRadius': '5px',
			            'textAlign': 'center',
			            'margin': '10px'
			        },
			        # Allow multiple files to be uploaded
			        multiple=True
			    ),
			html.Div(id='output-data-upload')
			]),
			
		html.Hr(style={
			            'borderStyle': 'dashed',
			            'width': '5px',
			            'color': 'white'
			        }),


	    html.Div([
	    dcc.Dropdown(id="slct_harm",
	                 options=[
	                 	{'label':'1', 'value': 1},
	                    {'label':'2', 'value': 2},
	                    {'label':'3', 'value': 3}
	                 ],
	                 multi=False,
	                 value=1,
	                 style={'width':"40%", 'verticalAlign':"middle"},
	                 className='plot_selector'),
	    dcc.Dropdown(id="slct_splice",
	    			 options=[{"label":x, 'value': x} for x in splice_option_list],
	    			 multi=False,
	    			 value='-', 
	    			 className='plot_selector'),

	   ]),

	    html.Br(),

	    html.Div([
		    html.Span(id='splicing', className='badge badge-success'),
		    html.Br(),
			html.Span(id='output_container', className='badge badge-success'),
		]),
	    
	    dcc.Graph(id='surface', figure={}) #set proper ID
	]),
	html.Footer()])




#----------------------------------------------------------------------------------#
#Filename parse function to check name
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if '.mdf' in filename:
            # Assume that the user uploaded a MDF file
            print("printed")
        else:
        	return html.Div([
        				html.Div(id="file_fail",className="alert alert-dismissible alert-danger", children=[
							html.Button(type="button", className="close"),
							html.P("Failed to Read MDF File:"),
							html.H5(filename),
				        	html.H6(datetime.datetime.fromtimestamp(date))
						])
    				])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.Div(id="file_success",className="alert alert-dismissible alert-success", children=[
			html.Button(type="button", className="close"),
			html.P("Succefully Read File:"),
			html.H5(filename),
        	html.H6(datetime.datetime.fromtimestamp(date))
			])
    ])
#----------------------------------------------------------------------------------#
#Callback Functioins 

#Callback for file upload
@app.callback(
	Output(component_id='output-data-upload', component_property='children'),
	[Input(component_id='upload-data', component_property='contents')],
	[State(component_id='upload-data', component_property='filename'),
    State(component_id='upload-data', component_property='last_modified')
    ])

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#----------------------------------------------------------------------------------#
#Callback for harm sliice
@app.callback(
	Output(component_id='splicing', component_property='children'),
	[Input(component_id='slct_harm', component_property='value')
	])

def harmonic(slct_harm):#, option_splice
	#print(option_harm, option_splice, option_plot)
	splicing = "Harmonic chosen by user is: {}".format(slct_harm)

	################## Filtering DF by harmonic #######################
	#print(df["harmonic"])
	df_harm1 = df[(df["harmonic"]==slct_harm)]
	df_harm1 = df_harm1[['gammaTuple', 'power', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff', 'r', 'x']].copy()
	df.set_index(keys=['gammaTuple'], drop=False,inplace=True)
	uniqGammas=df['gammaTuple'].unique().tolist()

	listGamDf = []

	for gam in uniqGammas:
	    gamDf = df_harm1.loc[df_harm1.gammaTuple==gam]
	    gamDf.index = range(len(gamDf))
	    listGamDf.append(gamDf)
	###################################################################

	return splicing#, fig

#----------------------------------------------------------------------------------#
#Callback for splicing index variable (PAE, GAIN, GammaTuple)
@app.callback(
	Output(component_id='output_container', component_property='children'),
	[Input(component_id='slct_splice', component_property='options')]
	)
def splic1(slct_splice):
	print(type(slct_splice))
	output_container = "Splice option by user is: {}".format(slct_splice)
	return output_container

#---------------------------------*API Function Call*-------------------------------------------------#

#----------------------------------------------------------------------------------#



	
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
