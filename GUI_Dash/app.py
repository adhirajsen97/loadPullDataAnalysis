import plotly
from flask import Flask
plotly.__version__
#----------------------------------------------------------------------------------#
#Library Imports
import os, pathlib, statistics;
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#----------------------------------------------------------------------------------#
#Dash Imports
import dash, datetime;
#import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
'''
Requirements: 
Plotly
flask
pandas
plotly.express
plotly.graph_objects
dash
dash_core_components 
dash_html_components
dash_bootstrap_components
dash.dependencies : Input, Output, State
'''

#-------------------------------------*Start App*------------------------------------------------#
#Start App
server = Flask(__name__)
app = dash.Dash(
	__name__,
	server=server,
	url_base_pathname='/LoadPull-Dashboard/',
	external_stylesheets=[dbc.themes.SUPERHERO]
	)

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
app.layout = html.Div(className="d-flex flex-column", id='dash-container', children=[

	
#------------------------Header
	html.Header([	
		html.Img(src=app.get_asset_url("logo192.png"), style={'top':'10px',
															'left':'30px',
															'float': 'left',
															'width': '6%',
															'position': 'absolute'
														}),								
		html.Div([
		    html.H1("LoadPull Analysis Dashboard", 
		    		style={ 'margin-top':'10px', 'margin-left':'160px', 'font-size':'60px'})
		    ])
	

		]),
	html.Br(),
#------------------------Body
	html.Div(className="container-fluid flex-fill", children = [
		
		

			html.Div(className = "jumbotron",children = [
				html.H1("Welcome!", className="display-3",),
				html.P("This is a dashboard app to help visualize and analyze Transistor Loadpull Data upon input of an MDF File.", className="lead"),
				html.Hr(className="my-4"),
				html.P( ["This dashboard posseses 3 major functionalities: ",
						html.Br(),
						" 1) It uses api function calls to parse the mdf file input by our own in-built parse.",
						html.Br(),
						"2) Our parsed DataFrame is then fed through Dashboard used by the user to filter the DataFrame.",
						html.Br(),
						"3) The spliced and filtered DataFrame is used to render 3d plot using a python package, Plotly."]),
				html.P(className="lead" , children = [
					html.A("Learn More.", className="btn btn-primary btn-lg", href="https://www.qorvo.com", target="_blank", role="button")
					])
				]),

			html.Div(id='upload-container', children=[
				dcc.Upload(
				        id='upload-data',
				        children=html.Div([
				        	html.Button(className='btn btn-outline-info',type='radio', autoFocus=True, children=[
				        		'Drag and Drop or ',
				            	html.A('Select Files'),
				            	
			        		], 
			        		style={
					            'width': '40%',
					            'height': '60px',
					            'lineHeight': '60px',
					            #'borderWidth': '1px',
					            #'borderStyle': 'dashed',
					            'borderRadius': '5px',
					            'textAlign': 'center',
					            'vertical-align':'center',
					            'margin': '10px'
					        }),
			        		
				        ]), # <- children container
				        # Allow multiple files to be uploaded
				        multiple=True
				    ),
				html.Div(id='output-data-upload')
				], style={'text-align':'center', 'borderRadius': '5px', 'borderStyle': 'dashed'}),
				
			html.Hr(style={
				            'borderStyle': 'dashed',
				            'width': '5px',
				            'color': 'white'
				        }),


		    html.Div(className='drpdowns', children = [
		    dcc.Dropdown(id="slct_harm", options=[
		                 	{'label':'1', 'value': 1},
		                    {'label':'2', 'value': 2},
		                    {'label':'3', 'value': 3}],
		                 multi=False,
		                 value=1,
		                 style={'width':"40%", 'verticalAlign':"middle"},
		                 className='plot_selector',
		                 ),

		    dcc.Dropdown(id="slct_splice",
		    			 options=[{"label":x, 'value': x} for x in splice_option_list],
		    			 multi=False,
		    			 value='-', 
		    			 style={'width':"60%", 'verticalAlign':"middle"},
		    			 className='plot_selector')

		   ]),

		    html.Br(),

		    html.Div([
			    html.Span(id='splicing', className='badge badge-success'),
			    html.Br(),
				html.Span(id='output_container', className='badge badge-success'),
			]),

			html.Div([
				dcc.ConfirmDialog(
		        id='confirm',
		        message='Danger danger! Are you sure you want to continue?',
		    	)

			]),
			
		    
		    dcc.Graph(id='surface', figure={}) #set proper ID
		]),
#------------------------Footer
		html.Footer()
])


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
			return dbc.Alert(
            html.B("Error! \"{}\" is not a valid .mdf file.".format(filename)),
            className="alert alert-dismissible alert-danger",
            dismissable=True,
            is_open=True,
        	)
			'''html.Div([ html.Div(id="file_fail",className="alert alert-dismissible alert-danger", children=[
																html.Button(type="button", className="close"),
																"Failed to Read MDF File: ", html.U(filename), 
																html.H6(datetime.datetime.fromtimestamp(date))
															])
														])'''

	except Exception as e:
		print(e)
		return html.Div(['Error occurred! Please try again.'])

	return dbc.Alert(
            html.B("Success! File: \"{}\"  has been read.".format(filename)),
	    	
            className="alert alert-dismissible alert-success",
            dismissable=True,
            is_open=True,
        	)


	html.Div([
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
	[Input(component_id='slct_splice', component_property='value')]
	)
def splic1(value):
	print(type(value))
	output_container = "Splice option by user is: {}".format(value)
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

@server.route("/LoadPull-Dashboard/")
def my_dash_app():
    return app.index()

if __name__ == '__main__':
	app.run_server(debug=True)

