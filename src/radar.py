import numpy as np
import matplotlib.pyplot as plt


def plot_radar(df, player1, player2, position, metrics, title):
	"""Genera un radar comparando dos jugadores por percentiles de posición."""
	# 1. Filtramos el DataFrame para conservar solo la posición indicada.
	position_df = df.loc[df["Primary_Pos"] == position].copy()

	# 2. Calculamos el percentil de cada métrica dentro de esa posición.
	#    rank(pct=True) produce valores entre 0 y 1, que convertimos a 0-100.
	percentile_df = position_df.copy()
	percentile_df[list(metrics)] = (
		position_df[list(metrics)].rank(pct=True) * 100
	)

	# 3. Buscamos los jugadores y extraemos sus valores percentiles.
	players = percentile_df.set_index("Player")
	metric_names = list(metrics)
	player1_values = players.loc[player1, metric_names].to_numpy(dtype=float)
	player2_values = players.loc[player2, metric_names].to_numpy(dtype=float)

	# 4. Cerramos los polígonos repitiendo el primer ángulo y valor.
	angles = np.linspace(0, 2 * np.pi, len(metric_names), endpoint=False)
	angles = np.concatenate([angles, angles[:1]])
	player1_values = np.concatenate([player1_values, player1_values[:1]])
	player2_values = np.concatenate([player2_values, player2_values[:1]])

	# 5. Creamos el gráfico polar y dibujamos ambos perfiles.
	fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
	ax.set_xticks(angles[:-1])
	ax.set_xticklabels(metric_names)
	ax.set_ylim(0, 100)
	ax.plot(angles, player1_values, linewidth=2, label=player1)
	ax.fill(angles, player1_values, alpha=0.15)
	ax.plot(angles, player2_values, linewidth=2, label=player2)
	ax.fill(angles, player2_values, alpha=0.15)
	ax.set_title(title, pad=20)
	ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

	# 6. Devolvemos la figura y el eje para permitir su reutilización.
	return fig, ax
