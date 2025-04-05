import pandas as pd
import streamlit as st

df = pd.read_csv("/home/sebalaborda/Descargas/cristiano_ronaldo.csv")
print(df.head())  # Muestra las primeras filas

# Cargar el dataset
@st.cache_data
def load_data():
    file_path = "/home/sebalaborda/Descargas/cristiano_ronaldo.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()
st.write("Columnas disponibles:", df.columns.tolist())