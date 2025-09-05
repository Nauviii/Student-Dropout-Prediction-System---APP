# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

---

### Permasalahan Bisnis
- Mengidentifikasi faktor-faktor utama penyebab tingginya nilai dropout yang terjadi.
- Mengembangkan model machine learning untuk memprediksi kemungkinan siswa melakukan dropout
- Memberikan insight berbasis data untuk membantu manajemen menggambil keputusan
- Membuat business dashboard interaktif untuk memonitor siswa secara real-time, sehingga dapat mendukung pengambilan keputusan berbasis data.

---

### Cakupan Proyek
1. **Data Understanding & Statistic Analysis**
   - Memahami data secara keseluruhan, mencari anomaly, dan melihat pola yang terjadi pada data
2. **Exploratory Data Analysis (EDA)**  
   - Visualisasi dan analisis statistik untuk menemukan pola dan insight.
3. **Data Preprocessing & Feature Engineering**  
   - Membersihkan data, menangani missing values, dan encoding fitur kategorikal.  
4. **Model Machine Learning**  
   - Membangun model klasifikasi untuk memprediksi kemungkinan siswa dropout menggunakan base tree model.  
5. **Evaluasi Model**  
   - Menggunakan metrik evaluasi seperti Confusion Matrix, Classification Report, dan ROC-AUC.  
6. **Dashboard Interaktif**  
   - Membuat aplikasi interaktif berbasis **Streamlit** untuk memudahkan manajamen menggunakan hasil model machine learning.  

---

### Persiapan

Sumber data: (https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)

### Setup environment:

Pastikan Anda mengikuti langkah-langkah berikut agar proyek dapat dijalankan dengan baik:

#### 1. Clone Repository

```bash
git clone https://github.com/Nauviii/Student-Dropout-Prediction-System---APP.git
cd Student-Dropout-Prediction-System---APP
```

#### 2. Membuat dan Mengaktifkan Virtual Environment

Agar lingkungan pengembangan terisolasi dan stabil, buat virtual environment (venv):

* **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

* **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Menjalankan Dashboard

```bash
streamlit run app.py
```
---
## Business Dashboard

🔗 Akses Dashboard: (https://student-dropout-prediction-system.streamlit.app/)  

Dashboard ini adalah aplikasi interaktif berbasis Streamlit yang membantu stakeholder memprediksi kemungkinan mahasiswa melakukan dropout. Dashboard mencakup:
1. **Prediksi Dropout**: Memprediksi kemungkinan mahasiswa dropout berdasarkan 14 parameter input
2. **Risk Assessment**: Menilai tingkat risiko dropout dengan confidence score
3. **Recommendation System**: Memberikan saran spesifik berdasarkan hasil prediksi
4. **Data Visualization**: Menampilkan probabilitas dalam bentuk chart interaktif
5. **Educational Tool**: Membantu institusi pendidikan dalam early intervention

---

## Menjalankan Sistem Machine Learning
Jelaskan cara menjalankan protoype sistem machine learning yang telah dibuat. Selain itu, sertakan juga link untuk mengakses prototype tersebut.

```

```

## Conclusion
Jelaskan konklusi dari proyek yang dikerjakan.

### Rekomendasi Action Items
Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- action item 1
- action item 2
