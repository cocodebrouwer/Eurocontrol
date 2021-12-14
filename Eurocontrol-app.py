#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# import statsmodels.api as sm
# import seaborn as sns


#Titel toevoegen
st.title("Eurocontrol Dashboard")

Data = pd.read_csv('FINAL.csv')

#Tekst toevoegen
st.markdown("""
Tekst\n
""")

# From
option = st.selectbox('From', Data['From'].unique())
st.write('You selected:', option)

# To
option = st.selectbox('From', Data['To'].unique())
st.write('You selected:', option)

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
