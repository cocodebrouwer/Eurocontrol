#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import seaborn as sns

#Titel toevoegen
st.title("Eurocontrol Dashboard")

#Tekst toevoegen
st.markdown("""
Tekst\n
""")

#Kies inspectie
st.sidebar.title("Choose page")
nav = st.sidebar.radio(label = "", 
                       options = ["Passengers", "Airports/Governments"])
