#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# import statsmodels.api as sm
# import seaborn as sns

# Data inladen
Data = pd.read_csv('FINAL.csv')

#Titel toevoegen
st.title("Eurocontrol Dashboard")

#Tekst toevoegen
st.markdown("""
Hier kan je je bestemming kiezen\n
""")

col1, col2 = st.beta_columns([1,1,2])



# From
From = col1.selectbox(label= 'From', options= Data['From'].unique())


# To
To = col2.selectbox(label= 'From', options= Data['To'].unique())


# with st.expander('Meer informatie:'):
# 	st.subheader('Extra informatie')
# 	st.markdown('''TEKST''')

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
  
my_expander = st.beta_expander(
        "Click here for description of models and their tasks"
    )
