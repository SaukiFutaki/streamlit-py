# Bike Sharing Dashboard 🚴‍♂️

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard.py
```


## Dataset
Analisis menggunakan gabungan dari dua dataset:
- `day.csv`: Data agregat harian penyewaan sepeda
- `hour.csv`: Data penyewaan sepeda per jam

Kedua dataset telah digabungkan menggunakan operasi merge berdasarkan tanggal untuk membuat dataset komprehensif `all_data.csv`.

## Pertanyaan Bisnis
1. Bagaimana kondisi cuaca (suhu, kelembaban, dan kecepatan angin) mempengaruhi jumlah peminjam sepeda?
2. Apakah ada pola musiman dalam penggunaan sepeda, terutama pada bulan-bulan tertentu?

## Fitur Dashboard
- **Filter Data**: Memungkinkan pengguna menyaring data berdasarkan rentang waktu dan jam
- **Metrik Utama**: Menampilkan total pengguna, rata-rata suhu, dan jam tersibuk
- **Tren Penggunaan**: Visualisasi tren penggunaan sepeda harian dan per jam
- **Analisis Musim & Cuaca**: Menampilkan pengaruh musim dan hubungan antara suhu dengan jumlah pengguna
- **Profil Pengguna**: Perbandingan pengguna casual vs registered
- **Heatmap Waktu**: Visualisasi pola penggunaan berdasarkan hari dan jam

