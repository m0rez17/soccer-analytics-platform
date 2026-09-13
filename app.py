"""Aplicación Streamlit para comparar jugadores mediante un gráfico radar."""

from pathlib import Path
import pandas as pd
import streamlit as st
from src.radar import plot_radar

# Configuración básica de la página
st.set_page_config(page_title="Soccer Scouting Radar", layout="centered")
st.title("⚽ Comparador de Jugadores")


# Carga de datos procesados en caché
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/df_filtered.csv", sep=";")


df = load_data()

# Métricas del modelo táctico
METRICS = ["PasTotCmp%", "PasProg", "CarPrgDist", "Tkl+Int", "Recov", "ScaPassLive"]

# 1. Filtro de posición en la barra lateral
st.sidebar.header("Filtros")
positions = sorted(df["Primary_Pos"].dropna().unique().tolist())
position = st.sidebar.selectbox("Posición", positions)

# 2. Filtrar lista de jugadores disponibles para esa posición
df_pos = df[df["Primary_Pos"] == position]
players = sorted(df_pos["Player"].dropna().unique().tolist())

if not players:
    st.warning("No hay jugadores disponibles para esta posición.")
    st.stop()

# 3. Selectores de los dos jugadores
player_1 = st.sidebar.selectbox(
    "Jugador 1", players, index=0 if len(players) > 0 else 0
)
player_2 = st.sidebar.selectbox(
    "Jugador 2", players, index=1 if len(players) > 1 else 0
)

# 4. Generar y mostrar el radar
if player_1 and player_2:
    # Invocamos plot_radar con los 6 parámetros exactos que espera
    fig, _ = plot_radar(
        df=df,
        player1=player_1,
        player2=player_2,
        position=position,
        metrics=METRICS,
        title=f"{player_1} vs {player_2} ({position})",
    )

    # Renderizar el gráfico en la interfaz
    st.pyplot(fig)