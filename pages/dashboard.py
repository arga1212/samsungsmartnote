import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from utils.session_state import change_page

def render_dashboard():
    """
    Render halaman dashboard utama
    """
    st.markdown('<h1 class="main-header">Smart Classroom Dashboard</h1>', unsafe_allow_html=True)
    
    # Tampilkan konten dashboard berdasarkan tipe user
    if st.session_state.user_type == "teacher":
        render_teacher_dashboard()
    elif st.session_state.user_type == "student":
        render_student_dashboard()
    else:
        render_welcome_screen()

def render_welcome_screen():
    """
    Tampilkan layar sambutan jika belum ada user yang dipilih
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown("""
    # 👋 Selamat Datang di Smart Classroom!
    
    Smart Classroom adalah aplikasi yang membantu proses pembelajaran dengan menggunakan teknologi AI.
    
    ### 🎯 Fitur Utama:
    
    - **🎙️ Rekam & Upload Audio** - Rekam suara atau upload file audio
    - **📝 Transkrip Otomatis** - Konversi audio menjadi teks dengan AI
    - **📚 Buat Modul Pembelajaran** - Generate modul dari audio/transkrip
    - **📋 Ringkasan Materi** - Dapatkan ringkasan dari konten pembelajaran
    - **❓ Pembuatan Quiz** - Buat quiz interaktif untuk evaluasi
    
    ### 🚀 Mulai Menggunakan
    
    Pilih jenis pengguna Anda di sidebar untuk memulai:
    - **👩‍🏫 Guru** - Untuk membuat materi dan quiz
    - **👨‍🎓 Siswa** - Untuk belajar dan mengerjakan quiz
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_teacher_dashboard():
    """
    Render dashboard untuk guru
    """
    # Welcome Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👋 Selamat Datang, Guru!")
    st.markdown("Dashboard ini menampilkan ringkasan aktivitas dan materi pembelajaran Anda.")
    
    # Quick Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**🎙️ Audio**\n\n{len(st.session_state.audio_files)} file")
    
    with col2:
        quiz_count = len(st.session_state.quizzes)
        st.success(f"**❓ Quiz**\n\n{quiz_count} quiz aktif")
    
    with col3:
        # Sample data for module count
        module_count = sum(1 for _ in st.session_state.audio_files)
        st.warning(f"**📚 Modul**\n\n{module_count} modul")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 Aktivitas Terbaru")
    
    # Create some sample activity data if none exists
    if len(st.session_state.audio_files) == 0:
        # Sample data
        sample_data = [
            {"activity": "Upload audio", "item": "materi_biologi.mp3", "date": (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y %H:%M")},
            {"activity": "Generate Modul", "item": "Struktur Sel", "date": (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y %H:%M")},
            {"activity": "Create Quiz", "item": "Quiz Biologi Dasar", "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
        ]
        
        activity_df = pd.DataFrame(sample_data)
    else:
        # Convert actual activity from session state
        activities = []
        for audio_id, audio_info in st.session_state.audio_files.items():
            activities.append({
                "activity": "Upload audio", 
                "item": audio_info.get("filename", f"audio_{audio_id}"),
                "date": audio_info.get("timestamp", datetime.now().strftime("%d/%m/%Y %H:%M"))
            })
            
        for quiz_id, quiz_info in st.session_state.quizzes.items():
            activities.append({
                "activity": "Create Quiz",
                "item": f"Quiz {quiz_id}",
                "date": quiz_info.get("created_at", datetime.now().strftime("%d/%m/%Y %H:%M"))
            })
            
        activity_df = pd.DataFrame(activities)
        
        # Sort by date (newest first)
        if not activity_df.empty and "date" in activity_df.columns:
            activity_df = activity_df.sort_values(by="date", ascending=False)
    
    # Display activity table
    if not activity_df.empty:
        st.table(activity_df)
    else:
        st.info("Belum ada aktivitas. Mulai dengan mengupload audio atau membuat quiz.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🚀 Aksi Cepat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎙️ Upload Audio Baru", use_container_width=True):
            change_page("upload")
            st.rerun()
    
    with col2:
        if st.button("❓ Buat Quiz Baru", use_container_width=True):
            if not st.session_state.audio_files:
                st.error("Anda perlu mengupload audio terlebih dahulu untuk membuat quiz.")
            else:
                change_page("upload")  # Start the wizard process
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_student_dashboard():
    """
    Render dashboard untuk siswa
    """
    # Welcome Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👋 Selamat Datang, Siswa!")
    st.markdown("Dashboard ini menampilkan materi pembelajaran dan quiz yang tersedia untuk Anda.")
    
    # Quick Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_quiz = len(st.session_state.quizzes)
        st.info(f"**❓ Quiz Tersedia**\n\n{available_quiz} quiz")
    
    with col2:
        # Sample data for completed quizzes
        completed_quiz = len(st.session_state.student_answers)
        st.success(f"**✅ Quiz Selesai**\n\n{completed_quiz} quiz")
    
    with col3:
        # Sample data for average score (random for demo)
        avg_score = random.randint(70, 100) if completed_quiz > 0 else 0
        st.warning(f"**📊 Rata-rata Nilai**\n\n{avg_score}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Available Quiz
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## ❓ Quiz Tersedia")
    
    if st.session_state.quizzes:
        for quiz_id, quiz_info in st.session_state.quizzes.items():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"Quiz {quiz_id}")
                st.write(f"Jumlah Soal: {quiz_info.get('num_questions', 0)}")
                st.write(f"Dibuat pada: {quiz_info.get('created_at', 'Unknown')}")
            
            with col2:
                if st.button(f"Kerjakan Quiz", key=f"take_quiz_{quiz_id}", use_container_width=True):
                    st.session_state.active_quiz = quiz_id
                    change_page("quiz_student")
                    st.rerun()
    else:
        st.info("Belum ada quiz tersedia. Silakan kembali nanti.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Available Learning Materials
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📚 Materi Pembelajaran")
    
    # Sample data for learning materials
    if not st.session_state.audio_files:
        materials = [
            {"title": "Biologi Dasar - Struktur Sel", "type": "Module", "date": "12/04/2025"},
            {"title": "Fisika - Hukum Newton", "type": "Summary", "date": "15/04/2025"},
            {"title": "Kimia - Reaksi Redoks", "type": "Module", "date": "20/04/2025"}
        ]
        
        materials_df = pd.DataFrame(materials)
        st.table(materials_df)
    else:
        materials = []
        for audio_id, audio_info in st.session_state.audio_files.items():
            materials.append({
                "title": audio_info.get("filename", f"Material {audio_id}").replace(".mp3", "").replace(".wav", ""),
                "type": "Audio Material",
                "date": audio_info.get("timestamp", datetime.now().strftime("%d/%m/%Y"))
            })
            
        materials_df = pd.DataFrame(materials)
        st.table(materials_df)
    
    st.markdown('</div>', unsafe_allow_html=True)