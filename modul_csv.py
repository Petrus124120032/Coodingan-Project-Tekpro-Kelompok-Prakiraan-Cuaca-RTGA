# modul_csv.py
import pandas as pd

def load_csv_auto(uploaded_file):
    encodings = ["utf-8", "latin1", "ISO-8859-1", "windows-1252"]
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)
            return df, enc
        except:
            continue
    return None, None


def normalisasi_dan_validasi(df):
    df.columns = [c.lower() for c in df.columns]

    required = ["timestamp", "temperature", "humidity", "pressure", "wind_speed"]
    if not all(col in df.columns for col in required):
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    return df
