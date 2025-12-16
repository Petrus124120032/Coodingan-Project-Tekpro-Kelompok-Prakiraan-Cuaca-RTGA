import pandas as pd

def load_csv_auto(uploaded_file):
    for enc in ["utf-8", "latin1", "ISO-8859-1", "windows-1252"]:
        try:
            return pd.read_csv(uploaded_file, encoding=enc), enc
        except:
            pass
    return None, None
