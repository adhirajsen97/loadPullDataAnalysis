##Stuff to add
# 	- Plotting variable dynamic list Dropdown


# lsof -i tcp:8050
import plotly
from flask import Flask

#print(plotly.__version__)
#----------------------------------------------------------------------------------#
#Library Imports
import os, io, pickle, pathlib, statistics;
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
#----------------------------------------------------------------------------------#
#Dash Imports
import dash, base64, datetime;
#import dash_table
import dash_daq as daq
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
# Initiate global varibales that cover the scope of the entire code

global decoded, listOfDf, PICKLE_LOC, fileCheck, parsedDf, slider_range, slct, harm, slicedDfAtVarX
global btn1hist, btn2hist, btn3hist
btn1hist = btn2hist = btn3hist = 0
UPLOAD_DIRECTORY = "./app_uploaded_files"
PICKLE_LOC = None
df=pd.DataFrame()
parsedDf = pd.DataFrame()

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True, mode=0o777)
os.chmod(UPLOAD_DIRECTORY, mode=0o777)

#---------------------------------------*API Dynamic List for dropdown/Slider*-------------------------------------------#

harm_list = ["1","2","3"]

splice_option_list = ["PAE", "Pout", "Gain", "Gcomp"] # 

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

	

	html.Header(className="page-header", children = [		#------------------------Header

		html.Img(src=app.get_asset_url("logo192.png"), style={
															'float': 'left',
															'top':'10px',
															'left':'30px',
															'width': '90px',
															'position': 'relative'
														}),								
		html.Div([
		    html.H1("LoadPull Analysis Dashboard", 
		    		style={ 'margin-top':'10px', 'margin-left':'160px', 'font-size':'60px'})
		    ])
		]),
	html.Br(),
#------------------------Body
	html.Div(id = 'body', className="container-fluid flex-fill", children = [
		

			html.Div(className = "jumbotron",children = [
				html.H1("Welcome!", className="display-3",),
				html.P("This is a dashboard app to enable slicing and visualization Transistor Loadpull Data upon input of an MDF File Type.", className="lead"),
				html.Hr(className="my-4"),
				html.H5("This dashboard posseses 3 major functionalities: "),
				html.Ol(
					[
						html.Li("It uses api function calls to parse the mdf file input by our own in-built parse."),
						html.Li("Our parsed DataFrame is then fed through Dashboard used by the user to filter the DataFrame."),
						html.Li("The sliced and filtered DataFrame is used to render 3d plot using a python package, Plotly.")
					]),
				html.P(className="lead" , children = [
					html.A("Learn More.", className="btn btn-primary btn-lg", href="https://www.qorvo.com", target="_blank", role="button")
					])
				]),

			html.Div(
				[
					dcc.Upload( id='upload-data', className='btn btn-outline-info',
								children=html.Div(["Drag and drop or click to select a file to upload."]),
					
            		style = {
            			"width": "100%",
		                "height": "60px",
		                "lineHeight": "40px",
		                "borderWidth": "2px",
		                "borderStyle": "dashed",
		                "borderRadius": "5px",
		                "textAlign": "center",
		                #"padding": "20px"
		                #"margin": "10px",
            		})
            	], 
            	style = {"padding":"10px"}

            ),
			html.H5(id="output-data-upload" , style = {"width":"100%", "align":"center"}),
				#
			
		
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
						html.Label(['Select Plotting Variable'], style={'font-weight': 'bold', "text-align": "left"}),
		    			dcc.Dropdown(id="slct_plot",options=[{'label':x, 'value':x}for x in plot_option_list],
						style={'width':'250px','vertical-align':"middle", 'color': 'black'},
						placeholder='None',
						), html.Span(id='plot_message', className='badge badge-success')
					])
				])
				
			], style={"display": "flex", "flexWrap": "wrap", "position":"relative"} ),

		    

		    html.Div([
			    html.Br(),

			    html.Br(),
				
				html.Br(),
				
			]),

	            
            html.Div([
            	dbc.Row([

					dbc.Col([html.H6(id='slider-label')],style={"width":"420px"}),
            		
					dbc.Col([
						daq.Slider(
	                    id="slice",
	                    size=500,
	                    #value=5, #default value
	                    handleLabel={"showCurrentValue": True,"label": "VALUE"},
	            		)], style={"padding-top":"60px"}
	            	)
	                 
            	]),
            	dbc.Row([
            		dbc.Col([html.H6(id='slider-label-2')],style={"width":"420px"}),
            		
					dbc.Col([
						daq.Slider(
	                    id="g-comp",
	                    min=0,
	                    max=10,
	                    step=1,
	                    size=500,
	                    #value=5, #default value
	                    handleLabel={"showCurrentValue": True,"label": "VALUE"},
	            		)], style={"padding-top":"60px"}
	            	)
            	])
            	
       		], style={"display": "flex", "flexWrap": "wrap"} ),
    	

		    html.Div(id='slider-output'),
		    
			
			html.Div([
    				html.Button('Plot Scatter', id='btn-nclicks-1', className = "btn btn-primary", type="button", style={"width":"100px"}),
					html.Button('Plot Contour', id='btn-nclicks-2', className = "btn btn-primary", type="button", style={"width":"100px"}),
					html.Button('Plot Surface', id='btn-nclicks-3', className = "btn btn-primary", type="button", style={"width":"100px"}),
					html.Button('Plot --', id='btn-nclicks-4', className = "btn btn-primary", type="button", style={"width":"100px"}),

    				#html.Div(id='container-button-timestamp')
            ], style={"display": "flex", "flexWrap": "wrap", "padding":"15px", "align":"center"}),
			
		    
		    dcc.Graph(id='surface-plot', figure={}) #set proper ID
		]),

		html.Footer() #------------------------Footer
])

#----------------------------------------------------------------------------------#

#Callback Functioins 
def stale(filename):
	return dbc.Alert(id='stale',
            children=[html.B("Input a File!")],
            className="alert alert-dismissible alert-light",
            dismissable=False,
            is_open=True,
			)
def success(filename):
	return dbc.Alert(id='succ',
            children=[html.B("Success! File: \"{}\"  has been read.".format(filename))],
            className="alert alert-dismissible alert-success",
            dismissable=True,
            is_open=True,
			)
def fail(filename):
	return dbc.Alert(id='fail', 
            children=[html.B("Error Occurred! \"{}\"  is not valid file type".format(filename))],
            className="alert alert-dismissible alert-danger",
            dismissable=True,
            is_open=True,
			)


#Callback for file upload
@app.callback(

	Output(component_id='output-data-upload', component_property='children'),
	[Input(component_id='upload-data', component_property='contents'),
	Input(component_id='upload-data', component_property='filename')],
    )

def update_output(contents, names):
	global fileCheck
	children = True
	fileCheck = False
	if contents is not None:
		children = file_check(contents, names)
		fileCheck = True 
		#print(children)
		
		if children == True:
			output_data_upload = success(names)	
		elif children == False:
			output_data_upload = fail(names)
		elif children == 0:
			output_data_upload = stale(names)
				
	else:
		output_data_upload = stale(names)
	
	return output_data_upload


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


#Filename parse function to check name
def file_check(contents, filename):
	#https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
	#print(contents)
	#content_type, content_string = contents.readlines()
	filename = str(filename)
	global PICKLE_LOC
	# API function call
	# Send contents into MDF Parser
	# return DF from parser and assign to global DF variable 
	#decoded = base64.b64decode(contents)
	try:
		if '.mdf' in str(filename):
		    # Assume that the user uploaded a MDF file
			
			
			save_file(contents, filename)
			mdfLoc = str(UPLOAD_DIRECTORY+ "/" +filename)
			df = mdfParser.parseMdf(mdfLoc)
			df = mdfParser.calculateMetrics(df)
			df = mdfParser.unitConversions(df)
			filepath = UPLOAD_DIRECTORY + "/" + filename[:-4]
			PICKLE_LOC = filepath + '.pkl'
			mdfParser.exportFiles(df, filepath)
			print("Read and converted: ", filename)

			return True
		else:
			return False
		
	except ValueError:
		return False

	return 0

def save_file(content, name):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))
#----------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------#
#Callback for harm slice
@app.callback(
	[
	Output(component_id='harm_message', component_property='children'),
	Output(component_id='splicing_message', component_property='children'),
	Output(component_id='plot_message', component_property='children'),
	
	],
	[
	Input(component_id='slct_harm', component_property='value'),
	Input(component_id='slct_splice', component_property='value'),
	Input(component_id='slct_plot', component_property='value'),
	
	]
	)

def drpdowns(slct_harm, slct_splice, slct_plot):
	
	
	global slct, PICKLE_LOC, harm
	# function call to slive df
	#sliceDF(slct_harm, slct_splice, slct_plot)
	#varInfoDict = getVarRangeForSlice(harm_message, splicing_message)

	if slct_splice and PICKLE_LOC is not None:
		
		splicing_message = "Slice option chosen:  {}".format(slct_splice)
		#slct = slct_splice
		
		#print(slider_range)
	else:
		splicing_message = "Slice option chosen:  {}".format("None")

	

	'''
   
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
	harm = slct_harm
	
	plot_message = "Plotting variable chosen:  {}".format(slct_plot)


	return harm_message, splicing_message, plot_message #, fig




#----------------------------------------------------------------------------------#

@app.callback(
	[
	Output(component_id='slice', component_property='min'),
	Output(component_id='slice', component_property='max'),
	Output(component_id='slice', component_property='step'),
	#Output(component_id='slider-output', component_property='children'),
	Output(component_id='slider-label', component_property='children'),
	Output(component_id='slider-label-2', component_property='children')
	],

	[
	Input(component_id='slct_splice', component_property='value'),
	Input(component_id='slice', component_property='value'),
	Input(component_id='g-comp', component_property='value')
	]

	)
def slide(slct, slice, g_comp):
	global PICKLE_LOC, harm
	min = 0
	max = 100
	step = 1
	value = 0

	if PICKLE_LOC is not None:
		if slct is not None:
			min, max, step, value = getVarRangeForSlice(harm, slct)
			#slider_output = "Slider Value chosen:  {}".format(slice)
			slider_label = checkDrpDown(slct)
			if slct == "Gcomp":
				slider_label_2 = checkDrpDown(slct)
			else:
				slider_label_2 = checkDrpDown(None)

		
		else:
			
			#slider_output = "Slider Value chosen:  {}".format("0")
			slider_label = checkDrpDown(slct)
			pass

		
	else:
		slider_label = checkDrpDown(slct)
		
		slider_label_2 = checkDrpDown(slct)
		







	
	return min, max, step, slider_label, slider_label_2 #slider_output,

#----------------------------------------------------------------------------------#

def getVarRangeForSlice(harm, slice):
	global parsedDf, listOfDf, PICKLE_LOC
	if PICKLE_LOC:
		parsedDf = pd.read_pickle(PICKLE_LOC)
		parsedDf = dx.filterColVal(parsedDf, 'harmonic', 1, 'eq')
		parsedDf = dx.dfWithCols(parsedDf, ['gammaTuple', 'power', 'harmonic', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff',
        'r', 'jx'])
		parsedDf = dx.splitGammaTuple(parsedDf)
		listGamDf = dx.splitOnUniqueGammaTuples(parsedDf)

		df = parsedDf
		listOfDf = listGamDf 
		varInfoDict = dx.pickVariable(slice, parsedDf)

		maxV = varInfoDict['maxVal'] 
		minV = varInfoDict['minVal']
		step = varInfoDict['stepSize']
		defaultV = varInfoDict['defaultVal']
		return minV, maxV, step, defaultV

	else:
		return 0

	'''if marks:
				    step = None
				else:
				    marks = {i: i for i in range(minV, maxV + 1, step)}'''

def checkDrpDown(opt):
	global PICKLE_LOC

	if opt is not None:
		if PICKLE_LOC is None:
			return dbc.Alert( 
		        children=[html.B("Please Choose a MDF File Input First!")],
		        className="alert alert-dismissible alert-warning",
		        dismissable=False,
		        is_open=True,
				)


		return dbc.Alert(
            children=[html.B("Choose slicing value for:			\"{}\" ".format(opt))],
            className="alert alert-dismissible alert-success",
            dismissable=False,
            is_open=True,
			)
	

	return dbc.Alert( 
            children=[html.B("Please assign Slicing/Plotting Selectors ^^")],
            className="alert alert-dismissible alert-danger",
            dismissable=False,
            is_open=True,
			)

@app.callback(
	[Output(component_id='surface-plot', component_property='figure')],
	[
	Input(component_id='btn-nclicks-1', component_property='n_clicks'),
	Input(component_id='btn-nclicks-2', component_property='n_clicks'),
	Input(component_id='btn-nclicks-3', component_property='n_clicks'),
	Input(component_id='btn-nclicks-4', component_property='n_clicks'),
	Input(component_id='slct_splice', component_property='value'),
	Input(component_id='slct_plot', component_property='value'),
	Input(component_id='slice', component_property='value')]
	)

def graphing(btn_1, btn_2, btn_3, btn_4, sliceVar, slicePlot, sliceVal):
	#btn_1=btn_2=btn_3 = 0
	global btn1hist, btn2hist, btn3hist
	fig=None


	btn_1=0 if btn_1 is None else btn_1
	btn_2=0 if btn_2 is None else btn_2
	btn_3=0 if btn_3 is None else btn_3
	btn_4=0 if btn_4 is None else btn_4

	if btn_1 > btn1hist:
		fig = scatterPlot(sliceVar, sliceVal, slicePlot)
		btn1hist = btn_1
	elif btn_2 > btn2hist:
		fig = contourPlot(sliceVar, sliceVal, slicePlot)
		btn2hist = btn_2
	elif btn_3 > btn3hist:
		fig = surfacePlot(sliceVar, sliceVal, slicePlot)
		btn3hist = btn_3
	'''if btn_4> 0:
		fig = (sliceVar, sliceVal, slicePlot)'''
	

	#fig.update_traces(text = 'percent+label')
	
	
	pio.renderers.default = 'browser'
	
    # 
	return fig if fig is None else [pio.show(fig)]

	
def scatterPlot(sliceVar, sliceVal, slicePlot):
	global parsedDf, listOfDf, PICKLE_LOC 
	if listOfDf is not None:
		selList, slicedDfAtVarX = dx.interpolatedSlice(listOfDf, sliceVar, sliceVal)
		#print(slicedDfAtVarX.head())
		fig = go.Figure()
		
		fig = px.scatter(data_frame=slicedDfAtVarX, x="r", y="jx", color=slicePlot, hover_data=[slicePlot], height=700, width=700) # color='PAE' , color=slicePlot, height=600, width=600
		#fig.update_layout(legend_font_color=slicedDfAtVarX[slicePlot])
		fig.update_traces(textposition='top center')
	return fig

def contourPlot(sliceVar, sliceVal, slicePlot):
	if listOfDf is not None:
		selList, slicedDfAtVarX = dx.interpolatedSlice(listOfDf, sliceVar, sliceVal)
	
		fig = go.Figure(data =
		go.Contour(
			z= slicedDfAtVarX[slicePlot],
			x= slicedDfAtVarX['r'], # horizontal axis
			y= slicedDfAtVarX['jx'], # vertical axis
			line_smoothing=1.3
		))

		fig.update_layout(height=700, width=700)
		return fig

def surfacePlot(sliceVar, sliceVal, slicePlot):
	if listOfDf is not None:
		selList, slicedDfAtVarX = dx.interpolatedSlice(listOfDf, sliceVar, sliceVal)
		df =  slicedDfAtVarX[['r','jx', slicePlot]].copy()
		fig = go.Figure(data=[go.Surface(z=df.values)])
		fig.update_layout(title='3D '+slicePlot, autosize=False,
						width=700, height=700)
		return fig


		
		

		


#----------------------------------------------------------------------------------#

#GComp
def compressionFilteration(COMP_THRESHOLD):
	pass
	return 0 ##


#----------------------------------------------------------------------------------#





'''


@app.callback(
	[Output(component_id='slider-output', component_property='children')],
	Input(component_id='PAE', component_property='value')
	)
def sliderVal(val):
	global slider_range, parsedDf
	print(parsedDf)

	return "You have selected: {}".format(val)
'''
	
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

