# lsof -i tcp:8050
import plotly
from flask import Flask

#print(plotly.__version__)
#----------------------------------------------------------------------------------#
#Library Imports
import os, io, pickle, pathlib, statistics;
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#----------------------------------------------------------------------------------#
#Dash Imports
import dash, base64, datetime;
#import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
#----------------------------------------------------------------------------------#
from loadPullDataAnalysis import mdfParser
from loadPullDataAnalysis import dataXformation as dx

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




'''directory = os.getcwd()
filepath = directory + "/DataFiles/" 
csvName = "UTD_LP_File_1.csv"
pickleName = "UTD_LP_File_1.pkl"
#df_csv = pd.read_csv(filepath + csvName) 
#df = pd.read_pickle(filepath + pickleName) '''

global decoded, df, listOfDf
UPLOAD_DIRECTORY = "./app_uploaded_files"
PICKLE_LOC = None
df=pd.DataFrame()

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True, mode=0o777)
os.chmod(UPLOAD_DIRECTORY, mode=0o777)

#---------------------------------------*API Dynamic List for dropdown/Slider*-------------------------------------------#

harm_list = ["1","2","3"]

splice_option_list = ["PAE", "Gain", "gammaTuple"]

plot_option_list = ["PAE", "Gain", "gammaTuple", "Pout"]

#------------------------------------------------------------------------------------------------#
'''  
	dcc.Dropdown(id="slct-plot",
				 options=[{"label":x, 'value': x} for x in plot_option_lst],
				 value='-',
				 className='plot_selector'), 
'''
'''
    dcc.Dropdown(id="slct_harm",options=[
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
    			 className='nav-item active')

    html.Div([
	    html.Div(id="file_success",className="alert alert-dismissible alert-success", children=[
			html.Button(type="button", className="close"),
			html.P("Succefully Read File:"),
			html.H5(filename),
	    	html.H6(datetime.datetime.fromtimestamp(date))
			])
	])
    '''


#-----------------------------------------------------------------App Layout--------------------------------------------------------------------------------#
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
				html.P("This is a dashboard app to enable slicing and visualization Transistor Loadpull Data upon input of an MDF File Type.", className="lead"),
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

			html.Div([
					
					dcc.Upload(
							id='upload-data', className='btn btn-outline-info',
							children=[
								html.Div(['Drag and Drop or', html.A('Select Files') ]),
							], 
							style={
								'width': '50%',
								'height': '60px',
								'borderRadius': '5px',
								'font-size':'30px',
								'font':'red',
								#'vertical-align':'center',
								'margin': '10px'
								},
							
						
							# <- children container
							# Allow multiple files to be uploaded
							multiple=True
					),
					html.Div(id='output-data-upload'),
			]),
				
			html.Hr(style={
				            'borderStyle': 'dashed',
				            'width': '5px',
				            'color': 'white'
				        }),

			html.Br(),
			html.Br(),
			html.H2("Slicing/Plotting Selectors: "),
		    html.Div(id="dropdown-div", children=[
				
		    	dbc.Row(id="dropdown-row", children=[
				
		    		dbc.Col(children=[
						html.Label(['Select harmonic'], style={'font-weight': 'bold', "text-align": "left"}),
		    			dcc.Dropdown(id="slct_harm", options=[{'label':x, 'value':x}for x in harm_list], 
						style={'width':'150px','vertical-align':"middle", 'color': 'black'},
						value='1',
						multi=False, 
		    			), html.Span(id='harm_message', className='badge badge-success'),
					]),
		    		dbc.Col(children=[
						html.Label(['Select Slice'], style={'font-weight': 'bold', "text-align": "left"}),
		    			dcc.Dropdown(id="slct_splice", options=[{'label':x, 'value':x}for x in splice_option_list],
						style={'width':'250px','vertical-align':"middle", 'color': 'black'},
						placeholder = 'None',
						), 
						html.Span(id='splicing_message', className='badge badge-success'),
					]),
		    		dbc.Col(children=[
						html.Label(['Select Plotting Varible'], style={'font-weight': 'bold', "text-align": "left"}),
		    			dcc.Dropdown(id="slct_plot",options=[{'label':x, 'value':x}for x in plot_option_list],
						style={'width':'250px','vertical-align':"middle", 'color': 'black'},
						placeholder='None',
						), html.Span(id='plot_message', className='badge badge-success')
					])
				])
				
			], style={"display": "flex", "flexWrap": "wrap"} ),

		    html.Br(),

		    html.Div([
			    
			    html.Br(),
				
				html.Br(),
				
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


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files
def success(filename):
	dbc.Alert(id='succ',
            children=[html.B("Success! File: \"{}\"  has been read.".format(filename))],
            className="alert alert-dismissible alert-success",
            dismissable=True,
            is_open=True,
			)
def fail(filename):
	dbc.Alert(id='fail', 
            children=[html.B("Error Occurred! \"{}\" file had a problem".format(filename))],
            className="alert alert-dismissible alert-danger",
            dismissable=True,
            is_open=True,
			)

#Filename parse function to check name
def file_check(contents, filename, date):
	#https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
	#print(contents)
	#content_type, content_string = contents.readlines()

	# API function call
	# Send contents into MDF Parser
	# return DF from parser and assign to global DF variable 
	#decoded = base64.b64decode(contents)
	try:
		if '.mdf' in filename:
		    # Assume that the user uploaded a MDF file
			global df
			save_file(contents, filename)
			mdfLoc = str(UPLOAD_DIRECTORY+ "/" +filename)
			df = mdfParser.parseMdf(mdfLoc)
			df = mdfParser.calculateMetrics(df)
			df = mdfParser.unitConversions(df)
			filepath = UPLOAD_DIRECTORY + "/" + filename[:-4]
			PICKLE_LOC = filepath + '.pkl'
			mdfParser.exportFiles(df, filepath)
			print(Read and converted)
			success(filename)

		else:
			print("NO")
			pass
			
		
			

	except Exception as e:
		return fail(filename)


	


def save_file(content, name):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))
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
            file_check(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)],
		
        return children


#----------------------------------------------------------------------------------#
#Callback for harm sliice
@app.callback(
	[
	Output(component_id='harm_message', component_property='children'),
	Output(component_id='splicing_message', component_property='children'),
	Output(component_id='plot_message', component_property='children')
	],
	[
	Input(component_id='slct_harm', component_property='value'),
	Input(component_id='slct_splice', component_property='value'),
	Input(component_id='slct_plot', component_property='value')
	]
	)

def drpdowns(slct_harm, slct_splice, slct_plot):
	
	

	# function call to slive df
	#sliceDF(slct_harm, slct_splice, slct_plot)
	#varInfoDict = getVarRangeForSlice(harm_message, splicing_message)
	try :
		if (PICKLE_LOC):
			parsedDf = pd.read_pickle(PICKLE_LOC)
			print(parsedDf.head())
	except e:
		print(e)

	
	'''
	f = open('/app_uploaded_files/UTD_LP_File_1.pkl', 'rb')
	parsedDf = pickle.load(f)
	#print(parsedDf.head())
	
				parsedDf = dx.filterColVal(parsedDf, 'harmonic', 1, 'eq')
				parsedDf = dx.dfWithCols(parsedDf, ['gammaTuple', 'power', 'harmonic', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff',
			        'r', 'jx'])
				parsedDf = dx.splitGammaTuple(parsedDf)
				listGamDf = dx.splitOnUniqueGammaTuples(parsedDf)
				listOfDf = listGamDf
				varInfoDict = dx.pickVariable(slice, parsedDf)
	
	maxV = varInfoDict['maxVal'] 
	minV = varInfoDict['minVal']
	step = varInfoDict['stepSize']
	defaultV = varInfoDict['defaultVal']
   
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
	'''
	###################################################################

	harm_message = "Harmonic set to:  {}".format(slct_harm)
	splicing_message = "Slice option chosen:  {}".format(slct_splice)
	plot_message = "Plotting variable chosen:  {}".format(slct_plot)

	return harm_message, splicing_message, plot_message#, fig

#----------------------------------------------------------------------------------#



#---------------------*API Function Call(slice DF)*--------------------------------#
def getVarRangeForSlice(harm, slice):
	global df, listOfDf
	parsedDf = df.copy()
	parsedDf = dx.filterColVal(parsedDf, 'harmonic', 1, 'eq')
	parsedDf = dx.dfWithCols(parsedDf, ['gammaTuple', 'power', 'harmonic', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff',
        'r', 'jx'])
	parsedDf = dx.splitGammaTuple(parsedDf)
	listGamDf = dx.splitOnUniqueGammaTuples(parsedDf)
	df = parsedDf
	listOfDf = listGamDf
	varInfoDict = dx.pickVariable(slice, parsedDf)
	print(varInfoDict)
	

	

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

@server.route("/api-calls/")
def function_calls():
	return 0

if __name__ == '__main__':
	app.run_server(debug=True)

