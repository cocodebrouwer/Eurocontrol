#Importeer streamlit
import streamlit as st

#Importeer de benodigde packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import seaborn as sns

#Titel toevoegen
st.title("✈️ NL luchthavens en COVID-19 ✈️")

#Tekst toevoegen
st.markdown("""
Welkom bij ons Dashboard over de Nederlandse Luchthavens in tijden van COVID-19!\n
\n
Wij zijn Coco de Brouwer en Inge Vijsma, derdejaars Aviation studenten en volgen momenteel de minor Data Science. 
Voor de eindpresentatie van het vak Visual Analytics hebben wij een Dashboard gemaakt over de bedrijvigheid van de Nederlandse Luchthavens tijdens de pandemie. 
Het Dashboard bestaat uit vijf verschillende soorten grafieken, deze zijn te selecteren in het keuzemenu.  
\n
Veel plezier met het bekijken van ons interactieve Dashboard en het uitproberen van de verschillende keuzemogelijkheden!
\n
----------
""")

#Kies inspectie
st.sidebar.title("Kies inspectie")
nav = st.sidebar.radio(label = "", 
                       options = ["Histogram", "Boxplot", "Correlatie Matrix", "Spreidingsdiagram", "Kaart"])

#--------------------
