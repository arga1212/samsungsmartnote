import streamlit as st

def initialize_session_state():
    """
    Inisialisasi semua session state yang dibutuhkan aplikasi
    """
    # Halaman saat ini
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Tipe pengguna (guru atau siswa)
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    
    # Wizard steps untuk proses rekam dan transkrip
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    
    # Jalur proses (dengan transkrip atau langsung)
    if 'process_path' not in st.session_state:
        st.session_state.process_path = None  # 'transcript' atau 'direct'
    
    # Audio files yang tersedia
    if 'audio_files' not in st.session_state:
        st.session_state.audio_files = {}
    
    # Audio yang dipilih untuk diproses
    if 'selected_audio' not in st.session_state:
        st.session_state.selected_audio = None
    
    # Transkrip asli dari audio
    if 'original_transcript' not in st.session_state:
        st.session_state.original_transcript = ""
    
    # Transkrip yang sudah diedit
    if 'edited_transcript' not in st.session_state:
        st.session_state.edited_transcript = ""
    
    # Statistik perubahan transkrip
    if 'transcript_stats' not in st.session_state:
        st.session_state.transcript_stats = {
            'added_words': 0,
            'removed_words': 0,
            'changed_words': 0
        }
    
    # Jenis output yang dipilih
    if 'output_types' not in st.session_state:
        st.session_state.output_types = []
    
    # Hasil dari proses summarize
    if 'summary_result' not in st.session_state:
        st.session_state.summary_result = ""
    
    # Hasil dari proses pembuatan modul
    if 'module_result' not in st.session_state:
        st.session_state.module_result = ""
    
    # Hasil dari pembuatan quiz
    if 'quiz_result' not in st.session_state:
        st.session_state.quiz_result = {}
    
    # Daftar quiz yang sudah dibuat
    if 'quizzes' not in st.session_state:
        st.session_state.quizzes = {}
    
    # Quiz yang sedang aktif
    if 'active_quiz' not in st.session_state:
        st.session_state.active_quiz = None
    
    # Jawaban siswa untuk quiz
    if 'student_answers' not in st.session_state:
        st.session_state.student_answers = {}

def reset_wizard():
    """
    Reset wizard steps ke awal
    """
    st.session_state.wizard_step = 1
    st.session_state.process_path = None
    st.session_state.selected_audio = None
    st.session_state.original_transcript = ""
    st.session_state.edited_transcript = ""
    st.session_state.transcript_stats = {
        'added_words': 0,
        'removed_words': 0,
        'changed_words': 0
    }
    st.session_state.output_types = []

def change_page(page):
    """
    Pindah ke halaman tertentu
    """
    st.session_state.current_page = page