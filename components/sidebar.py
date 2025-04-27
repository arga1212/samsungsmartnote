import streamlit as st
from utils.session_state import change_page, reset_wizard 

def create_sidebar():
    """
    Membuat sidebar navigasi sesuai dengan role pengguna
    """
    with st.sidebar:
        st.title("Smart Classroom 🎓")
        
        # User type selection jika belum dipilih
        if st.session_state.user_type is None:
            st.header("Pilih Jenis Pengguna")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👩‍🏫 Guru", use_container_width=True):
                    st.session_state.user_type = "teacher"
                    st.rerun()
            
            with col2:
                if st.button("👨‍🎓 Siswa", use_container_width=True):
                    st.session_state.user_type = "student"
                    st.rerun()
        
        # Menu navigasi untuk guru
        elif st.session_state.user_type == "teacher":
            st.subheader(f"Mode: Guru 👩‍🏫")
            
            st.markdown("### Menu Utama")
            
            if st.button("🏠 Dashboard", key="dashboard_btn", use_container_width=True):
                change_page("dashboard")
                reset_wizard()
                st.rerun()
            
            if st.button("🎙️ Upload Audio", key="upload_btn", use_container_width=True):
                change_page("upload")
                reset_wizard()
                st.rerun()
            
            st.markdown("### Hasil")
            
            if st.button("📝 Ringkasan", key="summary_btn", use_container_width=True):
                change_page("summary")
                st.rerun()
            
            if st.button("📚 Modul", key="module_btn", use_container_width=True):
                change_page("module")
                st.rerun()
            
            if st.button("❓ Quiz", key="quiz_btn", use_container_width=True):
                change_page("quiz_teacher")
                st.rerun()
        
        # Menu navigasi untuk siswa
        elif st.session_state.user_type == "student":
            st.subheader(f"Mode: Siswa 👨‍🎓")
            
            st.markdown("### Menu")
            
            if st.button("🏠 Dashboard", key="dashboard_btn", use_container_width=True):
                change_page("dashboard")
                st.rerun()
            
            if st.button("🎙️ Upload Audio", key="upload_btn", use_container_width=True):
                change_page("upload")
                reset_wizard()
                st.rerun()
            
            if st.button("📝 Ringkasan", key="summary_btn", use_container_width=True):
                change_page("summary")
                st.rerun()
            
            if st.button("📚 Modul", key="module_btn", use_container_width=True):
                change_page("module")
                st.rerun()
            
            if st.button("❓ Kerjakan Quiz", key="quiz_btn", use_container_width=True):
                change_page("quiz_student")
                st.rerun()
        
        # Tombol ganti pengguna
        if st.session_state.user_type is not None:
            st.markdown("---")
            if st.button("🔄 Ganti Pengguna", key="change_user_btn", use_container_width=True):
                st.session_state.user_type = None
                st.rerun()