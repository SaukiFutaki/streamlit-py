import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os





try:

    possible_paths = ["../data/day.csv", "data/day.csv", "./data/day.csv"]

    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            st.success(f"Berhasil membaca file dari  {path}, oke")
            break
    else:

        uploaded_file = st.file_uploader("Upload file CSV data sepeda", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File berhasil diupload!")
        else:
            st.error("File data tidak ditemukan. Silakan upload file CSV.")
            st.stop()


    df['dteday'] = pd.to_datetime(df['dteday'])


    st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_column_width=True)
    st.sidebar.header("Filter Data")

    start_date, end_date = st.sidebar.date_input(
        label='Pilih Rentang Waktu',
        min_value=df['dteday'].min().date(),
        max_value=df['dteday'].max().date(),
        value=[df['dteday'].min().date(), df['dteday'].max().date()]
    )

    filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]


    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.markdown("### Analisis Penggunaan Sepeda Berdasarkan Musim & Cuaca")


    total_rides = filtered_df['cnt'].sum()
    avg_temp = round(filtered_df['temp'].mean() * 41, 2)  # Konversi celcius

    col1, col2 = st.columns(2)
    col1.metric("Total Pengguna", value=f"{total_rides:,}")
    col2.metric("Rata-rata Suhu (°C)", value=f"{avg_temp}°C")


    st.subheader("📈 Tren Penggunaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_df['dteday'], y=filtered_df['cnt'], marker='o', color='#007BFF')
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_title("Tren Jumlah Pengguna Sepeda")
    st.pyplot(fig)


    st.subheader("🌦️ Pengaruh Musim & Cuaca")
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    sns.barplot(x=filtered_df['season'], y=filtered_df['cnt'], ax=ax[0], palette='coolwarm')
    ax[0].set_title("Pengaruh Musim")
    ax[0].set_xlabel("Musim")
    ax[0].set_ylabel("Jumlah Pengguna")

    sns.scatterplot(x=filtered_df['temp'] * 41, y=filtered_df['cnt'], alpha=0.7, color='#FF5733', ax=ax[1])
    ax[1].set_title("Suhu vs Pengguna")
    ax[1].set_xlabel("Suhu (°C)")
    ax[1].set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)


    st.subheader(" Pengguna Casual vs Registered")
    fig, ax = plt.subplots(figsize=(10, 5))
    casual_sum = filtered_df['casual'].sum()
    registered_sum = filtered_df['registered'].sum()
    labels = ['Casual', 'Registered']
    values = [casual_sum, registered_sum]
    colors = ['#FF6F61', '#6B5B95']
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
    ax.set_title("Distribusi Pengguna Sepeda")
    st.pyplot(fig)


    st.subheader("📊 Analisis Pertanyaan Bisnis")


    st.markdown("#### Bagaimana pengaruh cuaca terhadap jumlah peminjam sepeda?")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], palette='viridis')
    ax.set_xlabel("Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Rain/Snow, 4: Heavy Rain)")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_title("Pengaruh Cuaca Terhadap Jumlah Peminjam Sepeda")
    st.pyplot(fig)


    st.markdown("#### Apakah ada pola musiman dalam penggunaan sepeda?")

    monthly_data = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt'].mean().reset_index()
    monthly_data['month_name'] = monthly_data['dteday'].apply(lambda x: pd.to_datetime(f"2023-{x}-01").strftime('%B'))

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month_name', y='cnt', data=monthly_data, marker='o', color='#8B008B')
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Pengguna")
    ax.set_title("Pola Penggunaan Sepeda Berdasarkan Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.caption("🚀 Dashboard dibuat dengan Streamlit")

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Detail error lengkap:")
    st.exception(e)