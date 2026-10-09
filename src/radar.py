import numpy as np
import matplotlib.pyplot as plt


def plot_radar(df, player1, player2, position, metrics, title):
    """Genera un radar comparando dos jugadores por percentiles de posición."""
    # 1. Filtramos el DataFrame para conservar solo la posición indicada
    position_df = df.loc[df["Primary_Pos"] == position].copy()

    # 2. Calculamos el percentil de cada métrica dentro de esa posición
    percentile_df = position_df.copy()
    percentile_df[list(metrics)] = (
        position_df[list(metrics)].rank(pct=True) * 100
    )

    # 3. Buscamos los jugadores y extraemos sus valores percentiles
    players = percentile_df.set_index("Player")
    metric_names = list(metrics)
    player1_values = players.loc[player1, metric_names].to_numpy(dtype=float)
    player2_values = players.loc[player2, metric_names].to_numpy(dtype=float)

    # 4. Cerramos los polígonos repitiendo el primer ángulo y valor
    angles = np.linspace(0, 2 * np.pi, len(metric_names), endpoint=False)
    angles = np.concatenate([angles, angles[:1]])
    player1_values = np.concatenate([player1_values, player1_values[:1]])
    player2_values = np.concatenate([player2_values, player2_values[:1]])

    # 5. Creamos el gráfico polar con superficies oscuras para integrarlo con
    # Streamlit en modo oscuro, y ocultamos el borde polar para evitar un aro
    # negro que distraiga sobre el fondo.
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    ax.spines["polar"].set_visible(False)

    # La rejilla fina y semitransparente permite leer distancias y radios sin
    # competir visualmente con los perfiles de los jugadores.
    grid_color = "#4f5b66"
    ax.xaxis.grid(color=grid_color, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.yaxis.grid(color=grid_color, linestyle="--", linewidth=0.8, alpha=0.5)

    # Conservamos los percentiles en el rango 0-100 y mostramos referencias
    # cada 20 puntos; el gris claro mantiene el contraste con el fondo oscuro.
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80])
    ax.tick_params(axis="y", colors="#dcdcdc", labelsize=10)
    ax.set_rlabel_position(0)

    # Las etiquetas de cada eje describen la métrica comparada; el texto blanco
    # seminegrita y el espacio adicional separan los nombres del polígono.
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_names)
    ax.tick_params(axis="x", colors="#ffffff", labelsize=10, pad=15)
    for label in ax.get_xticklabels():
        label.set_fontweight("semibold")

    # Cian y coral distinguen claramente a ambos jugadores; los rellenos con
    # transparencia permiten ver la rejilla y cualquier zona de solapamiento.
    player1_color = "#00d4ff"
    player2_color = "#ff4b4b"
    ax.plot(
        angles,
        player1_values,
        color=player1_color,
        linewidth=2.5,
        label=player1,
    )
    ax.fill(angles, player1_values, color=player1_color, alpha=0.25)
    ax.plot(
        angles,
        player2_values,
        color=player2_color,
        linewidth=2.5,
        label=player2,
    )
    ax.fill(angles, player2_values, color=player2_color, alpha=0.25)

    # El título y la leyenda en tonos claros permanecen legibles; se reserva
    # espacio a la derecha para ubicar la leyenda fuera del área de los vértices.
    ax.set_title(title, color="#ffffff", fontsize=14, pad=25)
    fig.subplots_adjust(right=0.78)
    legend = ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.27, 1.08),
        frameon=True,
        facecolor="#0e1117",
        edgecolor="#4f5b66",
        framealpha=0.8,
    )
    for text in legend.get_texts():
        text.set_color("#ffffff")

    # Cerramos la figura en memoria para evitar renderizados duplicados en Jupyter
    plt.close(fig)

    # 6. Devolvemos la figura y el eje para permitir su reutilización
    return fig, ax