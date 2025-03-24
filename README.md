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

Kedua dataset telah digabungkan menggunakan operasi merge berdasarkan tanggal untuk membuat dataset komprehensif `main_data.csv`.

## Pertanyaan Bisnis
1. Bagaimana perbedaan jumlah peminjam sepeda antara hari kerja dan akhir pekan?
2. Apakah ada pola musiman dalam penggunaan sepeda, terutama pada bulan-bulan tertentu?

## Fitur Dashboard
- **Filter Data**: Memungkinkan pengguna menyaring data berdasarkan rentang waktu dan jam
- **Metrik Utama**: Menampilkan total pengguna, rata-rata suhu, dan jam tersibuk
- **Analisis Hari Kerja vs Akhir Pekan**: 
  - Perbandingan rata-rata pengguna antara hari kerja dan akhir pekan
  - Komposisi pengguna casual vs registered berdasarkan tipe hari
  - Distribusi persentase pengguna pada hari kerja dan akhir pekan
- **Analisis Pola Musiman**:
  - Tren total penggunaan sepeda berdasarkan bulan
  - Penggunaan sepeda berdasarkan musim (Musim Semi, Musim Panas, Musim Gugur, Musim Dingin)