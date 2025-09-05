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

Reviewer dapat menjalankan prototype sistem machine learning ini dengan langkah-langkah berikut:  

### 🔹 1. Setup Environment
1. Clone repository:
   ```bash
   git clone https://github.com/Nauviii/Student-Dropout-Prediction-System---APP.git
   cd Student-Dropout-Prediction-System---APP
   ```
2. Membuat dan Mengaktifkan Virtual Environment

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

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Menggunakan Model Secara Langsung:
   ```bash
   import joblib
   import pandas as pd
   
   # Load model & encoder
   model = joblib.load("model/model.joblib")
   encoders = joblib.load("model/encoders.joblib")
   
   # Contoh input (isi sesuai fitur dataset)
   data = pd.DataFrame([{
       "Application Order": 1,
       "Previous Qualification Grade": 100,
       "Admission Grade": 80,
       "Units Enrolled (Sem 1)": 5,
       "Units Evaluations (Sem 1)": 1,
       "Units Approved (Sem 1)": 4,
       "Units Grade (Sem 1)": 16,
       "Gender": "Male",
       "Scholarship_holder": "Yes",
       "Age": 21,
       "Debtor": "No",
       "Tuition_fees_up_to_date": "Yes",
       "Course": "Informatics_Engineering"
   }])
   
   # Transformasi kategorikal
   for col, encoder in encoders.items():
       data[col] = encoder.transform(data[col])
   
   # Prediksi
   prediction = model.predict(data)
   print("Hasil Prediksi:", prediction)
   ```
---

## Conclusion

Proyek ini berhasil mengimplementasikan sistem machine learning untuk memprediksi kemungkinan mahasiswa melakukan *dropout* di Jaya Jaya Institut.  
Melalui tahapan **data understanding, exploratory data analysis, preprocessing, model building, evaluasi, dan deployment**, sistem ini mampu memberikan solusi yang dapat langsung dimanfaatkan oleh pihak institusi.

Beberapa poin penting yang dapat disimpulkan:
1. **Model Machine Learning (XGBoost)** memberikan performa yang baik dalam mengklasifikasikan status mahasiswa dengan menggunakan 14 fitur utama.  
2. **Faktor-faktor penting** yang mempengaruhi prediksi dropout di antaranya adalah nilai akademik, status keuangan (pembayaran biaya kuliah), serta faktor beasiswa.  
3. **Dashboard interaktif berbasis Streamlit** mempermudah stakeholder untuk:
   - Melakukan prediksi dropout mahasiswa secara cepat dan mudah,  
   - Menilai tingkat risiko berdasarkan confidence score,  
   - Mendapatkan rekomendasi tindak lanjut,  
   - Mengeksplorasi data secara visual untuk mendukung pengambilan keputusan.  
4. Sistem ini dapat menjadi **alat bantu strategis** bagi manajemen dalam melakukan *early intervention* terhadap mahasiswa yang berpotensi dropout.

### Future Work
Untuk pengembangan ke depan, sistem ini masih dapat ditingkatkan, antara lain:
- Menambahkan lebih banyak data historis untuk meningkatkan akurasi model,  
- Mengintegrasikan data real-time dari sistem informasi akademik,  
- Mengembangkan sistem rekomendasi yang lebih personalisasi untuk mahasiswa berisiko tinggi,  
- Mengimplementasikan MLOps agar model dapat terus diperbarui secara otomatis dengan data terbaru.  

Dengan adanya sistem ini, diharapkan tingkat dropout mahasiswa di Jaya Jaya Institut dapat ditekan, serta memberikan pengalaman belajar yang lebih baik bagi mahasiswa.

---

### Rekomendasi Action Items

#### 1. Jika Mahasiswa Terindikasi Akan Melakukan Dropout, Maka Direkomendasikan untuk:

- **Berikan bimbingan akademik intensif**  
  Mahasiswa yang memiliki performa akademik rendah perlu mendapatkan sesi bimbingan tambahan, baik berupa tutoring, kelas remedial, atau mentoring dari dosen agar kesulitan belajar dapat segera diatasi.

- **Monitor progress secara berkala**  
  Pihak kampus perlu melakukan monitoring akademik dengan jadwal rutin (misalnya setiap akhir semester) untuk memastikan adanya perbaikan dari mahasiswa yang berisiko dropout.

- **Pertimbangkan program remedial**  
  Jika mahasiswa gagal pada beberapa mata kuliah, program remedial dapat membantu mereka memperbaiki nilai tanpa harus menunda kelulusan terlalu lama.

- **Konseling untuk mengatasi masalah personal/finansial**  
  Banyak kasus dropout tidak hanya disebabkan faktor akademik, tetapi juga permasalahan pribadi dan finansial. Konseling psikologis dan bantuan finansial (misalnya potongan biaya atau beasiswa darurat) bisa menjadi solusi efektif.

- **Libatkan academic advisor dan orang tua**  
  Advisor (dosen wali) bersama orang tua dapat dilibatkan dalam diskusi tindak lanjut sehingga mahasiswa merasa didukung baik dari sisi akademik maupun lingkungan keluarga.

#### 2. Jika Mahasiswa Tidak Terindikasi Akan Melakukan Dropout, Maka Direkomendasikan untuk:

- **Pertahankan kualitas akademik yang baik**  
  Mahasiswa tetap perlu diarahkan agar menjaga konsistensi performa akademiknya melalui kebiasaan belajar yang teratur dan disiplin.

- **Dorong partisipasi dalam kegiatan kampus**  
  Mahasiswa dapat diperkuat motivasinya dengan dilibatkan dalam kegiatan organisasi, penelitian, maupun lomba, sehingga mereka lebih terikat secara emosional dengan kampus.

- **Berikan apresiasi dan penghargaan**  
  Pemberian penghargaan (misalnya sertifikat, beasiswa prestasi, atau publikasi pencapaian) dapat meningkatkan motivasi dan menjadi teladan bagi mahasiswa lain.

- **Kembangkan soft skills dan keterampilan tambahan**  
  Walaupun tidak berisiko dropout, mahasiswa perlu difasilitasi untuk meningkatkan keterampilan non-akademik seperti kepemimpinan, komunikasi, dan pemecahan masalah, yang akan bermanfaat di dunia kerja.

- **Siapkan jalur percepatan akademik**  
  Bagi mahasiswa berprestasi, dapat diberikan opsi percepatan kelulusan, kesempatan mengambil mata kuliah lintas jurusan, atau program magang industri untuk memperkuat kompetensi mereka.

---

