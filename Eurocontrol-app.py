#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
# import statsmodels.api as sm
# import seaborn as sns


st.set_page_config(layout="wide")

# Data inladen
Data = pd.read_csv('PAGE1.csv')
Data2 = pd.read_csv('PAGE2.csv')
Data3 = pd.read_csv('PAGE3.csv')


#Kies inspectie
st.sidebar.title("Which user are you?")
nav = st.sidebar.radio(label='', options = ["Passengers", "Governments", "Airlines"])

if nav == "Passengers": 
  #Titel toevoegen
  st.title('Your sustainability tool')
  
  col1, col2, col3, col4 = st.columns((6,6,3,1))
  
  # From
  From = col1.selectbox(label= 'From', options= Data['From'].unique())
  
  # To
  To = col2.selectbox(label= 'To', options= Data['To'].unique())
  
  # Dagen
  To_vluchten = Data[Data['To']==To]
  
  col4.caption('All days')
  Alldays = col4.checkbox(label='', value=True)
  
  if Alldays == True:
    Weekdagen = []
  else:
    Weekdagen = To_vluchten.sort_values('Weekday number')['Weekday'].unique()
  
  Dag = col3.selectbox(label= 'Days', options= Weekdagen)
  
  
  col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((2,2,2,2,2,2,2,2))
  
  #top 3 data
  if Alldays == True:
    Dag_vluchten = To_vluchten
  else:
    Dag_vluchten = To_vluchten[To_vluchten['Weekday']==Dag]
  
  vluchten_sorted = Dag_vluchten.sort_values('Mean CO2 per pax compensated for flight time (kg)')
  vluchten_sorted = vluchten_sorted.drop_duplicates(subset=['Mean CO2 per pax compensated for flight time (kg)'])
  
  col1.write('**Ranking**')
  col2.write('**Airline**')
  col3.write('**Quality mark**')
  col4.write('**CO2 (kg)**')
  col5.write('**Number of trees**')
  col6.write('**Weekday**')
  
  range = len(vluchten_sorted.index)
  
  if range >= 1:
    col1.write('1.')
    col2.write(vluchten_sorted.iloc[0,13])
    col3.write(vluchten_sorted.iloc[0,-1])
    col4.write(str(round(vluchten_sorted.iloc[0,40],2)))
    col5.write(str(round(vluchten_sorted.iloc[0,-3],2))+ '🌳')
    col6.write(str(vluchten_sorted.iloc[0,-22]))
    
  if range >= 2:
    col1.write('2.')
    col2.write(vluchten_sorted.iloc[1,13])
    col3.write(vluchten_sorted.iloc[1,-1])
    col4.write(str(round(vluchten_sorted.iloc[1,40],2)))
    col5.write(str(round(vluchten_sorted.iloc[1,-3],2))+ '🌳')
    col6.write(str(vluchten_sorted.iloc[1,-22]))
  
  if range >= 3:
    col1.write('3.')
    col2.write(vluchten_sorted.iloc[2,13])
    col3.write(vluchten_sorted.iloc[2,-1])
    col4.write(str(round(vluchten_sorted.iloc[2,40],2)))
    col5.write(str(round(vluchten_sorted.iloc[2,-3],2))+ '🌳')
    col6.write(str(vluchten_sorted.iloc[1,-22]))
    
  col7.write('**From:**')
  col7.write('**To:**')
  col7.write('**Flight distance:**')
  col7.write('**Flight time:**')
  
  col8.write(vluchten_sorted.iloc[0,2])
  col8.write(vluchten_sorted.iloc[0,3])
  col8.write(str(int(vluchten_sorted['Mean distance (km)'].mean())) + ' km')
  col8.write(str(int(vluchten_sorted['Flight time (min)'].mean())) + ' min')

  col1, col2, col3 = st.columns((6,1,1))
  
  with col1.expander(label='INFO'):
    st.write('hier komt de uitleg voor de kolommen')
  
  # Begin Map
  DataDone = pd.read_csv('Datadone.csv', index_col='To')
  DataDone.drop(columns = 'Unnamed: 0', inplace = True)

  # Bepalen variabelen X en Y. 
  x = To[-4:-1]
  y = From[-4:-1]

  AvgLat = (DataDone['Latitude (From)'].loc[x] + DataDone['Latitude (To)'].loc[x])/2
  AvgLng = (DataDone['Longitude (From)'].loc[x] + DataDone['Longitude (To)'].loc[x])/2

  m = folium.Map(location=[AvgLat, AvgLng], width=750, height=500, zoom_start=4, control_scale=True)

  folium.Marker(location=[DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]],
                popup= '<strong>' + From + '<strong>',
                tooltip='Push to show airport code',
                icon = folium.Icon(color = 'blue', icon = 'home', prefix = 'fa')).add_to(m)

  folium.Marker(location=[DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]],
                popup= '<strong>' + To + '<strong>',
                tooltip='Push to show airport code',
                icon = folium.Icon(color = 'blue', icon = 'plane', prefix = 'fa')).add_to(m)

  points = ((DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]), 
            (DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]))

  folium.PolyLine(points, popup = '<strong>' + str(DataDone['Mean distance (km)'].loc[x]) + ' km' + '<strong>',
                  tooltip = 'Show the distance of the flight').add_to(m)

  with col1:
    folium_static(m)


elif nav == "Governments":
  st.title('Sustainability of airlines on the AMS network')
  
  Data2 = Data2.sort_values('Mean CO2 per seat per airline (kg/km)')
  
  col1, col2 = st.columns(2)
  
  Airline = Data2.sort_values('Airline')
  Airline = col1.multiselect(label='Airline', options=Airline['Airline'])
  
  Keurmerk = Data2.sort_values('Keurmerk')
  Keurmerk = col2.multiselect(label='Qualitymark', options=Keurmerk['Keurmerk'].unique())
  
  if Airline == []:
    Airlines = Data2
  else:
    Airlines = Data2.loc[Data2.apply(lambda x: x.Airline in Airline, axis=1)]
  
  if Keurmerk == []:
    Keurmerken = Data2
  else:
    Keurmerken = Data2.loc[Data2.apply(lambda x: x.Keurmerk in Keurmerk, axis=1)]
                              
  Merged = Airlines.merge(Keurmerken, on='Airline', how='inner', suffixes=('', 'delete'))
  Merged = Merged[[c for c in Merged.columns if not c.endswith('delete')]]
  Merged = Merged.sort_values('Mean CO2 per seat per airline (kg/km)')
  
  
  col1, col2, col3, col4 = st.columns(4)
  
  col1.write('**Ranking**')
  col2.write('**Airline**')
  col3.write('**Quality mark**')
  col4.write('**CO2 (kg)**')

  
  for i in range(len(Merged.index)):
    col1.write(str(i+1) + '.')
    col2.write(Merged.iloc[i,1])
    col3.write(Merged.iloc[i,3])
    col4.write(str(round(Merged.iloc[i,2],4)))
    
  with st.expander(label='INFO'):
    st.write('hier komt de uitleg voor de kolommen')   
  
  
elif nav == "Airlines":
  st.title('Airline comparison tool')
  
  col1, col2 = st.columns(2)
  
  Airline = Data3.sort_values('Airline')
  Airline1 = col1.selectbox(label='Airline 1', options=Airline['Airline'])
  Airline1 = Data3[Data3['Airline']==Airline1]
  loadfactor1 = float(Airline1.iloc[0,3])
  
  Airline2 = col2.selectbox(label='Airline 2', options=Airline['Airline'])
  Airline2 = Data3[Data3['Airline']==Airline2]
  loadfactor2 = float(Airline2.iloc[0,3])
  
  loadfactor1 = col1.slider(label='Loadfactor 1', min_value=0.0, max_value=1.0, value=loadfactor1, step=0.01)
  loadfactor2 = col2.slider(label='Loadfactor 2', min_value=0.0, max_value=1.0, value=loadfactor2, step=0.01)
  
#   st.write(Data3)
  
#   Data3['CO2 loadfactor'] = Data3['CO2 per seat per airline (kg/km)'] / Data3['Loadfactor']
#   Data3.loc[CO2 loadfactor['Mean CO2 per seat per airline (kg/km)'] <= 0.065, 'Keurmerk'] = 'A'
#   flights_seats_distance_fuel_range.loc[((flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] > 0.065) & (flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] <= 0.075)), 'Keurmerk'] = 'B'
#   flights_seats_distance_fuel_range.loc[((flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] > 0.075) & (flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] <= 0.085)), 'Keurmerk'] = 'C'
#   flights_seats_distance_fuel_range.loc[((flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] > 0.085) & (flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] <= 0.095)), 'Keurmerk'] = 'D'
#   flights_seats_distance_fuel_range.loc[flights_seats_distance_fuel_range['Mean CO2 per seat per airline (kg/km)'] > 0.095, 'Keurmerk'] = 'E'
  
#   st.write(Data3)
  
  
  col1, col2, col3, col4 = st.columns(4)
  
  col1.write('**Keurmerk met loadfactor 1**')
  col1.write('**CO2 met loadfactor 1**')
  col1.write('**Keurmerk met ingestelde loadfactor**')
  col1.write('**CO2 met ingestelde loadfactor**')
  
  col2.write(Airline1.iloc[0,4])
  col2.write(str(round(Airline1.iloc[0,2],4)))
  col2.write('test')
  col2.write('test')
  
  col3.write('**Keurmerk met loadfactor 1**')
  col3.write('**CO2 met loadfactor 1**')
  col3.write('**Keurmerk met ingestelde loadfactor**')
  col3.write('**CO2 met ingestelde loadfactor**')
  
  col4.write(Airline1.iloc[0,4])
  col4.write(str(round(Airline2.iloc[0,2],4)))
  col4.write('test')
  col4.write('test')
