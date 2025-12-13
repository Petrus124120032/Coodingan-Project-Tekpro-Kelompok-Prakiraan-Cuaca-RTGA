# generate_cuaca_lampung.py
import pandas as pd
import random
from datetime import datetime, timedelta

def buat_prakiraan_harian_lampung_selatan_sampai_akhir_2025():
    today = datetime.now().date()
    end_date = datetime(2025, 12, 31).date()

    if today > end_date:
        raise Exception("Tanggal hari ini sudah lewat tahun 2025")

    delta = end_date - today

    data = []
    kondisi = [
        "Cerah", "Cerah Berawan", "Berawan",
        "Hujan Ringan", "Hujan Sedang",
        "Hujan Lebat", "Badai Petir", "Kabut"
    ]

    for i in range(delta.days + 1):
        tanggal = today + timedelta(days=i)

        temperature = round(random.uniform(24, 33), 1)
        humidity = random.randint(80, 96)
        pressure = round(random.uniform(1005, 1015), 1)
        wind_speed = round(random.uniform(3, 18), 1)

        data.append([
            tanggal,
            temperature,
            humidity,
            pressure,
            wind_speed,
            random.choice(kondisi)
        ])

    df = pd.DataFrame(data, columns=[
        "timestamp",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "condition"
    ])

    return df


if __name__ == "__main__":
    df = buat_prakiraan_harian_lampung_selatan_sampai_akhir_2025()
    df.to_csv("prakiraan_cuaca_lampung_2025.csv", index=False)
    print("File CSV berhasil dibuat")
