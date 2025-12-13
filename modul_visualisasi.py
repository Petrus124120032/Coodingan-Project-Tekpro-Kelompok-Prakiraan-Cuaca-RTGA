# modul_visualisasi.py
import matplotlib.pyplot as plt

def plot_time_series(df, x, y, anomaly_col=None):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df[x], df[y], label=y)

    if anomaly_col:
        anomalies = df[df[anomaly_col]]
        ax.scatter(
            anomalies[x],
            anomalies[y],
            color="red",
            label="Anomali"
        )

    ax.set_xlabel("Waktu")
    ax.set_ylabel(y)
    ax.legend()

    return fig
