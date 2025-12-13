# main.py
import streamlit as st
import pandas as pd

from modul_csv import load_csv_auto, normalisasi_dan_validasi
from modul_analisis import analyze
from modul_visualisasi import plot_time_series

# SETTING STREAMLIT
st.set_page_config(page_title="Dashboard Cuaca", layout="wide")
st.title("🌦 Dashboard Analisis Cuaca (Modular)")

# UPLOAD CSV
uploaded = st.file_uploader("📂 Upload file CSV", type=["csv"])

if uploaded:
    df, encoding = load_csv_auto(uploaded)

    if df is None:
        st.error("❌ Gagal membaca file CSV")
        st.stop()

    st.success(f"✔ File terbaca (encoding: {encoding})")

    df = normalisasi_dan_validasi(df)
    if df is None:
        st.error("❌ Kolom CSV tidak sesuai")
        st.stop()

    # ANALISIS DATA 
    stats_temp, df = analyze(df, "temperature")
    stats_hum, df = analyze(df, "humidity")
    stats_pres, df = analyze(df, "pressure")
    stats_wind, df = analyze(df, "wind_speed")

    # METRIK
    st.subheader("📊 Rata-rata Parameter")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Suhu (°C)", f"{stats_temp['mean']:.2f}")
    c2.metric("Kelembaban (%)", f"{stats_hum['mean']:.2f}")
    c3.metric("Tekanan (hPa)", f"{stats_pres['mean']:.2f}")
    c4.metric("Angin (m/s)", f"{stats_wind['mean']:.2f}")

    # FILTER TANGGAL DARI HASIL YANG TADI DI ANALISIS
    st.sidebar.header("🔎 Filter Tanggal")
    start = st.sidebar.date_input("Mulai", df["timestamp"].min())
    end = st.sidebar.date_input("Akhir", df["timestamp"].max())

    df_filtered = df[
        (df["timestamp"] >= pd.to_datetime(start)) &
        (df["timestamp"] <= pd.to_datetime(end))
    ]

    # GRAFIKNYA GESSS
    st.subheader("📈 Grafik Cuaca")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌡 Suhu", "💧 Kelembaban", "📉 Tekanan", "🌬 Angin"
    ])

    with tab1:
        fig = plot_time_series(
            df_filtered,
            "timestamp",
            "temperature",
            "temperature_anomaly"
        )
        st.pyplot(fig)

    with tab2:
        fig = plot_time_series(df_filtered, "timestamp", "humidity")
        st.pyplot(fig)

    with tab3:
        fig = plot_time_series(df_filtered, "timestamp", "pressure")
        st.pyplot(fig)

    with tab4:
        fig = plot_time_series(df_filtered, "timestamp", "wind_speed")
        st.pyplot(fig)

    # ANOMALI CUACA BUKAN ANOMALI KAMPUS
    st.subheader("🚨 Data Anomali")

    anomalies = df[
        df["temperature_anomaly"] |
        df["humidity_anomaly"] |
        df["pressure_anomaly"] |
        df["wind_speed_anomaly"]
    ]

    if anomalies.empty:
        st.success("Tidak ada anomali terdeteksi")
    else:
        st.warning("Ditemukan anomali cuaca")
        st.dataframe(anomalies)

else:
    st.info("Silakan upload file CSV untuk memulai")
