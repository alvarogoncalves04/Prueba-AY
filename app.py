import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Cargar el archivo CSV
df = pd.read_csv('pitcheo.csv', encoding = 'latin-1', sep = ';')
st.set_page_config(
    page_title="Análisis de comportamiento de Pitchers",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Título de la aplicación ---
st.title("Análisis de comportamiento de Pitchers en la MLB")
st.markdown("""
            Explora el rendimiento de los pitchers en la MLB a través de visualizaciones con graficos obteniendo sus estadisticas de rendimiento.
            """)

#---Carga de datos optimizada---
@st.cache_data # Cache para optimizar la carga de datos
def load_data():
    df = pd.read_csv('pitcheo.csv', encoding='latin-1', sep=';')
    return df

df = load_data()

# --- Sidebar para filtros ---
with st.sidebar:
    st.header("Filtros de Datos")

    # Filtros por equipo, edad y innigs pitched
    equipos = df['Equipo'].unique()
    equipo_seleccionado = st.multiselect("Selecciona Equipo(s):", equipos, default=equipos)

    edades = df['Edad'].unique()
    edad_seleccionada = st.multiselect("Selecciona Edad(es):", edades, default=edades)

    innigs = df['Innings Pitched'].unique()
    innigs_seleccionada = st.multiselect("Selecciona Innings Pitched:", innigs, default=innigs)

    # Filtro por rango de ERA
    min_era = float(df['ERA'].min())
    max_era = float(df['ERA'].max())
    era_rango = st.slider("Selecciona Rango de ERA:", min_value=min_era, max_value=max_era, value=(min_era, max_era))
    
    # Filtro por rango de WHIP
    min_whip = float(df['WHIP'].min())
    max_whip = float(df['WHIP'].max())
    whip_rango = st.slider("Selecciona Rango de WHIP:", min_value=min_whip, max_value=max_whip, value=(min_whip, max_whip))

# Aplicar filtros al DataFrame
df_filtrado = df[
    (df['Equipo'].isin(equipo_seleccionado)) &
    (df['Edad'].isin(edad_seleccionada)) &
    (df['Innings Pitched'].isin(innigs_seleccionada)) &
    (df['ERA'] >= era_rango[0]) & (df['ERA'] <= era_rango[1]) &
    (df['WHIP'] >= whip_rango[0]) & (df['WHIP'] <= whip_rango[1])
]
# --- Cuerpo principal del dashboard ---
st.header("Visualizaciones de Datos")

total_teams = df_filtrado['Equipo'].nunique()
st.subheader(f"Total de Equipos Representados: {total_teams}")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
col1.metric("Total de Pitchers", f"{df_filtrado.shape[0]}")
col2.metric("ERA Promedio", f"{df_filtrado['ERA'].mean():.2f}")
col3.metric("WHIP Promedio", f"{df_filtrado['WHIP'].mean():.2f}")
col4.metric("K/9 Promedio", f"{df_filtrado['K/9'].mean():.2f}")
col5.metric("BB/9 Promedio", f"{df_filtrado['BB/9'].mean():.2f}")
col6.metric("H/9 Promedio", f"{df_filtrado['H/9'].mean():.2f}")
col7.metric("HR/9 Promedio", f"{df_filtrado['HR/9'].mean():.2f}")
col8.metric("WAR Promedio", f"{df_filtrado['WAR'].mean():.2f}")

st.markdown(f"### Total de Pitchers después de aplicar filtros: {df_filtrado.shape[0]}") 
st.dataframe(df_filtrado)
st.markdown("---")

#2. Visualizaciones 
st.subheader("Visualizaciones Interactivas")
# Gráfico de barras: Total de Pitchers por Equipo
fig1 = px.bar(df_filtrado['Equipo'].value_counts().reset_index(),
              x='index', y='Equipo',
              labels={'index': 'Equipo', 'Equipo': 'Total de Pitchers'},
              title='Total de Pitchers por Equipo',
              color='Equipo')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de dispersión: ERA vs WHIP    
fig2 = px.scatter(df_filtrado, x='ERA', y='WHIP',
                  size='K/9', color='Equipo',
                  hover_data=['Jugador', 'Edad', 'Innings Pitched'],
                  title='Relación entre ERA y WHIP',
                  labels={'ERA': 'Earned Run Average (ERA)', 'WHIP': 'Walks plus Hits per Inning Pitched (WHIP)'})
st.plotly_chart(fig2, use_container_width=True)

# Gráfico de líneas: Tendencia de ERA por Edad
fig3 = px.line(df_filtrado, x='Edad', y='ERA', color='Equipo',
                title='Tendencia de ERA por Edad',
                labels={'Edad': 'Edad', 'ERA': 'Earned Run Average (ERA)'})
st.plotly_chart(fig3, use_container_width=True)


# Gráfico de caja: Distribución de K/9 por Equipo
fig4 = px.box(df_filtrado, x='Equipo', y='K/9',
               title='Distribución de K/9 por Equipo',
               labels={'K/9': 'Strikeouts per 9 Innings (K/9)', 'Equipo': 'Equipo'})
st.plotly_chart(fig4, use_container_width=True)

# Gráfico de violín: Distribución de WHIP por Edad
fig5 = px.violin(df_filtrado, x='Edad', y='WHIP',
                  box=True, points='all',
                  title='Distribución de WHIP por Edad',
                  labels={'Edad': 'Edad', 'WHIP': 'Walks plus Hits per Inning Pitched (WHIP)'})
st.plotly_chart(fig5, use_container_width=True)

# Gráfico de barras apiladas: Total de Pitchers por Edad y Equipo
fig5b = px.histogram(df_filtrado, x='Edad', color='Equipo',
                     barmode='stack',
                     title='Total de Pitchers por Edad y Equipo',
                     labels={'Edad': 'Edad', 'count': 'Total de Pitchers'})
st.plotly_chart(fig5b, use_container_width=True)    

# Gráfico de burbujas: WAR vs Innings Pitched
fig6 = px.scatter(df_filtrado, x='Innings Pitched', y='WAR',
                  size='K/9', color='Equipo',
                  hover_data=['Jugador', 'Edad'],
                  title='Relación entre WAR y Innings Pitched',
                  labels={'Innings Pitched': 'Innings Pitched', 'WAR': 'Wins Above Replacement (WAR)'})
st.plotly_chart(fig6, use_container_width=True)

#3. Vista de datos crudos 
st.subheader("Vista de Datos Crudos")
st.dataframe(df_filtrado) 