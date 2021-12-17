#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

#Tekst toevoegen
st.markdown("""
Hier kan je je bestemming kiezen\n
""")

col1, col2, col3 = st.columns((4,4,3))


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



col1, col2, col3 = st.columns((7,2,1))

col2.write('From:')
col2.write('To:')
col2.write('flight distance:')
col2.write('flight time:')

col3.write(To_vluchten['From'][0])
col3.write(To_vluchten['To'][0])
col3.write(str(int(To_vluchten['Mean distance (km)'].mean())))
col3.write(str(int(To_vluchten['Flight time (min)'].mean())))



st.dataframe(To_vluchten)



# with st.expander('Meer informatie:'):
# 	st.subheader('Extra informatie')
# 	st.markdown('''TEKST''')


  
#my_expander = st.expander("Click here for description of models and their tasks")
