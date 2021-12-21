#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# from streamlit_folium import folium_static
import folium
# import statsmodels.api as sm
# import seaborn as sns


st.set_page_config(layout="wide")

# Data inladen
Data = pd.read_csv('DATA1.csv')


#Kies inspectie
st.sidebar.title("Choose page")
nav = st.sidebar.radio(label = "", 
                       options = ["Passengers", "Airports/Governments"])

if nav == "Passenger":
  y = st.radio(label = "Kies gewenste activiteit:", 
               options = ["Totaal aantal vluchten"]) 

 
elif nav == "Airports/Governments":
  y = st.radio(label = "Kies gewenste activiteit:", 
               options = ["Totaal aantal vluchten"])

  
#Titel toevoegen
st.title("Eurocontrol Dashboard")

# #Tekst toevoegen
# st.markdown("""
# Hier kan je je bestemming kiezen\n
# """)

col1, col2, col3 = st.columns((3,3,2))


# From
From = col1.selectbox(label= 'From', options= Data['From'].unique())

# To
To = col2.selectbox(label= 'To', options= Data['To'].unique())

# Dagen
#dagen = Data
To_vluchten = Data[Data['To']==To]
Weekdagen = To_vluchten.sort_values('Weekday number')['Weekday'].unique()

# Dag = col3.radio(label= 'Dagen', options= Weekdagen)
Dag = col3.selectbox(label= 'Dagen', options= Weekdagen)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((2,2,2,2,2,2,2,2))

#top 3 data
Dag_vluchten = To_vluchten[To_vluchten['Weekday']==Dag]
vluchten_sorted = Dag_vluchten.sort_values('Mean CO2 per pax compensated for flight time (kg)')
vluchten_sorted = vluchten_sorted.drop_duplicates(subset=['Mean CO2 per pax compensated for flight time (kg)'])

col1.write('**Ranking**')
col2.write('**Airline**')
col3.write('**Quality mark**')
col4.write('**C02 (kg)**')
col5.write('**Amount of trees**')

range = len(vluchten_sorted.index)

if range >= 1:
  col1.write('1.')
  col2.write(vluchten_sorted.iloc[0,13])
  col3.write('keurmerk')
  # col4.write(str(vluchten_sorted.iloc[0,40])
  col5.write('bomen')
  
  
if range >= 2:
  col1.write('2.')
  col2.write(vluchten_sorted.iloc[1,13])
  col3.write('keurmerk')
  # col4.write(str(vluchten_sorted.iloc[0,40])
  col5.write('bomen')
  
  
if range >= 3:
  col1.write('3.')
  col2.write(vluchten_sorted.iloc[2,13])
  col3.write('keurmerk')
  # col4.write(str(vluchten_sorted.iloc[0,40])
  col5.write('bomen')


# if range == 1:
#   col1.expander('1.     ' + '1.' + "\t" + vluchten_sorted.iloc[0,13] + '"\t"hier komt het keurmerk' + "\t" + str(vluchten_sorted.iloc[0,40]))

# elif range == 2:
#   col1.expander('1.     ' + '1.' + "\t" + vluchten_sorted.iloc[0,13] + '"\t"hier komt het keurmerk' + "\t" + str(vluchten_sorted.iloc[0,40]))
#   col1.expander('2.     ' + '2.     ' + vluchten_sorted.iloc[1,13] + '        hier komt het keurmerk        ' + str(vluchten_sorted.iloc[1,40]))

# else:
#   col1.expander('1.     ' + '1.' + "\t" + vluchten_sorted.iloc[0,13] + '"\t"hier komt het keurmerk' + "\t" + str(vluchten_sorted.iloc[0,40]))
#   col1.expander('2.     ' + '2.     ' + vluchten_sorted.iloc[1,13] + '        hier komt het keurmerk        ' + str(vluchten_sorted.iloc[1,40]))
#   col1.expander('3.     ' + '3.     ' + vluchten_sorted.iloc[2,13] + '        hier komt het keurmerk        ' + str(vluchten_sorted.iloc[2,40]))


col7.write('From:')
col7.write('To:')
col7.write('flight distance:')
col7.write('flight time:')

col8.write(vluchten_sorted.iloc[0,2])
col8.write(vluchten_sorted.iloc[0,3])
col8.write(str(int(vluchten_sorted['Mean distance (km)'].mean())) + ' km')
col8.write(str(int(vluchten_sorted['Flight time (min)'].mean())) + ' min')


# st.dataframe(Data)
# st.dataframe(Dag_vluchten)
st.dataframe(vluchten_sorted)
st.write(range)



# # Begin Map
# DataDone = pd.read_csv('Datadone.csv', index_col = 'To')
# DataDone.drop(columns = 'Unnamed: 0', inplace = True)

# # Bepalen variabelen X en Y. 
# x = To
# y = From

# AvgLat = (DataDone['Latitude (From)'].loc[x] + DataDone['Latitude (To)'].loc[x])/2
# AvgLng = (DataDone['Longitude (From)'].loc[x] + DataDone['Longitude (To)'].loc[x])/2

# m = folium.Map(location=[AvgLat, AvgLng], width=750, height=500, zoom_start=4)

# folium.Marker(location=[DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]],
#               popup= '<strong>' + y + '<strong>',
#               tooltip='Push to show airport code',
#               icon = folium.Icon(color = 'blue', icon = 'home', prefix = 'fa')).add_to(m)

# folium.Marker(location=[DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]],
#               popup= '<strong>' + x + '<strong>',
#               tooltip='Push to show airport code',
#               icon = folium.Icon(color = 'blue', icon = 'plane', prefix = 'fa')).add_to(m)

# points = ((DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]), 
#           (DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]))

# folium.PolyLine(points, popup = '<strong>' + str(DataDone['Mean distance (km)'].loc[x]) + ' km' + '<strong>',
#                tooltip = 'Show the distance of the flight').add_to(m)

# m

# with st.expander('Meer informatie:'):
# 	st.subheader('Extra informatie')
# 	st.markdown('''TEKST''')
