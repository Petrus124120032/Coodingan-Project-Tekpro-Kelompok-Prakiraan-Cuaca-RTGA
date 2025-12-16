import streamlit as st
import pandas as pd

from modul_csv import load_csv_auto
from modul_analisis import analyze
from modul_forecast import forecast_ml
from modul_utils import rmse
from modul_visualisasi import (
    plot_historis,
    plot_forecast
)

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Dashboard Cuaca", layout="wide")

st.markdown("""
<style>
div.block-container {padding-top: 20px;}
.card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
}
.metric-value {font-size: 32px; font-weight: bold; color: #2c3e50;}
.metric-label {font-size: 14px; color: #555;}
</style>
""", unsafe_allow_html=True)

st.title("🌦 Dashboard Analisis & Forecast Cuaca")
st.write("Analisis statistik, deteksi anomali, forecast, evaluasi error, dan input data manual.")

# UPLOAD CSV
uploaded = st.file_uploader("📂 Upload file CSV", type=["csv"])

if uploaded:
    df, enc = load_csv_auto(uploaded)
    if df is None:
        st.error("CSV gagal dibaca")
        st.stop()

    df.columns = df.columns.str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if "df" not in st.session_state:
        st.session_state.df = df.copy()

    df = st.session_state.df.sort_values("timestamp")

    # INPUT DATA MANUAL
    st.subheader("➕ Input Data Cuaca Dadakan")

    with st.expander("Klik untuk input data manual"):
        c1, c2 = st.columns(2)
        with c1:
            tgl = st.date_input("Tanggal")
            temp = st.number_input("Temperature (°C)", step=0.1)
            hum = st.number_input("Humidity (%)", step=0.1)
        with c2:
            pres = st.number_input("Pressure (hPa)", step=0.1)
            wind = st.number_input("Wind Speed (m/s)", step=0.1)

        if st.button("➕ Tambahkan Data"):
            new_row = {
                "timestamp": pd.to_datetime(tgl),
                "temperature": temp,
                "humidity": hum,
                "pressure": pres,
                "wind_speed": wind
            }
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Data berhasil ditambahkan")
            st.rerun()

    # FILTER WAKTU
    st.sidebar.header("🔎 Filter Waktu")
    start = st.sidebar.date_input("Mulai", df['timestamp'].min())
    end = st.sidebar.date_input("Akhir", df['timestamp'].max())

    df_f = df[
        (df['timestamp'] >= pd.to_datetime(start)) &
        (df['timestamp'] <= pd.to_datetime(end))
    ]

    # ANALISIS
    stats_temp, df_f = analyze(df_f,'temperature')
    stats_hum, df_f = analyze(df_f,'humidity')
    stats_pres, df_f = analyze(df_f,'pressure')
    stats_wind, df_f = analyze(df_f,'wind_speed')

    st.subheader("📊 Ringkasan Statistik")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Suhu (°C)", f"{stats_temp['mean']:.2f}")
    c2.metric("Kelembaban (%)", f"{stats_hum['mean']:.2f}")
    c3.metric("Tekanan (hPa)", f"{stats_pres['mean']:.2f}")
    c4.metric("Angin (m/s)", f"{stats_wind['mean']:.2f}")

    # GRAFIK HISTORIS
    st.subheader("📈 Grafik Historis")
    cols = ['temperature','humidity','pressure','wind_speed']
    tabs = st.tabs(["Suhu","Kelembaban","Tekanan","Angin"])

    for tab, col in zip(tabs, cols):
        with tab:
            st.pyplot(plot_historis(df_f, col))

    # FORECAST
    st.subheader("🔮 Forecast (perkiraan)")
    days = st.slider("Hari Prediksi", 1, 30, 7)

    forecasts = {
        c: forecast_ml(df_f, c, days) for c in cols
    }

    tabs_f = st.tabs(["Suhu","Kelembaban","Tekanan","Angin"])
    for tab, col in zip(tabs_f, cols):
        with tab:
            f_d, f_y, _ = forecasts[col]
            st.pyplot(plot_forecast(df_f, col, f_d, f_y))

    # RMSE
    
    st.subheader("📐 Evaluasi Nilai Error (RMSE)")
    st.write({
        col.title(): rmse(df_f[col], forecasts[col][2])
        for col in cols
    })

    # TABEL & DOWNLOAD

    forecast_df = pd.DataFrame({
        'Tanggal': forecasts['temperature'][0],
        'Temp_Pred': forecasts['temperature'][1],
        'Hum_Pred': forecasts['humidity'][1],
        'Pres_Pred': forecasts['pressure'][1],
        'Wind_Pred': forecasts['wind_speed'][1]
    })

    st.subheader("📋 Tabel Perkiraan")
    st.dataframe(forecast_df)

    st.download_button(
        "⬇ Download Tabel Perkiraan CSV",
        forecast_df.to_csv(index=False).encode('utf-8'),
        "perkiraan_cuaca.csv"
    )

    # ANOMALI

    st.subheader("🚨 Anomali")

    anom_cols = [f"{c}_anomaly" for c in cols]
    anom = df_f[df_f[anom_cols].any(axis=1)]

    if anom.empty:
        st.success("Tidak ada anomali")
    else:
        st.warning("Anomali terdeteksi")
        st.dataframe(anom)
