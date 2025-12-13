# modul_analisis.py
def analyze(df, col):
    stats = df[col].describe().to_dict()

    mean = stats["mean"]
    std = stats["std"]

    df[f"{col}_anomaly"] = (
        (df[col] > mean + 2 * std) |
        (df[col] < mean - 2 * std)
    )

    return stats, df
