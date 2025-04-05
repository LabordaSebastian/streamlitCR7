import streamlit as st
import pandas as pd
from PIL import Image
import base64

# Configuración de la página
st.set_page_config(layout="wide")

# Función para añadir imagen de fondo
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    bin_str = base64.b64encode(img_data).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: contain;
        background-position: center right;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 1;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Añadir imagen de fondo
try:
    add_bg_from_local('cr7_bg.jpg')
except:
    st.warning("No se encontró la imagen de fondo")

# Cargar el dataset
@st.cache_data
def load_data():
    file_path = "cristiano_ronaldo.csv"  # Ajusta la ruta según sea necesario
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Diseño personalizado con CSS
st.markdown("""
<style>
    /* Estilo para los selectores */
    .stMultiSelect [data-baseweb=select] span{
        max-width: 250px;
        font-size: 0.9rem;
    }
    
    /* Estilo para las tarjetas */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Estilo para el título */
    .title-text {
        color: white;
        text-shadow: 2px 2px 4px #000000;
    }
</style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.markdown('<h1 class="title-text">📊 Buscador de Estadísticas de Cristiano Ronaldo</h1>', unsafe_allow_html=True)

# Filtros en el sidebar con estilo de buscador
with st.sidebar:
    st.header("🔍 Filtros de Búsqueda")
    
    # Filtros con searchable=True para comportamiento de buscador
    season_selected = st.multiselect(
        "Temporada", 
        options=sorted(df["Season"].dropna().unique()),
        default=None,
        key="season",
        help="Busca y selecciona temporadas"
    )
    
    competition_selected = st.multiselect(
        "Competición", 
        options=sorted(df["Competition"].dropna().unique()),
        default=None,
        key="competition",
        help="Busca y selecciona competiciones"
    )
    
    club_selected = st.multiselect(
        "Club", 
        options=sorted(df["Club"].dropna().unique()),
        default=None,
        key="club",
        help="Busca y selecciona clubes"
    )
    
    opponent_selected = st.multiselect(
        "Oponente", 
        options=sorted(df["Opponent"].dropna().unique()),
        default=None,
        key="opponent",
        help="Busca y selecciona oponentes"
    )
    
    type_selected = st.multiselect(
        "Tipo de Gol", 
        options=sorted(df["Type"].dropna().unique()),
        default=None,
        key="type",
        help="Busca y selecciona tipos de gol"
    )

# Filtrar datos según selección
filter_conditions = []
if season_selected:
    filter_conditions.append(df["Season"].isin(season_selected))
if competition_selected:
    filter_conditions.append(df["Competition"].isin(competition_selected))
if club_selected:
    filter_conditions.append(df["Club"].isin(club_selected))
if opponent_selected:
    filter_conditions.append(df["Opponent"].isin(opponent_selected))
if type_selected:
    filter_conditions.append(df["Type"].isin(type_selected))

if filter_conditions:
    df_filtrado = df[pd.concat(filter_conditions, axis=1).all(axis=1)]
else:
    df_filtrado = df.copy()

# Mostrar resultados
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total de Goles", len(df_filtrado))
    st.metric("Competiciones Diferentes", df_filtrado["Competition"].nunique())
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Mostrar los datos filtrados con un expander
    with st.expander(f"📋 Mostrar datos filtrados ({len(df_filtrado)} registros)", expanded=False):
        st.dataframe(df_filtrado)

# Sección de estadísticas
st.markdown("## 📈 Análisis Visual")
tab1, tab2, tab3 = st.tabs(["Goles por Temporada", "Tipos de Gol", "Competiciones"])

# Color rojo Manchester United: #DA291C
rojo_man_u = '#DA291C'

with tab1:
    if not df_filtrado.empty:
        goles_temporada = df_filtrado["Season"].value_counts().sort_index()
        st.bar_chart(goles_temporada, use_container_width=True)

with tab2:
    if not df_filtrado.empty:
        tipos_gol = df_filtrado["Type"].value_counts()
        st.bar_chart(tipos_gol, use_container_width=True)

with tab3:
    if not df_filtrado.empty:
        competiciones = df_filtrado["Competition"].value_counts()
        st.bar_chart(competiciones, use_container_width=True)

# Nota sobre la imagen de fondo
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(0,0,0,0.7);
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 12px;
}
</style>
<div class="footer">
    App desarrollada por fans de CR7 | Imagen de fondo: Cristiano Ronaldo
</div>
""", unsafe_allow_html=True)
