import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

try:
    paths = ["main_data.csv", "./main_data.csv", "../data/main_data.csv", "data/main_data.csv", "./data/main_data.csv"]

    for path in paths:
        if os.path.exists(path):
            all_df = pd.read_csv(path)
            st.success(f"Berhasil membaca file dari {path}, oke")
            break
    else:
        uploaded_file = st.file_uploader("Upload file CSV data sepeda", type="csv")
        if uploaded_file is not None:
            all_df = pd.read_csv(uploaded_file)
            st.success("File berhasil diupload!")
        else:
            st.error("File data tidak ditemukan. Silakan upload file CSV.")
            st.stop()

    all_df['dteday'] = pd.to_datetime(all_df['dteday'])

    st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_column_width=True)
    st.sidebar.header("Filter Data")

    start_date, end_date = st.sidebar.date_input(
        label='Pilih Rentang Waktu',
        min_value=all_df['dteday'].min().date(),
        max_value=all_df['dteday'].max().date(),
        value=[all_df['dteday'].min().date(), all_df['dteday'].max().date()]
    )

    hour_range = st.sidebar.slider(
        "Pilih Rentang Jam",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

    filtered_df = all_df[
        (all_df['dteday'] >= pd.to_datetime(start_date)) &
        (all_df['dteday'] <= pd.to_datetime(end_date)) &
        (all_df['hr'] >= hour_range[0]) &
        (all_df['hr'] <= hour_range[1])
    ]

    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.markdown("### Analisis Penggunaan Sepeda")

    total_rides = filtered_df['cnt_y'].sum()
    avg_temp = round(filtered_df['temp_y'].mean() * 41, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pengguna", value=f"{total_rides:,}")
    col2.metric("Rata-rata Suhu (°C)", value=f"{avg_temp}°C")

    busiest_hour = filtered_df.groupby('hr')['cnt_y'].mean().idxmax()
    col3.metric("Jam Tersibuk", value=f"{busiest_hour}:00")

    st.markdown("---")

    st.header("Pertanyaan Bisnis 1")
    st.markdown("#### Bagaimana perbedaan jumlah peminjam sepeda antara hari kerja dan akhir pekan?")

    filtered_df["day_type"] = filtered_df["workingday_y"].map({0: "Akhir Pekan/Libur", 1: "Hari Kerja"})

    day_type_trends = filtered_df.groupby("day_type")["cnt_y"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="day_type", y="cnt_y", data=day_type_trends, palette=["#FF7F50", "#4682B4"])
    ax.set_title("Rata-rata Peminjaman Sepeda: Hari Kerja vs Akhir Pekan", fontsize=14)
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Rata-rata Jumlah Peminjam")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.markdown("#### Komposisi pengguna casual vs registered berdasarkan tipe hari")

    day_type_users = filtered_df.groupby("day_type")[["casual_y", "registered_y"]].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(day_type_users["day_type"], day_type_users["casual_y"], color="#FF7F50", label="Casual")
    ax.bar(day_type_users["day_type"], day_type_users["registered_y"], color="#4682B4",
           bottom=day_type_users["casual_y"], label="Registered")

    ax.set_title("Komposisi Peminjam Sepeda: Hari Kerja vs Akhir Pekan", fontsize=14)
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Rata-rata Jumlah Peminjam")
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.markdown("#### Persentase pengguna casual vs registered berdasarkan tipe hari")

    total_by_type = filtered_df.groupby("day_type")[["casual_y", "registered_y"]].sum()
    percentage = total_by_type.div(total_by_type.sum(axis=1), axis=0) * 100
    percentage = percentage.reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    weekend_data = percentage.loc[percentage["day_type"] == "Akhir Pekan/Libur", ["casual_y", "registered_y"]].iloc[0]
    ax1.pie(weekend_data, labels=["Casual", "Registered"], autopct='%1.1f%%',
            colors=["#FF7F50", "#4682B4"], startangle=90)
    ax1.set_title("Komposisi Peminjam\nAkhir Pekan/Libur")

    workday_data = percentage.loc[percentage["day_type"] == "Hari Kerja", ["casual_y", "registered_y"]].iloc[0]
    ax2.pie(workday_data, labels=["Casual", "Registered"], autopct='%1.1f%%',
            colors=["#FF7F50", "#4682B4"], startangle=90)
    ax2.set_title("Komposisi Peminjam\nHari Kerja")

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    st.header("Pertanyaan Bisnis 2")
    st.markdown("#### Apakah ada pola musiman dalam penggunaan sepeda?")

    monthly_data = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt_y'].sum().reset_index()
    month_names = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    monthly_data['month_name'] = monthly_data['dteday'].map(month_names)

    month_order = list(range(1, 13))
    monthly_data['month_rank'] = monthly_data['dteday'].map({m: i for i, m in enumerate(month_order)})
    monthly_data = monthly_data.sort_values('month_rank')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month_name', y='cnt_y', data=monthly_data, marker='o', color='#72BCD4', linewidth=2)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Pengguna")
    ax.set_title("Pola Penggunaan Sepeda Berdasarkan Bulan", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

    season_names = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    filtered_df['season_name'] = filtered_df['season_y'].map(season_names)

    seasonal_data = filtered_df.groupby('season_name')['cnt_y'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season_name', y='cnt_y', data=seasonal_data, palette='viridis')
    ax.set_title("Penggunaan Sepeda Berdasarkan Musim", fontsize=14)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Pengguna")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.caption("🚀 Dashboard dibuat dengan Streamlit")

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Detail error:")
    st.exception(e)