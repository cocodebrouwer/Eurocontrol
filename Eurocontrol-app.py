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
Data = pd.read_csv('DATA1.csv')


#Kies inspectie
st.sidebar.title("Choose page")
nav = st.sidebar.radio(label = "", 
                       options = ["Passengers", "Governments"])

if nav == "Passengers": 
  #Titel toevoegen
  st.title("Eurocontrol Dashboard for passengers")
  
  col1, col2, col3, col4 = st.columns((6,6,3,1))
  
  # From
  From = col1.selectbox(label= 'From', options= Data['From'].unique())
  
  # To
  To = col2.selectbox(label= 'To', options= Data['To'].unique())
  
  # Dagen
  #dagen = Data
  To_vluchten = Data[Data['To']==To]
  Weekdagen = To_vluchten.sort_values('Weekday number')['Weekday'].unique()
  Dag = col3.selectbox(label= 'Days', options= Weekdagen)
  # Dag = col3.selectbox(label= 'Days', options= ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
  
  
  col4.caption('All')
  Alldays = col4.checkbox(label='', value=True)
  
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
    col5.write(str(round(vluchten_sorted.iloc[0,-3],2))+ '🌳', help = 'extra info')
    col6.write(str(vluchten_sorted.iloc[0,-22]))
    
  if range >= 2:
    col1.write('2.')
    col2.write(vluchten_sorted.iloc[1,13])
    col3.write(vluchten_sorted.iloc[1,-1])
    col4.write(str(round(vluchten_sorted.iloc[1,40],2)))
    col5.write(str(round(vluchten_sorted.iloc[1,-3],2))+ '🌳', help = 'extra info')
    col6.write(str(vluchten_sorted.iloc[1,-22]))
  
  if range >= 3:
    col1.write('3.')
    col2.write(vluchten_sorted.iloc[2,13])
    col3.write(vluchten_sorted.iloc[2,-1])
    col4.write(str(round(vluchten_sorted.iloc[2,40],2)))
    col5.write(str(round(vluchten_sorted.iloc[2,-3],2))+ '🌳', help = 'extra info')
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
    
  # st.dataframe(vluchten_sorted)



elif nav == "Governments":
  st.title("Eurocontrol Dashboard for gevernments")
  
  col1, col2 = st.columns(2)
  
  Airline = col1.selectbox(label='Airline', options=Data['Airline'].unique())
                   
  Keurmerk = col2.multiselect(label='Qualitymark', options=Data['Keurmerk'].unique())
  
  Airlines = Data[Data['Airline'] == Airline]
                              
  
  
  st.dataframe(Airlines)
