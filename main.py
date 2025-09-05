import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk load gambar lokal dan konversikan ke base64
def get_base64_of_local_image(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        return ""


# Try to load background image
encoded_image = get_base64_of_local_image("background_1.jpg")

# Enhanced CSS dengan notifikasi
background_style = f'background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("data:image/jpg;base64,{encoded_image}");' if encoded_image else 'background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'

st.markdown(f"""
    <style>
    /* Background styling */
    .stApp {{
        {background_style}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: black;
    }}
    
    /* Notification styling */
    .welcome-notification {{
        position: fixed;
        top: 20px;
        right: 20px;
        width: 400px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: slideInRight 0.5s ease-out;
        border: 2px solid #90CAF9;
    }}
    
    @keyframes slideInRight {{
        from {{
            transform: translateX(100%);
            opacity: 0;
        }}
        to {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}
    
    @keyframes slideOutRight {{
        from {{
            transform: translateX(0);
            opacity: 1;
        }}
        to {{
            transform: translateX(100%);
            opacity: 0;
        }}
    }}
    
    .notification-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.3);
    }}
    
    .notification-title {{
        font-size: 1.2em;
        font-weight: bold;
        margin: 0;
    }}
    
    .notification-close {{
        background: none;
        border: none;
        color: white;
        font-size: 1.5em;
        cursor: pointer;
        padding: 0;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background-color 0.3s;
    }}
    
    .notification-close:hover {{
        background-color: rgba(255,255,255,0.2);
    }}
    
    .notification-content {{
        font-size: 0.9em;
        line-height: 1.4;
    }}
    
    .notification-content ul {{
        margin: 10px 0;
        padding-left: 20px;
    }}
    
    .notification-content li {{
        margin: 5px 0;
    }}
    
    .notification-fade-out {{
        animation: slideOutRight 0.5s ease-in forwards;
    }}
    
    /* Progress bar for auto-dismiss */
    .notification-progress {{
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: rgba(255,255,255,0.3);
        border-radius: 0 0 15px 15px;
        overflow: hidden;
    }}
    
    .notification-progress-bar {{
        height: 100%;
        background: white;
        width: 0%;
        animation: progress 15s linear;
    }}
    
    @keyframes progress {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
    }}
    
    /* Styling untuk judul utama */
    .centered-title {{
        text-align: center;
        color: #1976D2;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 2px solid #E3F2FD;
    }}
    
    /* Container untuk setiap section dengan border yang jelas */
    .section-box {{
        background: white;
        border: 2px solid #90CAF9;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .section-box:hover {{
        border-color: #1976D2;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    
    /* Header untuk setiap section */
    .section-header {{
        background: #E3F2FD;
        margin: -20px -20px 15px -20px;
        padding: 15px 20px;
        border-radius: 8px 8px 0 0;
        font-size: 1.3em;
        font-weight: bold;
        color: #1976D2;
        border-bottom: 2px solid #90CAF9;
    }}
    
    /* Data items styling */
    .data-item {{
        background: #F8F9FA;
        margin: 8px 0;
        padding: 12px;
        border-left: 4px solid #1976D2;
        border-radius: 5px;
        font-size: 1em;
    }}
    
    .data-item:hover {{
        background: #E3F2FD;
    }}
    
    /* Enhanced metric styling */
    div[data-testid="stMetric"] {{
        background-color: white !important;
        border: 2px solid #90CAF9 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }}

    div[data-testid="stMetric"]:hover {{
        border-color: #1976D2 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }}

    [data-testid="stMetricValue"], 
    [data-testid="stMetricLabel"] {{
        color: black !important;
    }}
    
    /* Container sidebar utama */
    section[data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 3px solid #1976D2 !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background-color: #FFFFFF !important;
        padding-top: 20px !important;
    }}
    
    /* Header sidebar */
    section[data-testid="stSidebar"] h1 {{
        color: #1976D2 !important;
        font-weight: bold !important;
        font-size: 1.5em !important;
        border-bottom: 2px solid #90CAF9 !important;
        padding: 15px !important;
        margin-bottom: 20px !important;
        background: #E3F2FD !important;
        border-radius: 8px !important;
        text-align: center !important;
    }}
    
    section[data-testid="stSidebar"] h2 {{
        color: #1976D2 !important;
        font-weight: 600 !important;
        font-size: 1.3em !important;
        margin: 20px 0 10px 0 !important;
        padding: 10px !important;
        background: #F5F5F5 !important;
        border-radius: 5px !important;
        border-left: 4px solid #1976D2 !important;
    }}
    
    section[data-testid="stSidebar"] h3 {{
        color: #1976D2 !important;
        font-weight: 600 !important;
        font-size: 1.2em !important;
        margin: 15px 0 8px 0 !important;
    }}
    
    /* Teks biasa di sidebar */
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown div {{
        color: #333333 !important;
        font-weight: 500 !important;
    }}
    
    
    /* Label untuk semua form controls */
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stCheckbox label {{
        color: #1976D2 !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
        margin-bottom: 8px !important;
        display: block !important;
    }}
    
    /* Dropdown/Selectbox styling yang diperbaiki */
    section[data-testid="stSidebar"] .stSelectbox > div > div {{
        background-color: #FFFFFF !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {{
        border-color: #1976D2 !important;
    }}
    
    /* Teks dalam dropdown button */
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="button"] {{
        background-color: #FFFFFF !important;
        color: #333333 !important;
        font-weight: 500 !important;
        padding: 10px 12px !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="button"] > div {{
        color: #333333 !important;
        font-size: 1em !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="button"] span {{
        color: #333333 !important;
    }}
    
    /* STYLING SUPER AGRESIF UNTUK DROPDOWN OPTIONS */
    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stSelectbox span,
    section[data-testid="stSidebar"] .stSelectbox li {{
        color: #333333 !important;
    }}
    
    /* Targeting semua possible dropdown elements */
    section[data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: #333333 !important;
    }}
    
    /* Override untuk memastikan visibility */
    section[data-testid="stSidebar"] .stSelectbox * {{
        visibility: visible !important;
        opacity: 1 !important;
    }}
    
    /* Specific untuk dropdown options yang terbuka */
    [data-baseweb="popover"] div[role="listbox"] {{
        background-color: #FFFFFF !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    
    [data-baseweb="popover"] div[role="listbox"] * {{
        color: #333333 !important;
        background-color: transparent !important;
    }}
    
    [data-baseweb="popover"] div[role="listbox"] > div {{
        padding: 8px 12px !important;
        font-weight: 500 !important;
    }}
    
    [data-baseweb="popover"] div[role="listbox"] > div:hover {{
        background-color: #E3F2FD !important;
        color: #1976D2 !important;
    }}
    
    /* Dropdown list/options */
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="listbox"] {{
        background-color: #FFFFFF !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="listbox"] > div,
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="option"] {{
        color: #333333 !important;
        background-color: #FFFFFF !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] div[role="option"]:hover {{
        background-color: #E3F2FD !important;
        color: #1976D2 !important;
    }}
    
    /* Placeholder text */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="button"] div[class*="placeholder"] {{
        color: #666666 !important;
        font-style: italic !important;
    }}
    
    /* Radio button styling */
    section[data-testid="stSidebar"] .stRadio > div {{
        background-color: #F8F9FA !important;
        padding: 10px !important;
        border-radius: 8px !important;
        border: 1px solid #E0E0E0 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio > div > div {{
        color: #333333 !important;
        font-weight: 500 !important;
    }}
    
    /* Slider styling */
    section[data-testid="stSidebar"] .stSlider > div > div {{
        color: #333333 !important;
        font-weight: 500 !important;
    }}
    
    /* Number input styling */
    section[data-testid="stSidebar"] .stNumberInput input {{
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }}
    
    section[data-testid="stSidebar"] .stNumberInput input:focus {{
        border-color: #1976D2 !important;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
    }}
    
    /* Text input styling */
    section[data-testid="stSidebar"] .stTextInput input {{
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }}
    
    section[data-testid="stSidebar"] .stTextInput input:focus {{
        border-color: #1976D2 !important;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
    }}
    
    /* Checkbox styling */
    section[data-testid="stSidebar"] .stCheckbox > div > div {{
        color: #333333 !important;
        font-weight: 500 !important;
    }}
    
    /* Multi-select styling */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {{
        background-color: #FFFFFF !important;
        border: 2px solid #90CAF9 !important;
        border-radius: 8px !important;
    }}
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div:hover {{
        border-color: #1976D2 !important;
    }}
    
    /* Button styling di sidebar */
    section[data-testid="stSidebar"] .stButton > button {{
        background-color: #1976D2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 1em !important;
        width: 100% !important;
        margin: 10px 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background-color: #1565C0 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }}

    .stButton > button {{
        background-color: #1976D2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 1em;
    }}
    
    .stButton > button:hover {{
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)


# Inisialisasi session state
if "notification_dismissed" not in st.session_state:
    st.session_state.notification_dismissed = False
if "countdown" not in st.session_state:
    st.session_state.countdown = 10

def show_welcome_notification_simple():
    if not st.session_state.notification_dismissed:
        notif_placeholder = st.empty()
        
        # Tampilkan notifikasi dengan countdown
        for remaining in range(10, 0, -1):
            notif_placeholder.markdown(
                f"""
                <div style="
                    position: fixed;
                    top: 80px;
                    right: 40px;
                    z-index: 9999;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    max-width: 350px;
                ">
                    <h3 style="margin-top:0; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                        🎓 Selamat Datang!
                        <button style="border:none; background:none; font-size:16px; cursor:pointer;" 
                                onclick="this.parentElement.parentElement.style.display='none'">✖</button>
                    </h3>
                    <p><strong>Student Dropout Prediction System</strong></p>
                    <ul style="margin-top:0; margin-bottom:10px;">
                        <li>Isi semua data di sidebar</li>
                        <li>Klik tombol 'Prediksi Dropout'</li>
                        <li>Lihat hasil dan rekomendasi</li>
                    </ul>
                    <p style="margin-bottom:0; font-size:12px; color:#666; text-align:center;">
                        ⏱️ Notifikasi akan hilang dalam <span style="font-weight:bold; color:#ff6b6b;">{remaining}</span> detik
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(1)
        
        # Hapus notifikasi setelah 10 detik
        notif_placeholder.empty()
        st.session_state.notification_dismissed = True

# Halaman utama
st.markdown("<h1 style='text-align:center;'>Student Dropout Prediction System 🎓</h1>", unsafe_allow_html=True)

show_welcome_notification_simple()

# Tombol untuk reset notifikasi (untuk testing) - di sebelah kanan
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("Reset Notification"):
        st.session_state.notification_dismissed = False
        st.session_state.countdown = 10
        if "start_time" in st.session_state:
            del st.session_state.start_time
        st.rerun()


# Fungsi untuk membuat section dengan border
def create_section_box(title, content_html):
    st.markdown(f"""
        <div class="section-box">
            <div class="section-header">{title}</div>
            {content_html}
        </div>
    """, unsafe_allow_html=True)

# Contoh penggunaan untuk data Anda:
col1, col2 = st.columns(2)

with col1:
    # Data Akademik
    academic_content = """
        <div class="data-item">📋 <strong>Application Order:</strong> 1</div>
        <div class="data-item">🎯 <strong>Previous Qualification Grade:</strong> 120.0</div>
        <div class="data-item">📖 <strong>Admission Grade:</strong> 120.0</div>
    """
    create_section_box("📊 Ringkasan Akademik", academic_content)
    
    # Data Semester 1
    semester_content = """
        <div class="data-item">📑 <strong>Units Enrolled:</strong> 6</div>
        <div class="data-item">📝 <strong>Units Evaluations:</strong> 6</div>
        <div class="data-item">✅ <strong>Units Approved:</strong> 6</div> 
    """
    create_section_box("📚 Data Semester 1", semester_content)

with col2:
    # Data Personal
    personal_content = """
        <div class="data-item">👨 <strong>Gender:</strong> Male</div>
        <div class="data-item">🎨 <strong>Course:</strong> Animation and Multimedia Design</div>
        <div class="data-item">👤 <strong>Age:</strong> 20</div>
    """
    create_section_box("👤 Data Personal", personal_content)
    
    # Status Keuangan
    financial_content = """
        <div class="data-item">💳 <strong>Tuition Fees Up to Date:</strong> No</div>
        <div class="data-item">💰 <strong>Debtor:</strong> No</div>
        <div class="data-item">🏠 <strong>Displaced:</strong> No</div>
    """
    create_section_box("💰 Status Keuangan", financial_content)

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model = joblib.load('model.joblib')
        return model
    except FileNotFoundError:
        st.error("Model file 'model.joblib' tidak ditemukan. Pastikan file model ada di direktori yang sama.")
        return None
    except Exception as e:
        st.error(f"Error memuat model: {str(e)}")
        return None

@st.cache_resource
def load_encoders():
    """Load the trained encoders"""
    try:
        encoders = joblib.load('encoders.joblib')
        return encoders
    except FileNotFoundError:
        st.error("❌ File 'encoders.joblib' tidak ditemukan. Pastikan file encoder ada di direktori yang sama.")
        st.info("💡 Gunakan fungsi encoding() untuk membuat encoders.joblib dari data training Anda.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading encoders: {e}")
        return None

def create_default_encoders():
    """Create default label encoders - only used as fallback"""
    st.warning("🚧 Menggunakan encoder default. Hasil prediksi mungkin tidak akurat!")
    st.info("📝 Untuk hasil optimal, gunakan encoders.joblib dari data training.")
    
    encoders = {}
    
    # Default mappings - sebaiknya tidak digunakan untuk produksi
    categorical_mappings = {
        'Scholarship_holder': ['No', 'Yes'],
        'Gender': ['Male', 'Female'],
        'Tuition_fees_up_to_date': ['No', 'Yes'],
        'Debtor': ['No', 'Yes'],
        'Displaced': ['No', 'Yes'],
        'Course': ['Animation and Multimedia Design',
                    'Tourism',
                    'Communication Design',
                    'Journalism and Communication',
                    'Social Service (evening attendance)',
                    'Management (evening attendance)',
                    'Nursing',
                    'Social Service',
                    'Advertising and Marketing Management',
                    'Basic Education',
                    'Veterinary Nursing',
                    'Equinculture',
                    'Oral Hygiene',
                    'Management',
                    'Agronomy',
                    'Biofuel Production Technologies',
                    'Informatics Engineering'],
        'Status': ['Graduate', 'Dropout', 'Enrolled']
    }
    
    for feature, categories in categorical_mappings.items():
        le = LabelEncoder()
        le.fit(categories)
        encoders[feature] = le
    
    return encoders

def get_user_input():
    """Create input widgets for user data"""
    st.sidebar.header("📊 Input Data Mahasiswa")
    
    # Numerical features
    st.sidebar.subheader("Data Numerik")
    application_order = st.sidebar.number_input("Application Order", min_value=0, max_value=10, value=1, help="Urutan aplikasi pendaftaran")
    prev_qual_grade = st.sidebar.slider("Previous Qualification Grade", 0.0, 200.0, 120.0, 0.1, help="Nilai kualifikasi sebelumnya")
    admission_grade = st.sidebar.slider("Admission Grade", 0.0, 200.0, 120.0, 0.1, help="Nilai penerimaan")
    
    # Semester 1 units
    st.sidebar.subheader("Data Semester 1")
    units_enrolled = st.sidebar.number_input("Units Enrolled (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang diambil")
    units_evaluations = st.sidebar.number_input("Units Evaluations (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang dievaluasi")
    units_approved = st.sidebar.number_input("Units Approved (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang lulus")
    units_grade = st.sidebar.slider("Units Grade (Sem 1)", 0.0, 20.0, 12.0, 0.1, help="Rata-rata nilai semester 1")
    
    age = st.sidebar.number_input("Age", min_value=17, max_value=70, value=20, help="Usia mahasiswa")
    
    # Validation for semester units
    if units_evaluations > units_enrolled:
        st.sidebar.warning("⚠️ Units Evaluations tidak boleh lebih besar dari Units Enrolled")
    
    if units_approved > units_evaluations:
        st.sidebar.warning("⚠️ Units Approved tidak boleh lebih besar dari Units Evaluations")
    
    # Categorical features
    st.sidebar.subheader("Data Kategorikal")
    scholarship = st.sidebar.selectbox("Scholarship Holder", ['No', 'Yes'], help="Apakah penerima beasiswa?")
    gender = st.sidebar.selectbox("Gender", ['Male', 'Female'], help="Jenis kelamin")
    tuition_updated = st.sidebar.selectbox("Tuition Fees Up to Date", ['No', 'Yes'], help="Apakah biaya kuliah up to date?")
    debtor = st.sidebar.selectbox("Debtor", ['No', 'Yes'], help="Apakah memiliki hutang?")
    displaced = st.sidebar.selectbox("Displaced", ['No', 'Yes'], help="Apakah mengalami perpindahan tempat tinggal?")
    
    course = st.sidebar.selectbox("Course", [
        'Animation and Multimedia Design',
        'Tourism',
        'Communication Design',
        'Journalism and Communication',
        'Social Service (evening attendance)',
        'Management (evening attendance)',
        'Nursing',
        'Social Service',
        'Advertising and Marketing Management',
        'Basic Education',
        'Veterinary Nursing',
        'Equinculture',
        'Oral Hygiene',
        'Management',
        'Agronomy',
        'Biofuel Production Technologies',
        'Informatics Engineering'
    ], help="Program studi yang diambil")
    
    return {
        'Application_order': application_order,
        'Previous_qualification_grade': prev_qual_grade,
        'Admission_grade': admission_grade,
        'Curricular_units_1st_sem_enrolled': units_enrolled,
        'Curricular_units_1st_sem_evaluations': units_evaluations,
        'Curricular_units_1st_sem_approved': units_approved,
        'Curricular_units_1st_sem_grade': units_grade,
        'Age': age,
        'Scholarship_holder': scholarship,
        'Gender': gender,
        'Tuition_fees_up_to_date': tuition_updated,
        'Debtor': debtor,
        'Displaced': displaced,
        'Course': course
    }

def preprocess_input(user_input, encoders):
    """Preprocess user input for prediction"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame([user_input])
        
        # Encode categorical features
        categorical_features = ['Scholarship_holder', 'Gender', 'Tuition_fees_up_to_date', 
                               'Debtor', 'Displaced', 'Course']
        
        for feature in categorical_features:
            if feature in encoders:
                try:
                    # Check if value exists in encoder classes
                    if hasattr(encoders[feature], 'classes_'):
                        original_value = df[feature].iloc[0]
                        if original_value not in encoders[feature].classes_:
                            st.error(f"Nilai '{original_value}' untuk fitur '{feature}' tidak dikenali oleh encoder.")
                            st.info(f"Nilai yang valid untuk '{feature}': {list(encoders[feature].classes_)}")
                            return None
                    
                    df[feature] = encoders[feature].transform(df[feature])
                    
                except ValueError as e:
                    st.error(f"Error encoding {feature}: {e}")
                    return None
        
        return df
        
    except Exception as e:
        st.error(f"Error dalam preprocessing: {str(e)}")
        return None

def display_prediction_result(prediction, prediction_proba, encoders):
    """Display prediction results with styling"""
    try:
        # Decode prediction
        status_labels = encoders['Status'].classes_
        predicted_status = status_labels[prediction[0]]
        confidence = np.max(prediction_proba) * 100
        
        # Display result with color coding
        if predicted_status == 'Graduate':
            st.markdown(f"""
            <div class="section-box" style="border-color: #28a745; background: #f0fff0;">
                <div class="section-header" style="background: #d4edda; color: #155724;">
                    ✅ Prediksi: LULUS<br>
                    Confidence: {confidence:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif predicted_status == 'Dropout':
            st.markdown(f"""
            <div class="section-box" style="border-color: #dc3545; background: #ffe4e1;">
                <div class="section-header" style="background: #f8d7da; color: #721c24;">
                    ⚠️ Prediksi: DROPOUT<br>
                    Confidence: {confidence:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="section-box" style="border-color: #ffc107; background: #fffacd;">
                <div class="section-header" style="background: #fff3cd; color: #856404;">
                    📚 Prediksi: MASIH KULIAH<br>
                    Confidence: {confidence:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        return predicted_status, confidence
        
    except Exception as e:
        st.error(f"Error menampilkan hasil prediksi: {str(e)}")
        return None, None

def create_probability_chart(prediction_proba, encoders):
    """Create a more engaging and informative probability bar chart."""
    try:
        status_labels = encoders['Status'].classes_
        probabilities = prediction_proba[0] * 100

        # Create a DataFrame for better data handling with Plotly Express
        df_probs = pd.DataFrame({
            'Status': status_labels,
            'Probabilitas': probabilities
        }).sort_values('Probabilitas', ascending=False) # Sort to highlight the highest probability

        # Assign colors based on status
        color_map = {
            'Graduate': '#28a745',
            'Dropout': '#dc3545',
            'Enrolled': '#ffc107'
        }

        # Create the bar chart using Plotly Express for a cleaner look
        fig = px.bar(
            df_probs,
            x='Status',
            y='Probabilitas',
            color='Status', # Use status to color the bars
            color_discrete_map=color_map, # Apply the custom color map
            text='Probabilitas', # Display probability text on the bars
            title='<b>Probabilitas Prediksi Status Mahasiswa</b>', # Make title bold
        )

        # Update the layout for improved readability
        fig.update_layout(
            title_font_size=24,
            xaxis_title=None, # Remove x-axis title as it's self-explanatory
            yaxis_title='Probabilitas (%)',
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
            # Add a clear grid and cleaner background
            plot_bgcolor='rgba(255,255,255,0.8)',
            paper_bgcolor='rgba(255,255,255,0.8)',
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color='black', size=14)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#e0e0e0',
                tickfont=dict(color='black', size=14)
            ),
            # Add tooltips for more information on hover
            hovermode="x unified",
        )

        # Add percentage sign to the bar text and format
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Probabilitas: %{y:.1f}%'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating the probability chart: {str(e)}")
        return None
    
st.markdown("""
    <style>
    /* Styling for the light blue recommendation box */
    .recommendation-box {
        background-color: #e0f2f7; /* Light blue color */
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #81d4fa;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .recommendation-box strong {
        color: #01579b; /* Darker blue for emphasis */
    }
    .recommendation-box ul {
        margin-top: 10px;
        padding-left: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    st.markdown("---")
    
    # Load model and encoders
    model = load_model()
    encoders = load_encoders()
    
    # Check if both are loaded successfully
    if model is None or encoders is None:
        st.error("❌ Aplikasi tidak dapat berjalan karena model atau encoders gagal dimuat.")
        st.markdown("""
        ### 📋 Cara Mengatasi:
        
        1. **Pastikan file tersedia**:
            - `model.joblib` (model yang sudah ditraining)
            - `encoders.joblib` (encoder dari data training)
        
        2. **Cara membuat encoders.joblib**:
        ```python
        # Saat training model
        categorical_features = ['Scholarship_holder', 'Gender', 'Tuition_fees_up_to_date', 
                               'Debtor', 'Displaced', 'Course', 'Status']
        
        # Encode dan simpan
        encoders = {}
        for feature in categorical_features:
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            encoders[feature] = le
        
        joblib.dump(encoders, 'encoders.joblib')
        ```
        
        3. **Restart aplikasi** setelah file tersedia
        """)
        
        # Show file status
        st.subheader("📁 Status File:")
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists('model.joblib'):
                st.success("✅ model.joblib tersedia")
            else:
                st.error("❌ model.joblib tidak ditemukan")
        
        with col2:
            if os.path.exists('encoders.joblib'):
                st.success("✅ encoders.joblib tersedia")
            else:
                st.error("❌ encoders.joblib tidak ditemukan")
        
        st.stop()
    
    # Get user input
    user_input = get_user_input()
    
    # Prediction button
    if st.button("🔮 Prediksi Dropout", type="primary", use_container_width=True):
        
        with st.spinner("🔄 Memproses prediksi..."):
            # Preprocess input
            processed_input = preprocess_input(user_input, encoders)
            
            if processed_input is not None:
                # Make prediction
                try:
                    prediction = model.predict(processed_input)
                    prediction_proba = model.predict_proba(processed_input)
                    
                    # Display results
                    st.subheader("🎯 Hasil Prediksi")
                    predicted_status, confidence = display_prediction_result(prediction, prediction_proba, encoders)
                    
                    if predicted_status is not None:
                        # Additional insights
                        col_insight1, col_insight2 = st.columns(2)
                        
                        with col_insight1:
                            st.metric("Confidence Level", f"{confidence:.1f}%")
                            
                            # Risk level
                            if predicted_status == 'Dropout':
                                risk_level = "Tinggi"
                                risk_color = "🔴"
                            elif predicted_status == 'Graduate':
                                risk_level = "Rendah" 
                                risk_color = "🟢"
                            else:
                                risk_level = "Sedang"
                                risk_color = "🟡"
                            
                            st.metric("Risk Level", f"{risk_color} {risk_level}")
                        
                        with col_insight2:
                            # Show top probabilities
                            probs = prediction_proba[0]
                            status_labels = encoders['Status'].classes_
                            sorted_indices = np.argsort(probs)[::-1]
                            
                            st.write("**Top Probabilitas:**")
                            for i in range(min(len(status_labels), 3)):
                                idx = sorted_indices[i]
                                st.write(f"{i+1}. {status_labels[idx]}: {probs[idx]*100:.1f}%")
                        
                        # Show probability chart
                        fig = create_probability_chart(prediction_proba, encoders)
                        if fig is not None:
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Recommendations based on prediction
                        st.subheader("💡 Rekomendasi")
                        if predicted_status == 'Dropout':
                            st.markdown("""
                            <div class="recommendation-box">
                                <p><strong>⚠️ Mahasiswa ini berisiko tinggi untuk dropout. Rekomendasi:</strong></p>
                                <ul>
                                    <li>🎯 Berikan bimbingan akademik intensif</li>
                                    <li>📊 Monitor progress secara berkala</li>
                                    <li>📚 Pertimbangkan program remedial</li>
                                    <li>💬 Konseling untuk mengatasi masalah personal/finansial</li>
                                    <li>👥 Libatkan academic advisor dan orang tua</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                        elif predicted_status == 'Graduate':
                            st.markdown("""
                            <div class="recommendation-box">
                                <p><strong>✅ Mahasiswa ini memiliki peluang tinggi untuk lulus. Rekomendasi:</strong></p>
                                <ul>
                                    <li>🌟 Pertahankan motivasi belajar</li>
                                    <li>🏆 Dorong untuk mencapai prestasi yang lebih tinggi</li>
                                    <li>🎭 Libatkan dalam kegiatan pengembangan diri</li>
                                    <li>🎓 Persiapkan untuk tahap selanjutnya (kerja/S2)</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="recommendation-box">
                                <p><strong>📚 Mahasiswa ini masih dalam proses kuliah. Rekomendasi:</strong></p>
                                <ul>
                                    <li>📈 Monitor perkembangan secara rutin</li>
                                    <li>🤝 Berikan dukungan akademik yang diperlukan</li>
                                    <li>🔍 Identifikasi potensi masalah sejak dini</li>
                                    <li>💪 Tingkatkan engagement dengan program studi</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"❌ Error saat melakukan prediksi: {e}")

if __name__ == "__main__":

    main()
