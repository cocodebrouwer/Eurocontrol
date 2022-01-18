#Import streamlit
import streamlit as st

#Import the required packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
#import statsmodels.api as sm
#import seaborn as sns

#--------------------

#Set page configuration
st.set_page_config(layout = "wide")

#--------------------

#Load the data frames
Data = pd.read_csv('PAGE1.csv')
Data2 = pd.read_csv('PAGE2.csv')
Data3 = pd.read_csv('PAGE3.csv')

#--------------------

#General information

#Set the sidebar title
st.sidebar.title("General information")

#Make a 
# main_info = st.sidebar.checkbox(label = 'Main page', value = True)
main_info = st.sidebar.button(label = 'Main page')

#--------------------

#Passengers, governments and airlines
#Set the sidebar title
st.sidebar.title("Which user are you?")

nav1 = st.sidebar.button(label = "Passenger")
nav2 = st.sidebar.button(label = "Government")
nav3 = st.sidebar.button(label = "Airline")

if 'page' not in st.session_state:
	st.session_state.page = 0
if nav1:
	st.session_state.page = 1
if nav2:
	st.session_state.page = 2
if nav3:
	st.session_state.page = 3
if main_info:
	st.session_state.page = 0


#--------------------

#Set title and subheader and write information for the guide page
if st.session_state.page == 0:
	st.title('Welcome to our dashboard!')
	st.subheader('Aviation sustainability on the AMS-network')
	st.write("""Commissioned by EUROCONTROL and as part of the minor Data Science at the Amsterdam University of Applied Sciences (AUAS), research was conducted on the sustainability of aviation on the AMS-network. The AMS-network consists of all flight routes from Amsterdam Airport Schiphol to European destinations to which at least two different airlines fly. A total of 54 European destinations and 33 airlines were investigated, through data from October and November 2021. With this information, three tools are created, each useful for a different target group. To guide you through this dashboard, the different tools are explained below.""")
	st.write("""*The different tools can be accessed via the sidebar "Which user are you?".*""")
	st.write("""**If you are a passenger...**""")
	st.write("""Sustainability is becoming increasingly important, especially in aviation. Are you someone who likes to fly but wants to pay attention to your ecological footprint, then use our tool! With this tool you can check (per day of the week) which airline offers the most sustainable flight to your chosen European destination. Thereby it is possible to see per flight how much CO2 is emitted per seat in kilograms. And if you really want to contribute, you can plant the number of trees that is indicated for your flight in order to compensate your CO2 emissions.""")
	st.write("""**If you are a member of a Dutch government agency...**""")
	st.write("""For a government agency it can be interesting to know how the airlines within a certain network perform in terms of sustainability. In this case this tool is especially useful for the Dutch government since it concerns the AMS-network. Using this tool, a number of specific airlines and/or quality marks can be selected. Based on this information, a government agency can for example take measures or issue recommendations to improve the sustainability of certain airlines.""") 
	st.write("""**If you are an airline...**""")
	st.write("""Sometimes it can be interesting to compare your own performance with another. How sustainable are you as an airline on the AMS-network compared to other airlines? With the help of this tool, two specific airlines can be compared. Sustainability can be compared based on the average load factor of 2019. Also, the load factor can be adjusted to see how you might be able to improve your sustainability with the load factor. In short, you can compare your sustainability performance with others and thereby see how you might be able to improve your own sustainability.""")
	st.write("""***Let's go for a more sustainable aviation together!***""")

	#Add a black line
	st.markdown('***')

	#Add a caption
	st.caption("""*Made by:*\n
	- *Daan Bouwmeester (500826025)*\n
	- *Coco de Brouwer (500832466)*\n
	- *Timon van Leeuwen (500782708)*\n
	- *Inge Vijsma (500819598)*""")


#Make the passengers page
if st.session_state.page == 1: 
	#Set title
	st.title('Your sustainability tool')
	#Set subheader
	st.subheader('How to fly sustainable from AMS to your destination.')
	#Write information
	st.write("Select the desired destination in the selectbox. Choose the preferred day of travel in the days selectbox. In case the travel day doesn't matter, click on the all days button, this will show the entire flight schedule from Amsterdam to the desired destination. When everything is selected, the top three results will be displayed.")
	
	#Set columns
	col1, col2, col3, col4 = st.columns((6, 6, 3, 1))
	
	#'From' selectbox
	From = col1.selectbox(label = 'From', options = Data['From'].unique())
	
	#'To' selectbox
	To = col2.selectbox(label = 'To', options = Data['To'].unique())
	
	#'Days' data
	To_vluchten = Data[Data['To'] == To]
	
	#'All days' checkbox
	col4.caption('All days')
	Alldays = col4.checkbox(label = '', value = True)
	
	if Alldays == True:
		Weekdagen = []
	else:
		Weekdagen = To_vluchten.sort_values('Weekday number')['Weekday'].unique()
	
	#'Days' selectbox
	Dag = col3.selectbox(label = 'Days', options = Weekdagen)
	
	#Set columns
	col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((2, 2, 2, 2, 2, 2, 2, 2))
	
	#Top 3 flights
	if Alldays == True:
		Dag_vluchten = To_vluchten
	else:
		Dag_vluchten = To_vluchten[To_vluchten['Weekday'] == Dag]
	
	vluchten_sorted = Dag_vluchten.sort_values('Mean CO2 per pax compensated for flight time (kg)')
	vluchten_sorted = vluchten_sorted.drop_duplicates(subset = ['Mean CO2 per pax compensated for flight time (kg)'])
	
	#Name columns
	col1.write('**Ranking**')
	col2.write('**Airline**')
	col3.write('**Quality mark**')
	col4.write('**CO2 (kg)**')
	col5.write('**Number of trees**')
	col6.write('**Weekday**')
	
	#Set index
	range = len(vluchten_sorted.index)
	
	#Set range
	if range >= 1:
		col1.write('1.')
		col2.write(vluchten_sorted.iloc[0, 13])
		col3.write(vluchten_sorted.iloc[0, -1])
		col4.write(str(round(vluchten_sorted.iloc[0, 40], 2)))
		col5.write(str(round(vluchten_sorted.iloc[0, -3], 2)) + '🌳')
		col6.write(str(vluchten_sorted.iloc[0, -22]))
		
	if range >= 2:
		col1.write('2.')
		col2.write(vluchten_sorted.iloc[1, 13])
		col3.write(vluchten_sorted.iloc[1, -1])
		col4.write(str(round(vluchten_sorted.iloc[1, 40], 2)))
		col5.write(str(round(vluchten_sorted.iloc[1, -3], 2)) + '🌳')
		col6.write(str(vluchten_sorted.iloc[1, -22]))
	
	if range >= 3:
		col1.write('3.')
		col2.write(vluchten_sorted.iloc[2, 13])
		col3.write(vluchten_sorted.iloc[2, -1])
		col4.write(str(round(vluchten_sorted.iloc[2, 40], 2)))
		col5.write(str(round(vluchten_sorted.iloc[2, -3], 2)) + '🌳')
		col6.write(str(vluchten_sorted.iloc[1, -22]))
	
	#Name columns
	col7.write('**From:**')
	col7.write('**To:**')
	col7.write('**Flight distance:**')
	col7.write('**Flight time:**')
	
	#Insert information
	col8.write(vluchten_sorted.iloc[0, 2])
	col8.write(vluchten_sorted.iloc[0, 3])
	col8.write(str(int(vluchten_sorted['Mean distance (km)'].mean())) + ' km')
	col8.write(str(int(vluchten_sorted['Flight time (min)'].mean())) + ' min')

	#Set columns
	col1, col2, col3 = st.columns((6, 1, 1))
	
	#More information expander
	with st.expander('More information:'):
		st.markdown("""**Airline:** This includes 33 airlines flying on the AMS-network.\n
			**Quality mark:** This provides information about the average CO2 emissions per seat (in kg/km) of an airline. This is then divided into five categories, shown below.\n
			A. ≤ 0.065 CO2 per seat (kg/km)\n
			B. 0.065 - 0.075 CO2 per seat (kg/km)\n
			C. 0.075 - 0.085 CO2 per seat (kg/km)\n
			D. 0.085 - 0.095 CO2 per seat (kg/km)\n
			E. > 0.095 CO2 per seat (kg/km)\n
			**CO2 (kg):** This provides the CO2 emissions per seat (in kg) for the entire flight.\n
			**Number of trees:** This indicates how much trees need to be planted in order to compensate the CO2 emissions for the flight.""")
	
	#Flight map: insert data frame, drop column
	DataDone = pd.read_csv('Datadone.csv', index_col = 'To')
	DataDone.drop(columns = 'Unnamed: 0', inplace = True)

	#Variables X and Y 
	x = To[-4:-1]
	y = From[-4:-1]

	#Latitude and longitude
	AvgLat = (DataDone['Latitude (From)'].loc[x] + DataDone['Latitude (To)'].loc[x])/2
	AvgLng = (DataDone['Longitude (From)'].loc[x] + DataDone['Longitude (To)'].loc[x])/2

	#Create the map
	m = folium.Map(location = [AvgLat, AvgLng], width = 750, height = 500, zoom_start = 4, control_scale = True)

	#Add marker
	folium.Marker(location = [DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]],
		      popup = '<strong>' + From + '<strong>',
		      tooltip = 'Push to show airport code',
		      icon = folium.Icon(color = 'blue', icon = 'home', prefix = 'fa')).add_to(m)

	folium.Marker(location = [DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]],
		      popup = '<strong>' + To + '<strong>',
		      tooltip = 'Push to show airport code',
		      icon = folium.Icon(color = 'blue', icon = 'plane', prefix = 'fa')).add_to(m)

	#Add points
	points = ((DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]), 
		  (DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]))

	#Add polyline
	folium.PolyLine(points, 
			popup = '<strong>' + str(DataDone['Mean distance (km)'].loc[x]) + ' km' + '<strong>',
			tooltip = 'Show the distance of the flight').add_to(m)

	folium_static(m)
	
	#Add black line
	st.markdown('***')
	
	#Add EUROCONTROL 
	st.write('***© EUROCONTROL***')

#--------------------

#Make the governments page
elif st.session_state.page == 2:
	#Set title
	st.title('Sustainability of airlines on the AMS-network')
	#Set subheader
	st.subheader('Which airline is the most sustainable on the AMS-network?')
	#Write information
	st.write("Choose one or more airline(s) and/or select the desired quality mark. As a result, a ranking of the most sustainable airline, based on your selection, will appear.")
	
	#Sort values
	Data2 = Data2.sort_values('Mean CO2 per seat per airline (kg/km)')
	
	#Set columns
	col1, col2 = st.columns(2)
	
	#Sort values
	Airline = Data2.sort_values('Airline')
	
	#'Airline' multiselect
	Airline = col1.multiselect(label = 'Airline', options = Airline['Airline'])
	
	#Sort values
	quality_mark = Data2.sort_values('Keurmerk')
	
	#'Quality mark' multiselect
	quality_mark = col2.multiselect(label = 'Quality mark', options = quality_mark['Keurmerk'].unique())
	
	#If-else statements
	if Airline == []:
		Airlines = Data2
	else:
		Airlines = Data2.loc[Data2.apply(lambda x: x.Airline in Airline, axis = 1)]
	
	if quality_mark == []:
		quality_marks = Data2
	else:
		quality_marks = Data2.loc[Data2.apply(lambda x: x.Keurmerk in quality_mark, axis = 1)]
	
	#Merge
	Merged = Airlines.merge(quality_marks, on = 'Airline', how = 'inner', suffixes = ('', 'delete'))
	Merged = Merged[[c for c in Merged.columns if not c.endswith('delete')]]
	Merged = Merged.sort_values('Mean CO2 per seat per airline (kg/km)')
	
	#Set columns
	col1, col2, col3, col4 = st.columns(4)
	
	#Name columns
	col1.write('**Ranking**')
	col2.write('**Airline**')
	col3.write('**Quality mark**')
	col4.write('**CO2 (kg)**')

	#Set range
	for i in range(len(Merged.index)):
		col1.write(str(i+1) + '.')
		col2.write(Merged.iloc[i, 1])
		col3.write(Merged.iloc[i, 3])
		col4.write(str(round(Merged.iloc[i, 2], 4))) 
	
	#More information expander
	with st.expander('More information:'):
		st.markdown("""**Airline:** This includes 33 airlines flying on the AMS-network.\n
			**Quality mark:** This provides information about the average CO2 emissions per seat (in kg/km) of an airline. This is then divided into five categories, shown below.\n
			A. ≤ 0.065 CO2 per seat (kg/km)\n
			B. 0.065 - 0.075 CO2 per seat (kg/km)\n
 			C. 0.075 - 0.085 CO2 per seat (kg/km)\n
			D. 0.085 - 0.095 CO2 per seat (kg/km)\n
			E. > 0.095 CO2 per seat (kg/km)\n
			**CO2 (kg/km):** This provides information about the average CO2 emissions per seat (in kg/km) of an airline.""")
	
	Merged.rename(columns = {'Unnamed: 0':'Ranking'}, inplace = True)
	Merged['Ranking'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
	Merged.to_csv('path_to_local_git_folder/Government.csv')
	
	test = pd.read_csv('Government.csv)
	st.write(test)
	
	#st.download_button(label='Download', data=csv, file_name='Government.csv', mime='text/csv')
	

	#Add a black line
	st.markdown('***')
	
	#Add EUROCONTROL
	st.write('***© EUROCONTROL***')
	
#--------------------

#Make the airlines page
elif st.session_state.page == 3:
	#Set title
	st.title('Airline comparison tool')
	#Set subheader
	st.subheader('How to improve your sustainability based on your load factor.')
	#Write information
	st.write("Select two airlines to compare or choose the same airline twice, to see immediately effect of the load factor. First, the quality mark and the average CO2 emissions per passenger (in kg/km), based on the average load factor in 2019, of the airlines are given. This load factor can be changed with the slider; load factor 0 means an empty aircraft and load factor 1 means a full aircraft. Changing the load factor changes the quality mark and the CO2 emissions of the airlines accordingly. This tool can be used to show the impact of the load factor on your sustainability and perhaps explore how your airline can become more sustainable.")
	
	#Set columns
	col1, col2 = st.columns(2)
	
	#Sort values
	Airline = Data3.sort_values('Airline')
	
	#'Airline X' selectbox
	selectboxX = col1.selectbox(label = 'Airline X', options = Airline['Airline'])
	AirlineX = Data3[Data3['Airline'] == selectboxX]
	loadfactorX = float(AirlineX.iloc[0, 3])
	
	#'Airline Y' selectbox
	selectboxY = col2.selectbox(label='Airline Y', options = Airline['Airline'])
	AirlineY = Data3[Data3['Airline'] == selectboxY]
	loadfactorY = float(AirlineY.iloc[0, 3])
	
	#Loadfactor X
	loadfactorX = col1.slider(label = 'Load factor X', min_value = 0.0, max_value = 1.0, value = loadfactorX, step = 0.01)
	
	#Loadfactor Y
	loadfactorY = col2.slider(label = 'Load factor Y', min_value = 0.0, max_value = 1.0, value = loadfactorY, step = 0.01)
	
	#Quality marks
	Data3['CO2 gem loadfactor'] = Data3['Mean CO2 per seat per airline (kg/km)']/Data3['Loadfactor']
	Data3.loc[Data3['CO2 gem loadfactor'] <= 0.065, 'Keurmerkgem'] = 'A'
	Data3.loc[((Data3['CO2 gem loadfactor'] > 0.065) & (Data3['CO2 gem loadfactor'] <= 0.075)), 'Keurmerkgem'] = 'B'
	Data3.loc[((Data3['CO2 gem loadfactor'] > 0.075) & (Data3['CO2 gem loadfactor'] <= 0.085)), 'Keurmerkgem'] = 'C'
	Data3.loc[((Data3['CO2 gem loadfactor'] > 0.085) & (Data3['CO2 gem loadfactor'] <= 0.095)), 'Keurmerkgem'] = 'D'
	Data3.loc[Data3['CO2 gem loadfactor'] > 0.095, 'Keurmerkgem'] = 'E'
	
	Data3['CO2 loadfactorA'] = Data3['Mean CO2 per seat per airline (kg/km)']/loadfactorX
	Data3.loc[Data3['CO2 loadfactorA'] <= 0.065, 'KeurmerkA'] = 'A'
	Data3.loc[((Data3['CO2 loadfactorA'] > 0.065) & (Data3['CO2 loadfactorA'] <= 0.075)), 'KeurmerkA'] = 'B'
	Data3.loc[((Data3['CO2 loadfactorA'] > 0.075) & (Data3['CO2 loadfactorA'] <= 0.085)), 'KeurmerkA'] = 'C'
	Data3.loc[((Data3['CO2 loadfactorA'] > 0.085) & (Data3['CO2 loadfactorA'] <= 0.095)), 'KeurmerkA'] = 'D'
	Data3.loc[Data3['CO2 loadfactorA'] > 0.095, 'KeurmerkA'] = 'E'
	
	Data3['CO2 loadfactorB'] = Data3['Mean CO2 per seat per airline (kg/km)']/loadfactorY
	Data3.loc[Data3['CO2 loadfactorB'] <= 0.065, 'KeurmerkB'] = 'A'
	Data3.loc[((Data3['CO2 loadfactorB'] > 0.065) & (Data3['CO2 loadfactorB'] <= 0.075)), 'KeurmerkB'] = 'B'
	Data3.loc[((Data3['CO2 loadfactorB'] > 0.075) & (Data3['CO2 loadfactorB'] <= 0.085)), 'KeurmerkB'] = 'C'
	Data3.loc[((Data3['CO2 loadfactorB'] > 0.085) & (Data3['CO2 loadfactorB'] <= 0.095)), 'KeurmerkB'] = 'D'
	Data3.loc[Data3['CO2 loadfactorB'] > 0.095, 'KeurmerkB'] = 'E'
	
	AirlineX = Data3[Data3['Airline'] == selectboxX]
	AirlineY = Data3[Data3['Airline'] == selectboxY]
	
	#Set columns
	col1, col2, col3, col4 = st.columns(4)
	
	#Name columns
	col1.write('**Quality mark with average load factor**')
	col1.write('**CO2 (kg/km) with average load factor**')
	col1.write('**Quality mark with set load factor**')
	col1.write('**CO2 (kg/km) with set load factor**')
	
	#Insert information
	col2.write(AirlineX.iloc[0, 6])
	col2.write(str(round(AirlineX.iloc[0, 5], 4)))
	col2.write(AirlineX.iloc[0, 8])
	col2.write(str(round(AirlineX.iloc[0, 7], 4)))
	
	#Name columns
	col3.write('**Quality mark with average load factor**')
	col3.write('**CO2 (kg/km) with average load factor**')
	col3.write('**Quality mark with set load factor**')
	col3.write('**CO2 (kg/km) with set load factor**')
	
	#Insert information
	col4.write(AirlineY.iloc[0, 6])
	col4.write(str(round(AirlineY.iloc[0, 5], 4)))
	col4.write(AirlineY.iloc[0, 10])
	col4.write(str(round(AirlineY.iloc[0, 9], 4)))
	
	#Add a black line
	st.markdown('***')
	
	#Add EUROCONTROL
	st.write('***© EUROCONTROL***')
