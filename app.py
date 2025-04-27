import streamlit as st
import os
import sys

# Menambahkan direktori saat ini ke path untuk import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import komponen
from components.sidebar import create_sidebar
from utils.session_state import initialize_session_state

# Set konfigurasi halaman
st.set_page_config(
    page_title="Smart Classroom",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2563EB;
            margin-bottom: 0.8rem;
        }
        .card {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #EFF6FF;
            border: 1px solid #BFDBFE;
            color: #1E40AF;
            margin-bottom: 1rem;
        }
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #ECFDF5;
            border: 1px solid #A7F3D0;
            color: #065F46;
            margin-bottom: 1rem;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #FFFBEB;
            border: 1px solid #FDE68A;
            color: #92400E;
            margin-bottom: 1rem;
        }
        .error-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #FEF2F2;
            border: 1px solid #FECACA;
            color: #B91C1C;
            margin-bottom: 1rem;
        }
        .stButton button {
            width: 100%;
        }
        /* Styling untuk progress steps */
        .progress-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        .progress-step {
            flex: 1;
            text-align: center;
            position: relative;
        }
        .progress-step::after {
            content: '';
            position: absolute;
            top: 1.5rem;
            left: 50%;
            right: -50%;
            height: 0.25rem;
            background-color: #D1D5DB;
            z-index: -1;
        }
        .progress-step:last-child::after {
            display: none;
        }
        .step-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 9999px;
            background-color: #D1D5DB;
            color: white;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .step-active .step-number {
            background-color: #2563EB;
        }
        .step-completed .step-number {
            background-color: #10B981;
        }
        .step-active .step-text {
            color: #2563EB;
            font-weight: bold;
        }
        .step-completed .step-text {
            color: #10B981;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Inisialisasi session state
    initialize_session_state()
    
    # Load CSS
    load_css()
    
    # Tampilkan sidebar
    create_sidebar()
    
    # Tampilkan konten berdasarkan halaman saat ini
    if st.session_state.current_page == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    
    elif st.session_state.current_page == "upload":
        from pages.upload import render_upload
        render_upload()
    
    elif st.session_state.current_page == "transcript":
        from pages.transcript import render_transcript
        render_transcript()
    
    elif st.session_state.current_page == "generate":
        from pages.gen import render_generate
        render_generate()
    
    elif st.session_state.current_page == "summary":
        from pages.summary import render_summary
        render_summary()
    
    elif st.session_state.current_page == "module":
        from pages.module import render_module
        render_module()
    
    elif st.session_state.current_page == "quiz_teacher":
        from pages.quiz_teacher import render_quiz_teacher
        render_quiz_teacher()
    
    elif st.session_state.current_page == "quiz_student":
        from pages.quiz_student import render_quiz_student
        render_quiz_student()

if __name__ == "__main__":
    main()