# Dicoding Collection Dashboard ✨

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

## Ringkasan Proyek
Proyek ini menganalisis data penyewaan sepeda untuk memahami pola dan faktor yang mempengaruhi jumlah penyewaan. Fokus analisis adalah bagaimana kondisi cuaca mempengaruhi penggunaan sepeda dan mengidentifikasi pola musiman dalam perilaku penyewaan.

## Dataset
Analisis menggunakan dua dataset utama:
- `day.csv`: Data agregat harian penyewaan sepeda
- `hour.csv`: Data penyewaan sepeda per jam

## Pertanyaan Penelitian
1. Bagaimana kondisi cuaca (suhu, kelembaban, dan kecepatan angin) mempengaruhi jumlah penyewaan sepeda?
2. Apakah ada pola musiman dalam penggunaan sepeda, terutama pada bulan-bulan tertentu?

## Temuan Utama
- Suhu menunjukkan korelasi positif dengan penyewaan sepeda
- Kelembaban menunjukkan korelasi negatif dengan jumlah penyewaan
- Bulan-bulan musim panas memiliki jumlah penyewaan tertinggi
- Bulan-bulan musim dingin menunjukkan aktivitas penyewaan terendah