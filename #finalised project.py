#finalised project
#four cities dash-tables & dash-graph

import pandas as pd
#import matplotlib.pyplot as plt #at least was useful when sketching dataframes and plots in python jupyter
import numpy as np

from dash import dcc, html, Input, Output, callback, Dash, dash_table
from dash.dependencies import Input, Output, State #this import enables us to use the current values of dataframe without triggering callback when value changes

import plotly.express as px
import plotly.graph_objs as go

pd.set_option('future.no_silent_downcasting', True) #to make .replace('NA', np.nan, inplace=True) valid in the future versions of pandas

#________________________________________________________________________
#Göteborg

pm10 = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\göteborgPM10.xlsx")
no2 = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\göteborgNO2.xlsx")

#
#clean pm10 data
pm10 = pm10.iloc[5:26, 0:6]
pm10 = pm10.drop(pm10.columns[1:4], axis = 1) #axis = 1 precises that we want to drop the columns and not the rows as here columns not stated yet
pm10.columns = ['year','to be dropped', 'mean PM10 concentration (µg/m³)']
pm10 = pm10.drop(columns = ['to be dropped'])
pm10['year'] = pm10['year'].astype(str)
pm10.set_index('year', inplace = True) #as funny issue with index in plot, might be why when not plot graph and simply use table, then no year-index appear

#
#clean data II: some values were interpreted as dates by excel
#suppressed one unimportant printing stage (sought to get matrix dimensions of dataframe)
for (row_idx, col_idx), value in zip(zip([0,1,2,3,5,9,16,20],[0,0,0,0,0,0,0,0]), [14.11, 9.34, 12.21, 12.81, 12.68, 15.03, 20.03, 21.12]): #caution with dimensions, turned pm10 into a matrix of 21rows and 1 column, and we start counting at 0 so column 0 is the only valid one
    pm10.iat[row_idx, col_idx] = value #iat is preferred to iloc as inserts individual values

#
#clean no2 data
no2 = no2.iloc[5:26, 0:6]
no2 = no2.drop(no2.columns[1:4], axis = 1)
no2.columns = ['year', 'drop', 'mean NO2 concentration (µg/m³)']
no2 = no2.drop(columns = ['drop'])
no2['year'] = no2['year'].astype(str)
no2.set_index('year', inplace = True)

#
#clean data II: some values were interpreted as dates in Excel
for (row_idx, col_idx), value in zip(zip([0,1,2,19], [0,0,0,0]), [11.41, 12.66, 12.55, 27.03]):
    no2.iat[row_idx, col_idx] = value

#
#now merge two tables on Göteborg
no2['mean PM10 concentration (µg/m³)'] = pm10['mean PM10 concentration (µg/m³)']
goteborg = no2
goteborg.columns = ['mean PM10 concentration (µg/m³)', 'mean NO2 concentration (µg/m³)'] #such that data also printed for Goteborg on Dashboard's first page, where Dropdown

goteborg['mean PM10 concentration (µg/m³)'] = pd.to_numeric(goteborg['mean PM10 concentration (µg/m³)'], errors='coerce') #to turn PM10 figures to numeric values
goteborg['mean NO2 concentration (µg/m³)'] = pd.to_numeric(goteborg['mean NO2 concentration (µg/m³)'], errors = 'coerce')

goteborg.index.astype(str) ## -> instead of int
goteborg = goteborg.reset_index() #to make data stored in index directly available for plotting (in a graph per exp.)

#methods to show decimals although non-decimal figure; however other command later in dashtable which enables this for dashboard layout
#pd.options.display.float_format = '{:,.2f}'.format #this methpd unlike next one, doesn't turn data values to strings
#goteborg = goteborg.map(lambda x: f"{x:.2f}")

#
#not essential to plot graph anymore
#goteborg.index = goteborg.index.astype(int)
#goteborg = goteborg.reset_index() #resetting index to its default value
#gtb = goteborg.plot(x='year', y=['mean NO2 concentration (µg/m³)', 'mean PM10 concentration (µg/m³)'], title="Göteborg air quality across time") #as classical version didn't work, used this method of plotting stating directly what axis referred to
#gtb.grid(True)

#years = list(range(2002, 2023))  # Assuming the data is up to 2022
#plt.xticks(ticks=range(2002, 2023), labels=[str(year) for year in range(2002, 2023)], rotation=45) #??what is rotation??

#plt.axvline(x=2013, color='r', linewidth=2, label='Policy Year')
#plt.legend()


#
#we donnot plot graph as not too useful, here no 'plt.show()', finally no graph pop-ups

#________________________________________________________________________
#London

ldn_n = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\NO2_tables_2021secondshot.xlsx", sheet_name = 'Table3_1a')
ldn_p = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\PM10_tables_2021.xlsx", sheet_name = 'Table1_1a')

#
#select NO2 data for Marylebone Road
ldn_n = ldn_n.iloc[286:311, 0:3]
ldn_n.columns = ['year', 'street', 'Annual Mean NO2 concentration (µg/m3)']
maryn = ldn_n.drop(columns = ['street'])
maryn['year'] = maryn['year'].astype(str)
maryn.set_index('year', inplace = True)

#
#select PM10 data for Marylebone Road
ldn_p = ldn_p.iloc[106:129, 0:3]
ldn_p.columns = ['year', 'street', 'Annual Mean PM10 concentration (µg/m3)']
maryp = ldn_p.drop(columns = ['street'])
maryp['year'] = maryp['year'].astype(str)
maryp.set_index('year', inplace = True)

#
#add NA for PM10 in 2020
data2020 = pd.DataFrame({'Annual Mean PM10 concentration (µg/m3)': ['NA']}, index = ['2020']) #add an extra row to "Annual Mean PM10 concentration (µg/m3)" column
maryp = pd.concat([maryp, data2020]) #concat work as append, to add element to our dataframe
maryp = maryp.sort_index(ascending = True) #sorted index such that 2020-row comes before 2021

#
#merge the two datasets and tables into one London table
maryp['Annual Mean NO2 concentr. (µg/m3)'] = maryn['Annual Mean NO2 concentration (µg/m3)'] #stick NO2 data into the maryp dataframe
maryp.columns = ['Annual Mean PM10 concentr. (µg/m3)', 'Annual Mean NO2 concentr. (µg/m3)']
mary = maryp
mary.replace('NA', np.nan, inplace = True) #turn NA string into a numpy (mathematical) NA figure, now in tables, not called NA anymore but assume data from tendency
mary['Annual Mean PM10 concentr. (µg/m3)'] = pd.to_numeric(mary['Annual Mean PM10 concentr. (µg/m3)'], errors='coerce') #to turn PM10 figures to numeric values
mary['Annual Mean NO2 concentr. (µg/m3)'] = pd.to_numeric(mary['Annual Mean NO2 concentr. (µg/m3)'], errors = 'coerce')
mary = mary.round(2) #round to two decimals
#mary.applymap(lambda x: f"{x:.2f}")
mary['Annual Mean PM10 concentr. (µg/m3)'] = mary['Annual Mean PM10 concentr. (µg/m3)'].interpolate() #to set value according to trend on NA value

#
#plot London graph
#not essential here
#mary['Annual Mean PM10 concentr. (µg/m3)'] = mary['Annual Mean PM10 concentr. (µg/m3)'].interpolate() #.interpolate() enables to ignore the NA value on the graph & avoid discountinuity on 2020 (where NA is)

#ldn = mary['1998':'2021'].plot(title = "Marylebone - central London - air quality across time ")
#ldn.set_ylabel('annual mean concentration in (µg/m3)')
#ldn.set_xlabel('years')
#ldn.grid(True)

#years = list(range(1998, 2024))
#plt.xticks(range(len(years)), years)
#plt.gca().set_xticks(range(0, len(years), 2))

#
#to enable disapearence of name "label" in dashtable of London
mary_reversed = mary.iloc[::-1].reset_index()
mary_reversed.rename(columns={'index': 'year'}, inplace=True)

#________________________________________________________________________
#Milan

file = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\Aria_2004-2021.xlsx")

file.columns = ['Labels', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004']
f = file.iloc[[4, 8]] #we have selected the rows we are interested in, don't need 2 as we created columns for dates

#
#transposing of dataframe, to make it more conventional and easier to use, and get rid of the label row
tf = f.T
tf = tf.drop('Labels')

#
#now we'll reverse the rows such that we have a dataframe and graph in increasing order
tf.columns = ['PM10 Media annua (µg/m³)', 'NO2 Media annua (µg/m³)']
#rtf = tf[::-1] #to be done later when sketching Milan graph (in Milan callback)
rtf = tf


#
#matplotlib commands to plot python graph not required anymore as to be plotted in dashboard with callbacks as done below
#Milan = rtf['2004':'2021'].plot(title = "Qualità dell'aria tra gli anni in Milano")
#Milan.set_xlabel("years")
#Milan.set_ylabel("conzentratione in (µg/m³)")
#Milan.grid(True)

#years = list(range(2004, 2024))
#plt.xticks(range(len(years)), years) #we want to show each year on the x-axis grid
#plt.gca().set_xticks(range(0, len(years), 2)) #year is labelled once in two years, "gca()" means get current axes (as we work on these), "set_xticks()" sets location of the x-axis' ticks (its labelising on the grid)

#policy_year = 2008 #use this method as simple method with two lines doesn't work in this case
#policy = policy_year - 2004 #this enables to tell that policy happens on the fourth place of the x-axis, which is 2008
#plt.axvline(x = policy, color = 'red', label = "ZTL") #introduces vertical line on graph in 2008 when policy was introduced
#plt.legend()

#
#not plot.show() as not important here (but can be done eventually)

#resetting of the index of Milan to make it function in the dashboard
rtf.reset_index(inplace=True)
rtf.columns = ['year', 'PM10 Media annua (µg/m³)', 'NO2 Media annua (µg/m³)']

#not to be done as then later suppresses values of dashboard
#rtf = rtf[['year']].applymap(str)  # Convert year entries to string

#________________________________________________________________________
#Palermo

no2 = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\2001_2022_NO2__STATISTICHE.xlsx")
pm10 = pd.read_excel(r"C:\Users\James Curtin\OneDrive\Documents\advanced programming\2002_2022_PM10__STATISTICHE.xlsx")

#clean no2 data
no2 = no2.iloc[9961:9982, 15:19]
no2.columns = ['year', 'n', 'sup200', 'NO2 conzentrazione media (µg/m³)']
no2 = no2.drop(columns = ['n', 'sup200'])
no2['year'] = no2['year'].astype(str)
no2.set_index('year', inplace = True)

#clean pm10 data
pm10 = pm10.iloc[8191:8212, 15:20]
pm10.columns = ['year', 'n', 'sup50', 'sup45', 'PM10 conzentrazione media (µg/m³)']
pm10 = pm10.drop(columns = ['n', 'sup50', 'sup45'])
pm10['year'] = pm10['year'].astype(str) #turn it back to integers??!
pm10.set_index('year', inplace = True)

#merge two tables
pm10['NO2 conzentrazione media (µg/m³)'] = no2['NO2 conzentrazione media (µg/m³)']
palermo = pm10
palermo.columns = ['PM10 conzentrazione media (µg/m³)', 'NO2 conzentrazione media (µg/m³)'] #such that in dashboard we have NO2 data first as for other tables

palermo['PM10 conzentrazione media (µg/m³)'] = pd.to_numeric(palermo['PM10 conzentrazione media (µg/m³)'], errors='coerce') #to turn PM10 figures to numeric values
palermo['NO2 conzentrazione media (µg/m³)'] = pd.to_numeric(palermo['NO2 conzentrazione media (µg/m³)'], errors = 'coerce')
#palermo = palermo.applymap(lambda x: f"{x:.2f}")

#turn Palermo dataframe to decreasing order, such that harmonised with rest of dash-tables
palermo = palermo[::-1]

#ignore unavailable data in the graph
palermo['NO2 conzentrazione media (µg/m³)'] = palermo['NO2 conzentrazione media (µg/m³)'].interpolate() #such that no discountuinity on NA values
palermo['PM10 conzentrazione media (µg/m³)'] = palermo['PM10 conzentrazione media (µg/m³)'].interpolate()

palermo = palermo.reset_index()

#
# no need to plot graph in python as will be done in callbacks for dashboard
#plm = palermo.plot(x = 'year', y=['NO2 conzentrazione media (µg/m³)', 'PM10 conzentrazione media (µg/m³)'], title = "Qalità dell'aria tra gli anni in Palermo")
#plm.grid(True)

#years = list(range(2002, 2023))
#plt.xticks(range(len(years)), years)
#plt.gca().set_xticks(range(0, len(years), 2))

#policy_year = 2016
#policy = policy_year - 2002 
#plt.axvline(x = policy, color = 'red', label = "ZTL")
#plt.legend()

#print("Note that there is unavailable data for both NO2 & PM10 in years 2018-2019-2020")
#plt.show()

#________________________________________________________________________
#Dash with Göteborg & London & Milan & Palermo

app = Dash(__name__)

app.layout = html.Div([
    #title
    html.Div(children = 'Air quality Dashboard', style={'textAlign': 'center', 'color': 'black', 'fontSize': 60, 'fontWeight': 'bold'}),
    html.Div(children = 'European cities which recently implemented urban tolls', style={'textAlign': 'center', 'color': 'black', 'fontSize': 40, 'fontWeight': 'bold'}),
    html.Hr(style={'height': '38px', 'background-color': '#FA8072', 'border': 'none'}), #displays thick empty row, of salmon color
    html.Hr(style={'height': '38px', 'background-color': '#30C6AA', 'border': 'none'}), #displays thick empty row, of turquoise color
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}), #displays thin empty row (of white colour)
    html.Div(children = 'Select both a city and a year from the following research bars', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'}),
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}),
    
    #introduce a research bar at top of Dashboard, before presenting full data
    dcc.Dropdown(
        id= 'citybar',
        options=[ #selection between four cities
            {'label': 'Göteborg', 'value': 'Göteborg'}, 
            {'label': 'London', 'value': 'London'},
            {'label': 'Milano', 'value': 'Milano'},
            {'label': 'Palermo', 'value': 'Palermo'}
        ],
        placeholder= 'select a city',
        style={
        'width': '100%',
        'color': 'black',  # Text color
        'backgroundColor': 'white',  # Dropdown background color
        'border': '1.5px solid black'  # Border properties
        }
    ),
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}),
    #will propose a dropdown for last decade's data
    dcc.Dropdown(
        id='yearbar',
        options=[{'label': str(year), 'value': str(year)} for year in reversed(range(1998, 2023))],
        placeholder= 'select a year',
        style={
        'width': '100%',
        'color': 'black',  
        'backgroundColor': 'white', 
        'border': '1.5px solid black'
        }
    ),
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}),
    html.Hr(style={'height': '38px', 'background-color': '#FA8072', 'border': 'none'}),

    #display the data for the selected city-year
    html.Div(id='city-data-output'),
    html.Hr(style={'height': '38px', 'background-color': '#30C6AA', 'border': 'none'}),
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children='The precise datatables and graphs for all four cities are available below', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'}),
    html.Hr(style={'height': '10px', 'background-color': 'white', 'border': 'none'}),

    #insert Göteborg dataframe table in app
    html.Hr(style={'height': '15px', 'background-color': 'black', 'border': 'none', 'margin': '10px 0'}), #to get a black horizontal line, and make it thicker
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = 'Air quality per decade in Göteborg', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20, 'fontWeight': 'bold'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    dash_table.DataTable(
        id = 'goteborgtable',
        columns=[
            {"name": "year", "id": "year"},  # Assuming you have a 'year' column; format not needed if it's just an identifier
            {"name": "mean NO2 concentration (µg/m³)", "id": "mean NO2 concentration (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}, #this command enables to rouund our data to two decimals
            {"name": "mean PM10 concentration (µg/m³)", "id": "mean PM10 concentration (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}
        ],
        data = goteborg.to_dict('records'), 
        page_size = 10,
        style_data_conditional=[ #set background colour to salmon in NO2 table column & to turquoise in PM10 column
            {'if': {'column_id': 'mean NO2 concentration (µg/m³)'},
            'backgroundColor': '#FA8072',
            'color': 'white'}, 
            {'if': {'column_id': 'mean PM10 concentration (µg/m³)'},
             'backgroundColor': '#30C6AA',
             'color': 'white'}
            ]
        ),
    dcc.Graph(id = 'goteborggraph'), #which can sketch graph of goteborg once we later introduce callback&function for such a graph

    #insert London dataframe table in app
    html.Hr(style={'height': '15px', 'background-color': 'black', 'border': 'none', 'margin': '10px 0'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = 'Air quality per decade in London', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20, 'fontWeight': 'bold'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = 'PM10 value for 2020 was not-assigned, therefore estimated value proposed (according to trend)', style ={'fontsize': 15}),
    dash_table.DataTable(
        id = 'londontable', #cannot have same id as previous table, if not, duplication of identity
        columns=[
            {"name": "year", "id": "year"},
            {"name": "mean NO2 concentration (µg/m³)", "id": "Annual Mean NO2 concentr. (µg/m3)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}, #this command enables to rouund our data to two decimals
            {"name": "mean PM10 concentration (µg/m³)", "id": "Annual Mean PM10 concentr. (µg/m3)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}
        ],
        data = mary_reversed.to_dict('records'),
        #data = mary.iloc[::-1].reset_index(name = 'year').to_dict('records'), #this .iloc[::-1] is meant to reverse table order, make it decreasing #this reset_index() functionality enables the year index to re-appear, as in the graph plottings, some dataframes need index-resettings
        page_size = 10,
        style_data_conditional=[ 
            {'if': {'column_id': 'Annual Mean NO2 concentr. (µg/m3)'},
            'backgroundColor': '#FA8072',
            'color': 'white'}, 
            {'if': {'column_id': 'Annual Mean PM10 concentr. (µg/m3)'},
             'backgroundColor': '#30C6AA',
             'color': 'white'}
            ]
        ),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children='CS: congestion charge introduced for Central London in 2003'),
    html.Div(children='LEZ: low emission zone only concerning high polluting diesel vehicles (such as lorries) on most of Greater London, in 2008'),
    html.Div(children='ULEZ: low emission zone expansion to all vehicles, applies only to Inner London boroughs, in 2019'),
    dcc.Graph(id='londongraph'),
    
    #insert Milan dataframe in the app
    html.Hr(style={'height': '15px', 'background-color': 'black', 'border': 'none', 'margin': '10px 0'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = "Air quality per decade in Milan", style={'textAlign': 'center', 'color': 'black', 'fontSize': 20, 'fontWeight': 'bold'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    dash_table.DataTable(
        id = 'milantable',
        columns=[
            {"name": "year", "id": "year"},
            {"name": "mean NO2 concentration (µg/m³)", "id": "NO2 Media annua (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}, #this command enables to round our data to two decimals
            {"name": "mean PM10 concentration (µg/m³)", "id": "PM10 Media annua (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}
        ],
        data = rtf.to_dict('records'),
        page_size =10,
        style_data_conditional = [
            {'if': {'column_id': 'NO2 Media annua (µg/m³)'},
            'backgroundColor' : '#FA8072',
            'color': 'white'},
            {'if': {'column_id': 'PM10 Media annua (µg/m³)'},
             'backgroundColor': '#30C6AA',
             'color': 'white'}
        ]
    ),
    dcc.Graph(id= 'milangraph'),
    
    #insert Palermo dataframe in the app
    html.Hr(style={'height': '15px', 'background-color': 'black', 'border': 'none', 'margin': '10px 0'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = 'Air quality per decade in Palermo', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20, 'fontWeight': 'bold'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.Div(children = 'NO2 & PM10 data for 2018, 2019 & 2020 were not-assigned, therefore estimated value proposed (according to trend)'),
    dash_table.DataTable(
        id = 'palermotable',
        columns=[
            {"name": "year", "id": "year"},
            {"name": "mean NO2 concentration (µg/m³)", "id": "NO2 conzentrazione media (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}, #this command enables to rouund our data to two decimals
            {"name": "mean PM10 concentration (µg/m³)", "id": "PM10 conzentrazione media (µg/m³)", "type": "numeric", 
             "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)}
        ],
        data = palermo.to_dict('records'),
        page_size = 10,
        style_data_conditional=[ 
            {'if': {'column_id': 'NO2 conzentrazione media (µg/m³)'},
            'backgroundColor': '#FA8072',
            'color': 'white'}, 
            {'if': {'column_id': 'PM10 conzentrazione media (µg/m³)'},
             'backgroundColor': '#30C6AA',
             'color': 'white'}
            ]
        ),
        dcc.Graph('palermograph'),

    #insert Radio button system for graph
    html.Hr(style={'height': '15px', 'background-color': 'black', 'border': 'none', 'margin': '10px 0'}),
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    html.H1(children = 'Air quality comarison between cities', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20, 'fontWeight': 'bold'}), 
    html.Hr(style={'height': '5px', 'background-color': 'white', 'border': 'none'}),
    dcc.RadioItems( #instead of using dcc.Dropdown, here we have dot-type to select (either NO2 or PM10)
        id = 'selection',
        options = [
            {'label': 'NO2 data', 'value': 'option1'},
            {'label': 'PM10 data', 'value': 'option2'},
            ], 
        value = 'option1',
        style={'textAlign': 'center', 'fontSize': 15, 'fontWeight': 'bold'}
        ),
    
    #insert graph of all four cities
    dcc.Graph(id = 'graph') #to enable graph after dashtables
])

#________________________________________________________________________
#Callback for research tab

from dash.exceptions import PreventUpdate

@app.callback(
        Output('city-data-output', 'children'),
        [Input('citybar', 'value'), Input('yearbar', 'value')]
)

def update_city_data(selectedcity, selectedyear):

    #to have the selection table plotted, make sure indexes are in form of strings
    goteborg['year'] = goteborg['year'].astype(str)
    palermo['year'] = palermo['year'].astype(str)
    rtf['year'] = rtf['year'].astype(str)
    mary_reversed['year'] = mary_reversed['year'].astype(str)

    if not selectedcity or not selectedyear:
        raise PreventUpdate # -> unclear!! prevents the callback from firing if mo dropdown selected
    
    if selectedcity == 'Göteborg':
        df = goteborg
    elif selectedcity == 'London':
        df = mary_reversed
    elif selectedcity == 'Milano':
        df = rtf
    elif selectedcity == 'Palermo':
        df = palermo
    else:
        return None
    
    #dataframe filtered to the selected year such that not entire DataFrame printed
    filtereddf = df[df['year'] == selectedyear] #enables filtereddf to express the selected DataFrame (df)'s data for selected year
    if filtereddf.empty:
        return "No available data for such selection"
    
    #return selection
    return dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in filtereddf.columns],
        data= filtereddf.to_dict('records'),
        #style_data_conditional= but hard to sketch as uses key name_id which is different for each city
    )

#________________________________________________________________________
#Callback for four cities' graph at bottom

@app.callback(
    Output('graph', 'figure'),
    [Input('selection', 'value')]
)

def update(value):
   
   #make the dataframe be plotted in increasing order, this also requires index to be in form of int.
   goteborg['year'] = goteborg['year'].astype(int)
   goteborgsort = goteborg.sort_values(by='year', ascending=True)
   palermo['year'] = palermo['year'].astype(int)
   palermosort = palermo.sort_values(by='year', ascending=True)
   rtf['year'] = rtf['year'].astype(int)
   rtfsort = rtf.sort_values(by='year', ascending=True)
   mary_reversed['year'] = mary_reversed['year'].astype(int)
   mary_reversedsort = mary_reversed.sort_values(by='year', ascending=True)

   if  value == 'option1':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=goteborgsort['year'], 
            y=goteborgsort['mean NO2 concentration (µg/m³)'],
            mode='lines', 
            name='Göteborg', 
            line=dict(color='#FFA07A'),
            hovertemplate='Year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=palermosort['year'], 
            y=palermosort['NO2 conzentrazione media (µg/m³)'],
            mode='lines', 
            name='Palermo', 
            line=dict(color='#FA8072'),
            hovertemplate='Year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=rtfsort['year'], 
            y=rtfsort['NO2 Media annua (µg/m³)'],
            mode = 'lines', 
            name='Milan', 
            line=dict(color='#E9967A'),
            hovertemplate='Year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=mary_reversedsort['year'], #.astype(int), #as from print(mary_reversed.dtypes) saw that not of int. type
            y=mary_reversedsort['Annual Mean NO2 concentr. (µg/m3)'],
            mode='lines', 
            name='London', 
            line=dict(color='#CD5C5C'),
            hovertemplate='Year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.update_layout(
            title='NO2 concentration comparison', 
            xaxis=dict(
                title='year',
                dtick=1,
                tickmode='linear',
                gridcolor='LightGrey'
            ),
            yaxis=dict(
                title='mean NO2 concentration (µg/m³)',
                gridcolor='LightGrey')
            )
        return fig 
    
   elif value == 'option2':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=goteborgsort['year'], 
            y=goteborgsort['mean PM10 concentration (µg/m³)'],
            mode='lines', 
            name='Göteborg', 
            line=dict(color='#40E0D0'),
            hovertemplate='Year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=palermosort['year'], 
            y=palermosort['PM10 conzentrazione media (µg/m³)'],
            mode='lines', 
            name='Palermo', 
            line=dict(color='#20B2AA'),
            hovertemplate='Year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=rtfsort['year'], 
            y=rtfsort['PM10 Media annua (µg/m³)'],
            mode= 'lines', 
            name='Milan', 
            line=dict(color='#008080'),
            hovertemplate='Year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.add_trace(go.Scatter(
            x=mary_reversedsort['year'],
            y=mary_reversedsort['Annual Mean PM10 concentr. (µg/m3)'],
            mode='lines',
            name='London',
            line=dict(color='#00CED1'), 
            hovertemplate='Year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<br><extra>%{data.name}</extra>'))
        fig.update_layout(
            title='PM10 concentration comparison', 
            xaxis=dict(
                title='year',
                dtick=1,
                tickmode='linear',
                gridcolor='LightGrey'
            ),
            yaxis=dict(
                title='mean PM10 concentration (µg/m³)',
                gridcolor='LightGrey')
            )
        return fig
   
#________________________________________________________________________
#callback for graph of goteborg (just after its table)

@app.callback(
    Output('goteborggraph', 'figure'),
    [Input('goteborgtable', 'data')]
)

def update_goteborg(data):
    if data:
        dfg = pd.DataFrame(data) #dfg for datagrame Göteborg
        dfg['year'] = dfg['year'].astype(int)
        fig = go.Figure()
        if 'mean PM10 concentration (µg/m³)' in dfg.columns:
            fig.add_trace(go.Scatter(
                x=dfg['year'], 
                y=dfg['mean NO2 concentration (µg/m³)'], 
                mode='lines', name='NO2', line=dict(color='#FA8072'),
                hovertemplate='year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<extra>NO2</extra>')) #to customize the little interactive box on each graph point
        if 'mean PM10 concentration (µg/m³)' in dfg.columns:
            fig.add_trace(go.Scatter(
                x=dfg['year'], 
                y=dfg['mean PM10 concentration (µg/m³)'], 
                mode='lines', name='PM10', 
                line=dict(color='#30C6AA'),
                hovertemplate='year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<extra>PM10</extra>'))
        fig.add_shape( #introduces policy year vertical line
            type='line',
            x0=2013,  #start of x-coordinate, year 2013 is on 11th place after 2002
            y0=0,  # start y-coordinate
            x1=2013,  # end of x-coordinate
            y1=30,  # end of y-coordinate
            line=dict(color='red', width=2, dash='dash')
        )
        #adds notation to vertical line
        fig.add_annotation(
            x=2013, 
            y=30,
            text="Jan. 2013: urban toll introduced",
            bgcolor="red"
        )
        fig.update_layout(
            xaxis=dict(
                title='year',
                dtick=1,  # sets the interval for ticks (1 year intervals)
                tickmode='linear',  # nsures linear spacing of ticks
                gridcolor='LightGrey'  # set the grid color
            ),
            yaxis=dict(
                title='concentration in (µg/m³)',
                gridcolor='LightGrey'
            ),
            hovermode='x' #highlights closest values to cursor
        )
        return fig
    
    else:
        return px.line()  # Default graph

#________________________________________________________________________
#callback for graph of London (just after its table)

#print(mary_reversed.dtypes)

@app.callback(
    Output('londongraph', 'figure'),
    [Input('londontable', 'data')]
)

def update_london(data):
    if data:
        dfl = pd.DataFrame(mary_reversed)
        dfl['year']=dfl['year'].astype(int) #to as from print(mary_reversed.dtypes) we saw that the year index was not in form of an int.
        fig = go.Figure()
        if 'Annual Mean NO2 concentr. (µg/m3)' in dfl.columns:
            fig.add_trace(go.Scatter(
                x=dfl['year'], 
                y=dfl['Annual Mean NO2 concentr. (µg/m3)'], 
                mode='lines',
                name='NO2', 
                line=dict(color='#FA8072'),
                hovertemplate='year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<extra>NO2</extra>'))
        if 'Annual Mean PM10 concentr. (µg/m3)' in dfl.columns:
            fig.add_trace(go.Scatter(
                x=dfl['year'], 
                y=dfl['Annual Mean PM10 concentr. (µg/m3)'], 
                mode='lines',
                name='PM10', 
                line=dict(color='#30C6AA'),
                hovertemplate='year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<extra>PM10</extra>'))
        fig.add_shape( 
            type='line',
            x0=2003,
            y0=0,
            x1=2003,
            y1=120,
            line=dict(color='red', width=2, dash='dash'),
            name='Urban toll introduced: congestion charge for Central London'
        )
        fig.add_annotation(
            x=2003, 
            y=120,
            text="2003: CS",
            bgcolor="red"
        )
        fig.add_shape( 
            type='line',
            x0=2008,
            y0=0,
            x1=2008,
            y1=120,
            line=dict(color='red', width=2, dash='dash'),
            name='Low emission zone introduced: LEZ -- concerning lorries mostly -- for almost entire Greater London'
        )
        fig.add_annotation(
            x=2008, 
            y=120,
            text="2008: LEZ",
            bgcolor="red"
        )
        fig.add_shape( 
            type='line',
            x0=2019,
            y0=0,
            x1=2019,
            y1=120,
            line=dict(color='red', width=2, dash='dash'),
            name='Low emission zone introduced: ULEZ for Inner London bouroughs'
        )
        fig.add_annotation(
            x=2019, 
            y=120,
            text="2019: ULEZ",
            bgcolor="red"
        )
        fig.update_layout(
            xaxis=dict(
                title='year',
                dtick=1,
                tickmode='linear',
                gridcolor='LightGrey'
            ),
            yaxis=dict(
                title='concentration in (µg/m³)',
                gridcolor='LightGrey'
            ),
            hovermode='x'
        )
        return fig
    else:
        return px.line()

#________________________________________________________________________
#callback for graph of Milan (just after its table)

@app.callback(
    Output('milangraph', 'figure'),
    [Input('milantable', 'data')] #data can be reused although used for goteborggraph, it is not an identified value so to say
)

def update_milan(data):
    if data:
        dfm = pd.DataFrame(rtf)
        fig = go.Figure()
        if 'NO2 Media annua (µg/m³)' in dfm.columns:
            fig.add_trace(go.Scatter(
                x=dfm['year'][::-1], #to sketch the years in increasing order
                y=dfm['NO2 Media annua (µg/m³)'][::-1], #as have to reverse data values corresonding to years too, now that years switched to increasing
                mode='lines', name='NO2', 
                line=dict(color='#FA8072'),
                hovertemplate='year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<extra>NO2</extra>'))
        if 'PM10 Media annua (µg/m³)' in dfm.columns:
            fig.add_trace(go.Scatter(
                x=dfm['year'][::-1], #to see years in increasing order
                y=dfm['PM10 Media annua (µg/m³)'][::-1], #as have to reverse data values corresonding to years too, now that years switched to increasing
                mode='lines', name='PM10', 
                line=dict(color='#30C6AA'),
                hovertemplate='year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<extra>PM10</extra>'))
        fig.add_shape( 
            type='line',
            x0=2008,
            y0=0,
            x1=2008,
            y1=68,
            line=dict(color='red', width=2, dash='dash')
        )
        fig.add_annotation(
            x=2008, 
            y=68,
            text="Jan. 2008: urban toll introduced",
            bgcolor="red"
        )
        fig.update_layout(
            xaxis=dict(
                title='year',
                dtick=1,
                tickmode='linear',
                gridcolor='LightGrey'
            ),
            yaxis=dict(
                title='concentration in (µg/m³)',
                gridcolor='LightGrey'
            ),
            hovermode='x'
        )
        return fig
    else:
        return px.line()

#________________________________________________________________________
#callback for graph of Palermo (just after its table)

@app.callback(
    Output('palermograph', 'figure'),
    [Input('palermotable', 'data')]
)

def update_palermo(data):
    if data:
        dfp = pd.DataFrame(palermo)
        dfp['year'] = dfp['year'].astype(int) #as year column wasn't of integer type before
        fig = go.Figure()
        if 'NO2 conzentrazione media (µg/m³)' in dfp.columns:
            fig.add_trace(go.Scatter(
                x=dfp['year'][::-1], # [::-1] operation to have panel-graph in increasing order
                y=dfp['NO2 conzentrazione media (µg/m³)'][::-1], #to have panel-graph in increasing order
                mode='lines', 
                name='NO2', 
                line=dict(color='#FA8072'),
                hovertemplate='year: %{x}<br>NO2 concentration: %{y:.2f} µg/m³<extra>NO2</extra>'))
        if 'PM10 conzentrazione media (µg/m³)' in dfp.columns:
            fig.add_trace(go.Scatter(
                x=dfp['year'][::-1], #to have panel-graph in increasing order
                y=dfp['PM10 conzentrazione media (µg/m³)'][::-1], #to have panel-graph in increasing order
                mode='lines', 
                name='PM10', 
                line=dict(color='#30C6AA'),
                hovertemplate='year: %{x}<br>PM10 concentration: %{y:.2f} µg/m³<extra>PM10</extra>'))
        fig.add_shape( 
            type='line',
            x0=2016.5,  
            y0=0,  
            x1=2016.5,  
            y1=62,
            line=dict(color='red', width=2, dash='dash'),
            name='Urban toll introduced'
        )
        fig.add_annotation(
            x=2016.5, 
            y=62,
            text="Autumn 2016: urban toll introduced",
            bgcolor="red"
        )
        fig.update_layout(
            xaxis=dict(
                title='year',
                dtick=1,
                tickmode='linear',
                gridcolor='LightGrey'
            ),
            yaxis=dict(
                title='concentration in (µg/m³)',
                gridcolor='LightGrey'
            ),
            hovermode='x'
        )
        return fig
    else:
        return px.line()

#________________________________________________________________________
#run Dash

if __name__ == '__main__':
    app.run_server(debug = True)