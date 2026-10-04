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

    # Seleccionamos, dentro de la posición comparada, los valores originales por 90 minutos
    # de cada jugador para las mismas métricas que se representaron en el radar.
    player_1_values = df.loc[
        (df["Primary_Pos"] == position) & (df["Player"] == player_1), METRICS
    ].iloc[0]
    player_2_values = df.loc[
        (df["Primary_Pos"] == position) & (df["Player"] == player_2), METRICS
    ].iloc[0]

    # Convertimos las dos series en una tabla con una fila por métrica y una columna
    # por jugador; añadimos la diferencia con signo positivo cuando player_1 supera a player_2.
    comparison_df = pd.DataFrame(
        [player_1_values, player_2_values], index=[player_1, player_2]
    ).T
    comparison_df["Diferencia"] = comparison_df.iloc[:, 0] - comparison_df.iloc[:, 1]

    # Redondeamos a dos decimales para facilitar la lectura y damos un nombre explícito
    # al índice, que contiene las métricas comparadas.
    comparison_df = comparison_df.round(2)
    comparison_df.index.name = "Métrica"

    # Mostramos debajo del radar la comparación de los valores reales por 90 minutos,
    # aprovechando todo el ancho disponible en la página.
    st.subheader("Valores reales por 90 minutos")
    st.dataframe(comparison_df, use_container_width=True)