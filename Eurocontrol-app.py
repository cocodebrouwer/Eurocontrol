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

select = st.sidebar.selectbox('hoi', ('hey'))

# st.sidebar.title("Spinazie")
# nav_main = st.sidebar.radio(label='', options = ["Main page"])

if select == "hey":
  #Titel toevoegen
  st.title('hallo')
  st.subheader('hey')
  st.write("hoi")

#Kies inspectie
st.sidebar.title("Which user are you?")
nav = st.sidebar.radio(label='', options = ["Passengers", "Governments", "Airlines"])

if nav == "Passengers": 
  #Titel toevoegen
  st.title('Your sustainability tool')
  st.subheader('How to fly sustainable from AMS to your destination.')
  st.write("Select the desired destination in the selectbox. Choose the preferred day of travel in the days selectbox. In case the travel day doesn't matter, click on the all days button, this will show the entire flight schedule from Amsterdam to the desired destination. When everything is selected, the top three results will be displayed.")
  
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
  
  # More information
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
  
  # Begin Map
  DataDone = pd.read_csv('Datadone.csv', index_col='To')
  DataDone.drop(columns = 'Unnamed: 0', inplace = True)

  # Bepalen variabelen X en Y. 
  x = To[-4:-1]
  y = From[-4:-1]

  AvgLat = (DataDone['Latitude (From)'].loc[x] + DataDone['Latitude (To)'].loc[x])/2
  AvgLng = (DataDone['Longitude (From)'].loc[x] + DataDone['Longitude (To)'].loc[x])/2

  m = folium.Map(location=[AvgLat, AvgLng], width=750, hight=500, zoom_start=4, control_scale=True)

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

  folium_static(m)
  
  #Add black line
  st.markdown('***')
  
  st.write('***© EUROCONTROL***')

elif nav == "Governments":
  st.title('Sustainability of airlines on the AMS-network')
  st.subheader('Which airline is the most sustainable on the AMS-network?')
  st.write("Choose one or more airline(s) and/or select the desired quality mark. As a result, a ranking of the most sustainable airline, based on your selection, will appear.")
  
  Data2 = Data2.sort_values('Mean CO2 per seat per airline (kg/km)')
  
  col1, col2 = st.columns(2)
  
  Airline = Data2.sort_values('Airline')
  Airline = col1.multiselect(label='Airline', options=Airline['Airline'])
  
  Keurmerk = Data2.sort_values('Keurmerk')
  Keurmerk = col2.multiselect(label='Quality mark', options=Keurmerk['Keurmerk'].unique())
  
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
  
  with st.expander('More information:'):
        st.markdown("""**Airline:** This includes 33 airlines flying on the AMS-network.\n
  **Quality mark:** This provides information about the average CO2 emissions per seat (in kg/km) of an airline. This is then divided into five categories, shown below.\n
  A. ≤ 0.065 CO2 per seat (kg/km)\n
  B. 0.065 - 0.075 CO2 per seat (kg/km)\n
  C. 0.075 - 0.085 CO2 per seat (kg/km)\n
  D. 0.085 - 0.095 CO2 per seat (kg/km)\n
  E. > 0.095 CO2 per seat (kg/km)\n
  **CO2 (kg/km):** This provides information about the average CO2 emissions per seat (in kg/km) of an airline.""")
  
  #Add black line
  st.markdown('***')
  
  st.write('***© EUROCONTROL***')
  
elif nav == "Airlines":
  st.title('Airline comparison tool')
  st.subheader('How to improve your sustainability based on your load factor.')
  st.write("Select two airlines to compare or choose the same airline twice, to see immediately effect of the load factor. First, the quality mark and the average CO2 emissions per passenger (in kg/km), based on the average load factor in 2019, of the airlines are given. This load factor can be changed with the slider; load factor 0 means an empty aircraft and load factor 1 means a full aircraft. Changing the load factor changes the quality mark and the CO2 emissions of the airlines accordingly. This tool can be used to show the impact of the load factor on your sustainability and perhaps explore how your airline can become more sustainable.")
  
  col1, col2 = st.columns(2)
  
  Airline = Data3.sort_values('Airline')
  selectboxA = col1.selectbox(label='Airline X', options=Airline['Airline'])
  AirlineA = Data3[Data3['Airline']==selectboxA]
  loadfactorA = float(AirlineA.iloc[0,3])
  
  selectboxB = col2.selectbox(label='Airline Y', options=Airline['Airline'])
  AirlineB = Data3[Data3['Airline']==selectboxB]
  loadfactorB = float(AirlineB.iloc[0,3])
  
  loadfactorA = col1.slider(label='Load factor X', min_value=0.0, max_value=1.0, value=loadfactorA, step=0.01)
  loadfactorB = col2.slider(label='Load factor Y', min_value=0.0, max_value=1.0, value=loadfactorB, step=0.01)
  
  Data3['CO2 gem loadfactor'] = Data3['Mean CO2 per seat per airline (kg/km)'] / Data3['Loadfactor']
  Data3.loc[Data3['CO2 gem loadfactor'] <= 0.065, 'Keurmerkgem'] = 'A'
  Data3.loc[((Data3['CO2 gem loadfactor'] > 0.065) & (Data3['CO2 gem loadfactor'] <= 0.075)), 'Keurmerkgem'] = 'B'
  Data3.loc[((Data3['CO2 gem loadfactor'] > 0.075) & (Data3['CO2 gem loadfactor'] <= 0.085)), 'Keurmerkgem'] = 'C'
  Data3.loc[((Data3['CO2 gem loadfactor'] > 0.085) & (Data3['CO2 gem loadfactor'] <= 0.095)), 'Keurmerkgem'] = 'D'
  Data3.loc[Data3['CO2 gem loadfactor'] > 0.095, 'Keurmerkgem'] = 'E'
  
  Data3['CO2 loadfactorA'] = Data3['Mean CO2 per seat per airline (kg/km)'] / loadfactorA
  Data3.loc[Data3['CO2 loadfactorA'] <= 0.065, 'KeurmerkA'] = 'A'
  Data3.loc[((Data3['CO2 loadfactorA'] > 0.065) & (Data3['CO2 loadfactorA'] <= 0.075)), 'KeurmerkA'] = 'B'
  Data3.loc[((Data3['CO2 loadfactorA'] > 0.075) & (Data3['CO2 loadfactorA'] <= 0.085)), 'KeurmerkA'] = 'C'
  Data3.loc[((Data3['CO2 loadfactorA'] > 0.085) & (Data3['CO2 loadfactorA'] <= 0.095)), 'KeurmerkA'] = 'D'
  Data3.loc[Data3['CO2 loadfactorA'] > 0.095, 'KeurmerkA'] = 'E'
  
  Data3['CO2 loadfactorB'] = Data3['Mean CO2 per seat per airline (kg/km)'] / loadfactorB
  Data3.loc[Data3['CO2 loadfactorB'] <= 0.065, 'KeurmerkB'] = 'A'
  Data3.loc[((Data3['CO2 loadfactorB'] > 0.065) & (Data3['CO2 loadfactorB'] <= 0.075)), 'KeurmerkB'] = 'B'
  Data3.loc[((Data3['CO2 loadfactorB'] > 0.075) & (Data3['CO2 loadfactorB'] <= 0.085)), 'KeurmerkB'] = 'C'
  Data3.loc[((Data3['CO2 loadfactorB'] > 0.085) & (Data3['CO2 loadfactorB'] <= 0.095)), 'KeurmerkB'] = 'D'
  Data3.loc[Data3['CO2 loadfactorB'] > 0.095, 'KeurmerkB'] = 'E'
  
  AirlineA = Data3[Data3['Airline']==selectboxA]
  AirlineB = Data3[Data3['Airline']==selectboxB]
  
  
  col1, col2, col3, col4 = st.columns(4)
  
  col1.write('**Quality mark with average load factor**')
  col1.write('**CO2 (kg/km) with average load factor**')
  col1.write('**Quality mark with set load factor**')
  col1.write('**CO2 (kg/km) with set load factor**')
  
  col2.write(AirlineA.iloc[0,6])
  col2.write(str(round(AirlineA.iloc[0,5],4)))
  col2.write(AirlineA.iloc[0,8])
  col2.write(str(round(AirlineA.iloc[0,7],4)))
  
  
  col3.write('**Quality mark with average load factor**')
  col3.write('**CO2 (kg/km) with average load factor**')
  col3.write('**Quality mark with set load factor**')
  col3.write('**CO2 (kg/km) with set load factor**')
  
  col4.write(AirlineB.iloc[0,6])
  col4.write(str(round(AirlineB.iloc[0,5],4)))
  col4.write(AirlineB.iloc[0,10])
  col4.write(str(round(AirlineB.iloc[0,9],4)))
  
  #Add black line
  st.markdown('***')
  
  st.write('***© EUROCONTROL***')
