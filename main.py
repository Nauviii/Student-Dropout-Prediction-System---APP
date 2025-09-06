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

    /* Styling untuk warning dan info boxes */
    .recommendation-box {{
        background-color: #e0f2f7;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #81d4fa;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-size: 1.1em;
        line-height: 1.6;
    }}
    .recommendation-box strong {{
        color: #01579b;
    }}
    .recommendation-box ul {{
        margin-top: 10px;
        padding-left: 20px;
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
                         Selamat Datang!
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

@st.cache_resource
def get_model_feature_names():
    """Get expected feature names from model"""
    try:
        model = load_model()
        if model is not None and hasattr(model, 'feature_names_in_'):
            return list(model.feature_names_in_)
        else:
            # Fallback: return common feature names if model doesn't have feature_names_in_
            st.warning("⚠️ Model tidak memiliki informasi feature names. Menggunakan feature names default.")
            return None
    except Exception as e:
        st.error(f"Error getting model features: {e}")
        return None

def get_user_input():
    """Create input widgets for user data - Updated to match model features"""
    st.sidebar.header("📊 Input Data Mahasiswa")
    
    # Get expected features from model
    expected_features = get_model_feature_names()
    if expected_features:
        st.sidebar.info(f"Model mengharapkan {len(expected_features)} features")
        with st.sidebar.expander("Lihat Expected Features"):
            for i, feature in enumerate(expected_features, 1):
                st.write(f"{i}. {feature}")
    
    # Create input dictionary with all possible features
    user_input = {}
    
    # Numerical features - sesuaikan dengan error message
    st.sidebar.subheader("Data Numerik")
    
    # Basic info
    user_input['Age'] = st.sidebar.number_input("Age", min_value=17, max_value=70, value=20, help="Usia mahasiswa")
    user_input['Application_order'] = st.sidebar.number_input("Application Order", min_value=0, max_value=10, value=1, help="Urutan aplikasi pendaftaran")
    
    # Grades
    user_input['Previous_qualification_grade'] = st.sidebar.slider("Previous Qualification Grade", 0.0, 200.0, 120.0, 0.1, help="Nilai kualifikasi sebelumnya")
    user_input['Admission_grade'] = st.sidebar.slider("Admission Grade", 0.0, 200.0, 120.0, 0.1, help="Nilai penerimaan")
    
    # Semester 1 units
    st.sidebar.subheader("Data Semester 1")
    user_input['Curricular_units_1st_sem_enrolled'] = st.sidebar.number_input("Units Enrolled (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang diambil")
    user_input['Curricular_units_1st_sem_evaluations'] = st.sidebar.number_input("Units Evaluations (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang dievaluasi")
    user_input['Curricular_units_1st_sem_approved'] = st.sidebar.number_input("Units Approved (Sem 1)", min_value=0, max_value=30, value=6, help="Jumlah mata kuliah yang lulus")
    user_input['Curricular_units_1st_sem_grade'] = st.sidebar.slider("Units Grade (Sem 1)", 0.0, 20.0, 12.0, 0.1, help="Rata-rata nilai semester 1")
    
    # Additional features that might be expected by model
    st.sidebar.subheader("Data Tambahan")
    
    # Business/Travel related (if model expects these)
    user_input['BusinessTravel'] = st.sidebar.selectbox("Business Travel", ['No', 'Yes'], help="Apakah sering melakukan perjalanan bisnis?")
    
    # Department
    user_input['Department'] = st.sidebar.selectbox("Department", [
        'Engineering', 'Business', 'Education', 'Arts', 'Science', 'Medicine', 'Other'
    ], help="Departemen/Fakultas")
    
    # Distance from home
    user_input['DistanceFromHome'] = st.sidebar.slider("Distance From Home (km)", 0, 100, 10, 1, help="Jarak dari rumah dalam km")
    
    # Environment Satisfaction
    user_input['EnvironmentSatisfaction'] = st.sidebar.slider("Environment Satisfaction", 1, 5, 3, 1, help="Tingkat kepuasan lingkungan (1-5)")
    
    # Job Role
    user_input['JobRole'] = st.sidebar.selectbox("Job Role", [
        'Student', 'Part-time Worker', 'Intern', 'Full-time Worker', 'Unemployed'
    ], help="Peran pekerjaan saat ini")
    
    # Categorical features - existing ones
    st.sidebar.subheader("Data Kategorikal")
    user_input['Scholarship_holder'] = st.sidebar.selectbox("Scholarship Holder", ['No', 'Yes'], help="Apakah penerima beasiswa?")
    user_input['Gender'] = st.sidebar.selectbox("Gender", ['Male', 'Female'], help="Jenis kelamin")
    user_input['Tuition_fees_up_to_date'] = st.sidebar.selectbox("Tuition Fees Up to Date", ['No', 'Yes'], help="Apakah biaya kuliah up to date?")
    user_input['Debtor'] = st.sidebar.selectbox("Debtor", ['No', 'Yes'], help="Apakah memiliki hutang?")
    user_input['Displaced'] = st.sidebar.selectbox("Displaced", ['No', 'Yes'], help="Apakah mengalami perpindahan tempat tinggal?")
    
    user_input['Course'] = st.sidebar.selectbox("Course", [
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
    
    # Validation for semester units
    if user_input['Curricular_units_1st_sem_evaluations'] > user_input['Curricular_units_1st_sem_enrolled']:
        st.sidebar.warning("⚠️ Units Evaluations tidak boleh lebih besar dari Units Enrolled")
    
    if user_input['Curricular_units_1st_sem_approved'] > user_input['Curricular_units_1st_sem_evaluations']:
        st.sidebar.warning("⚠️ Units Approved tidak boleh lebih besar dari Units Evaluations")
    
    return user_input

def preprocess_input(user_input, encoders, expected_features=None):
    """Preprocess user input for prediction - Updated to handle feature matching"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame([user_input])
        
        # Get expected features if available
        if expected_features is None:
            expected_features = get_model_feature_names()
        
        if expected_features:
            # Only keep features that are expected by the model
            missing_features = []
            available_features = []
            
            for feature in expected_features:
                if feature in df.columns:
                    available_features.append(feature)
                else:
                    missing_features.append(feature)
                    # Add missing feature with default value
                    if feature.endswith('_encoded') or feature in ['Gender', 'Course', 'Department', 'JobRole', 'BusinessTravel']:
                        df[feature] = 0  # Default encoded value
                    else:
                        df[feature] = 0  # Default numeric value
            
            # Show info about feature matching
            if missing_features:
                st.warning(f"⚠️ Model mengharapkan {len(missing_features)} features yang tidak tersedia dalam input form.")
                with st.expander("Detail Missing Features"):
                    st.write("Missing features (akan diisi dengan nilai default):")
                    for feature in missing_features:
                        st.write(f"- {feature}")
            
            if available_features:
                st.info(f"✅ {len(available_features)} features tersedia dari input form")
        
        # Encode categorical features
        categorical_features = ['Scholarship_holder', 'Gender', 'Tuition_fees_up_to_date', 
                               'Debtor', 'Displaced', 'Course', 'Department', 'JobRole', 'BusinessTravel']
        
        for feature in categorical_features:
            if feature in df.columns and feature in encoders:
                try:
                    # Check if value exists in encoder classes
                    if hasattr(encoders[feature], 'classes_'):
                        original_value = df[feature].iloc[0]
                        if original_value not in encoders[feature].classes_:
                            st.warning(f"Nilai '{original_value}' untuk fitur '{feature}' tidak dikenali. Menggunakan nilai default.")
                            # Use the first class as default
                            df[feature] = encoders[feature].classes_[0]
                    
                    df[feature] = encoders[feature].transform(df[feature])
                    
                except ValueError as e:
                    st.warning(f"Warning encoding {feature}: {e}. Menggunakan nilai default.")
                    df[feature] = 0
        
        # Ensure all expected features are present and in correct order
        if expected_features:
            # Reorder columns to match expected features
            df = df.reindex(columns=expected_features, fill_value=0)
        
        return df
        
    except Exception as e:
        st.error(f"Error dalam preprocessing: {str(e)}")
        return None

def display_prediction_result(prediction, prediction_proba, encoders):
    """Display prediction results with styling"""
    try:
        # Decode prediction
        if 'Status' in encoders:
            status_labels = encoders['Status'].classes_
            predicted_status = status_labels[prediction[0]]
        else:
            # Fallback if Status encoder not available
            status_mapping = {0: 'Dropout', 1: 'Enrolled', 2: 'Graduate'}
            predicted_status = status_mapping.get(prediction[0], 'Unknown')
        
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
        if 'Status' in encoders:
            status_labels = encoders['Status'].classes_
        else:
            # Fallback labels
            status_labels = ['Dropout', 'Enrolled', 'Graduate']
            
        probabilities = prediction_proba[0] * 100

        # Create a DataFrame for better data handling with Plotly Express
        df_probs = pd.DataFrame({
            'Status': status_labels[:len(probabilities)],  # Ensure matching length
            'Probabilitas': probabilities
        }).sort_values('Probabilitas', ascending=False)

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
            color='Status',
            color_discrete_map=color_map,
            text='Probabilitas',
            title='<b>Probabilitas Prediksi Status Mahasiswa</b>',
        )

        # Update the layout for improved readability
        fig.update_layout(
            title_font_size=24,
            xaxis_title=None,
            yaxis_title='Probabilitas (%)',
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
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

def main():
    """Main application function"""
    # Sample data display
    col1, col2 = st.columns(2)

    with col1:
        # Data Akademik
        with st.container():
            st.markdown("### 📊 Ringkasan Akademik")
            st.markdown("📋 **Application Order:** 1")
            st.markdown("🎯 **Previous Qualification Grade:** 120.0")
            st.markdown("📖 **Admission Grade:** 120.0")
        
        # Data Semester 1
        with st.container():
            st.markdown("### 📚 Data Semester 1")
            st.markdown("📑 **Units Enrolled:** 6")
            st.markdown("📝 **Units Evaluations:** 6")
            st.markdown("✅ **Units Approved:** 6")

    with col2:
        # Data Personal
        with st.container():
            st.markdown("### 👤 Data Personal")
            st.markdown("👨 **Gender:** Male")
            st.markdown("🎨 **Course:** Animation and Multimedia Design")
            st.markdown("👤 **Age:** 20")
        
        # Status Keuangan
        with st.container():
            st.markdown("### 💰 Status Keuangan")
            st.markdown("💳 **Tuition Fees Up to Date:** No")
            st.markdown("💰 **Debtor:** No")
            st.markdown("🏠 **Displaced:** No")
    
    st.markdown("---")
    
    # Load model and encoders
    model = load_model()
    encoders = load_encoders()
    expected_features = get_model_feature_names()
    
    # Check if model is loaded successfully
    if model is None:
        st.error("❌ Aplikasi tidak dapat berjalan karena model gagal dimuat.")
        st.markdown("""
        ### 📋 Cara Mengatasi:
        
        1. **Pastikan file tersedia**:
            - `model.joblib` (model yang sudah ditraining)
        
        2. **Restart aplikasi** setelah file tersedia
        """)
        
        # Show file status
        st.subheader("📁 Status File:")
        if os.path.exists('model.joblib'):
            st.success("✅ model.joblib tersedia")
        else:
            st.error("❌ model.joblib tidak ditemukan")
        
        st.stop()
    
    # Handle missing encoders
    if encoders is None:
        st.warning("⚠️ Encoders tidak tersedia. Menggunakan fallback encoding.")
        encoders = {}
    
    # Get user input
    user_input = get_user_input()
    
    # Prediction button
    if st.button("🔮 Prediksi Dropout", type="primary", use_container_width=True):
        
        with st.spinner("🔄 Memproses prediksi..."):
            # Preprocess input
            processed_input = preprocess_input(user_input, encoders, expected_features)
            
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
                            if 'Status' in encoders:
                                status_labels = encoders['Status'].classes_
                            else:
                                status_labels = ['Dropout', 'Enrolled', 'Graduate']
                                
                            sorted_indices = np.argsort(probs)[::-1]
                            
                            st.write("**Top Probabilitas:**")
                            for i in range(min(len(status_labels), len(probs))):
                                idx = sorted_indices[i]
                                if idx < len(status_labels):
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
                    st.info("💡 Tips troubleshooting:")
                    st.write("- Pastikan model kompatibel dengan input features")
                    st.write("- Periksa format dan tipe data input")
                    st.write("- Pastikan encoders sesuai dengan model")

if __name__ == "__main__":
    main()
