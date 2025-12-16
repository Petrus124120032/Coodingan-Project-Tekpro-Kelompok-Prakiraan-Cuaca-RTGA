import matplotlib.pyplot as plt

def plot_historis(df, col):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df['timestamp'], df[col], marker='o')
    ax.set_ylabel(col)
    return fig

def plot_forecast(df, col, f_d, f_y):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df['timestamp'], df[col], label="Historis")
    ax.plot(f_d, f_y, '--', label="Forecast")
    ax.legend()
    return fig
