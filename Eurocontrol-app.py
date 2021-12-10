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
Welkom bij ons Dashboard over de Nederlandse Luchthavens in tijden van COVID-19!\n
\n
Wij zijn Coco de Brouwer en Inge Vijsma, derdejaars Aviation studenten en volgen momenteel de minor Data Science. 

\n
Veel plezier met het bekijken van ons interactieve Dashboard en het uitproberen van de verschillende keuzemogelijkheden!
\n
----------
""")

#Kies inspectie
st.sidebar.title("Kies inspectie")
nav = st.sidebar.radio(label = "", 
                       options = ["Histogram", "Boxplot", "Correlatie Matrix", "Spreidingsdiagram", "Kaart"])
