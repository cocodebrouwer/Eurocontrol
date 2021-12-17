#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
# import statsmodels.api as sm
# import seaborn as sns


st.set_page_config(layout="wide")

# Data inladen
Data = pd.read_csv('DATA.csv')


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

col1, col2, col3 = st.columns((2,2,1))


# From
From = col1.selectbox(label= 'From', options= Data['From'].unique())

# To
To = col2.selectbox(label= 'To', options= Data['To'].unique())

# Dagen
#dagen = Data
To_vluchten = Data[Data['To']==To]
Weekdagen = To_vluchten.sort_values('Weekday number')['Weekday'].unique()
#st.dataframe(vluchten)

Dag = col3.radio(label= 'Dagen', options= Weekdagen)

col1.header('TOP 3')

col1, col2 = st.columns((4,1))

st.succes('test1')
# col2.succes('test2')
# col3.succes('test3')



col1, col2, col3 = st.columns((12,2,1))

col2.write('From:')
col2.write('To:')
col2.write('flight distance:')
col2.write('flight time:')

col3.write(To_vluchten['From'][0])
col3.write(To_vluchten['To'][0])
col3.write(str(int(To_vluchten['Mean distance (km)'].mean())))
col3.write(str(int(To_vluchten['Flight time (min)'].mean())))



st.dataframe(To_vluchten)



# Begin Map
DataDone = pd.read_csv('Datadone.csv', index_col = 'To')
DataDone.drop(columns = 'Unnamed: 0', inplace = True)

# Bepalen variabelen X en Y. 
x = To
y = From

AvgLat = (DataDone['Latitude (From)'].loc[x] + DataDone['Latitude (To)'].loc[x])/2
AvgLng = (DataDone['Longitude (From)'].loc[x] + DataDone['Longitude (To)'].loc[x])/2

m = folium.Map(location=[AvgLat, AvgLng], width=750, height=500, zoom_start=4)

folium.Marker(location=[DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]],
              popup= '<strong>' + y + '<strong>',
              tooltip='Push to show airport code',
              icon = folium.Icon(color = 'blue', icon = 'home', prefix = 'fa')).add_to(m)

folium.Marker(location=[DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]],
              popup= '<strong>' + x + '<strong>',
              tooltip='Push to show airport code',
              icon = folium.Icon(color = 'blue', icon = 'plane', prefix = 'fa')).add_to(m)

points = ((DataDone['Latitude (From)'].loc[x], DataDone['Longitude (From)'].loc[x]), 
          (DataDone['Latitude (To)'].loc[x], DataDone['Longitude (To)'].loc[x]))

folium.PolyLine(points, popup = '<strong>' + str(DataDone['Mean distance (km)'].loc[x]) + ' km' + '<strong>',
               tooltip = 'Show the distance of the flight').add_to(m)

folium_static(m)

# with st.expander('Meer informatie:'):
# 	st.subheader('Extra informatie')
# 	st.markdown('''TEKST''')


  
#my_expander = st.expander("Click here for description of models and their tasks")
