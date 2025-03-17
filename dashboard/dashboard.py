import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

try:

    paths = ["main_data.csv","./main_data.csv","../data/main_data.csv", "data/main_data.csv", "./data/main_data.csv"]

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
    st.markdown("### Analisis Penggunaan Sepeda Berdasarkan Musim, Cuaca & Waktu")


    total_rides = filtered_df['cnt_y'].sum()
    avg_temp = round(filtered_df['temp_y'].mean() * 41, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pengguna", value=f"{total_rides:,}")
    col2.metric("Rata-rata Suhu (°C)", value=f"{avg_temp}°C")


    busiest_hour = filtered_df.groupby('hr')['cnt_y'].mean().idxmax()
    col3.metric("Jam Tersibuk", value=f"{busiest_hour}:00")


    st.subheader("📈 Tren Penggunaan Sepeda")

    tab1, tab2 = st.tabs(["Tren Harian", "Tren Per Jam"])

    with tab1:

        daily_data = filtered_df.groupby('dteday')['cnt_y'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=daily_data['dteday'], y=daily_data['cnt_y'], marker='o', color='#007BFF')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Pengguna")
        ax.set_title("Tren Jumlah Pengguna Sepeda Harian")
        st.pyplot(fig)

    with tab2:

        hourly_data = filtered_df.groupby('hr')['cnt_y'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=hourly_data['hr'], y=hourly_data['cnt_y'], marker='o', color='#FF5733')
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Pengguna")
        ax.set_title("Rata-rata Penggunaan Sepeda per Jam")
        ax.set_xticks(range(0, 24))
        st.pyplot(fig)


    st.subheader("🌦️ Pengaruh Musim & Cuaca")
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    season_names = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    filtered_df['season_name'] = filtered_df['season_y'].map(season_names)

    sns.barplot(x='season_name', y='cnt_y', data=filtered_df, ax=ax[0], palette='coolwarm')
    ax[0].set_title("Pengaruh Musim")
    ax[0].set_xlabel("Musim")
    ax[0].set_ylabel("Jumlah Pengguna")
    ax[0].tick_params(axis='x', rotation=45)

    sns.scatterplot(x=filtered_df['temp_y'] * 41, y=filtered_df['cnt_y'], alpha=0.7, color='#FF5733', ax=ax[1])
    ax[1].set_title("Suhu vs Pengguna")
    ax[1].set_xlabel("Suhu (°C)")
    ax[1].set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)


    st.subheader("👥 Pengguna Casual vs Registered")
    fig, ax = plt.subplots(figsize=(10, 5))
    casual_sum = filtered_df['casual_y'].sum()
    registered_sum = filtered_df['registered_y'].sum()
    labels = ['Casual', 'Registered']
    values = [casual_sum, registered_sum]
    colors = ['#FF6F61', '#6B5B95']
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
    ax.set_title("Distribusi Pengguna Sepeda")
    st.pyplot(fig)


    st.subheader("📊 Analisis Pertanyaan Bisnis")


    st.markdown("#### Bagaimana pengaruh cuaca terhadap jumlah peminjam sepeda?")
    weather_map = {1: "Clear", 2: "Mist/Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain"}
    filtered_df['weather_desc'] = filtered_df['weathersit_y'].map(weather_map)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='weather_desc', y='cnt_y', data=filtered_df, palette='viridis')
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_title("Pengaruh Cuaca Terhadap Jumlah Peminjam Sepeda")
    st.pyplot(fig)


    st.markdown("#### Apakah ada pola musiman dalam penggunaan sepeda?")

    monthly_data = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt_y'].mean().reset_index()
    month_names = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    monthly_data['month_name'] = monthly_data['dteday'].map(month_names)


    month_order = list(range(1, 13))
    monthly_data['month_rank'] = monthly_data['dteday'].map({m: i for i, m in enumerate(month_order)})
    monthly_data = monthly_data.sort_values('month_rank')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month_name', y='cnt_y', data=monthly_data, marker='o', color='#8B008B')
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Pengguna")
    ax.set_title("Pola Penggunaan Sepeda Berdasarkan Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)


    st.subheader("🕒 Analisis Berdasarkan Hari dan Jam")


    day_names = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
    filtered_df['day_name'] = filtered_df['weekday_y'].map(day_names)


    heatmap_data = filtered_df.pivot_table(
        index='hr',
        columns='day_name',
        values='cnt_y',
        aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False, fmt=".0f", ax=ax)
    ax.set_title("Pola Penggunaan Sepeda Berdasarkan Hari dan Jam")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jam")
    st.pyplot(fig)

    st.caption("🚀 Dashboard dibuat dengan Streamlit")

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Detail error:")
    st.exception(e)