import streamlit as st
import os
from utils.audio_processor import save_uploaded_file, is_valid_audio_file
from utils.flask_client import get_file_list, download_file, check_server_status
from utils.session_state import change_page
from components.wizard_progress import render_wizard_progress, render_wizard_nav_buttons
from datetime import datetime

def render_upload():
    """
    Render audio upload page
    """
    st.markdown('<h1 class="main-header">Upload Audio</h1>', unsafe_allow_html=True)
    
    # Wizard steps if in process mode
    if st.session_state.wizard_step > 1:
        step_titles = ["Upload", "Transkrip", "Pilih Output", "Hasil"]
        render_wizard_progress(
            current_step=st.session_state.wizard_step,
            total_steps=4,
            step_titles=step_titles
        )
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Different modes: upload from local or from server
    tab1, tab2 = st.tabs(["Upload dari Perangkat", "Audio dari Server"])
    
    with tab1:
        render_local_upload()
    
    with tab2:
        render_server_files()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # If we have audio files, show next step options
    if st.session_state.audio_files and st.session_state.wizard_step == 1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Pilih Jalur Pemrosesan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✏️ Dengan Transkrip & Edit
            
            Proses audio melalui transkrip terlebih dahulu, lalu edit hasil transkripsi sebelum menghasilkan output.
            
            **Cocok untuk:** Rekaman asli atau konten yang memerlukan verifikasi/koreksi.
            """)
            
            if st.button("Pilih Jalur Transkrip", key="choose_transcript_path", use_container_width=True):
                if not st.session_state.selected_audio:
                    st.error("Pilih file audio terlebih dahulu!")
                else:
                    st.session_state.process_path = "transcript"
                    st.session_state.wizard_step = 2
                    change_page("transcript")
                    st.rerun()
        
        with col2:
            st.markdown("""
            ### 🚀 Langsung ke Output
            
            Proses audio langsung menjadi output (ringkasan, modul, quiz) tanpa melalui tahap transkrip dan edit.
            
            **Cocok untuk:** Materi dari sumber eksternal yang sudah terverifikasi.
            """)
            
            if st.button("Pilih Jalur Langsung", key="choose_direct_path", use_container_width=True):
                if not st.session_state.selected_audio:
                    st.error("Pilih file audio terlebih dahulu!")
                else:
                    st.session_state.process_path = "direct"
                    st.session_state.wizard_step = 3
                    change_page("generate")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_local_upload():
    """
    Render local file upload interface
    """
    st.subheader("Upload File Audio")
    
    st.markdown("""
    Upload file audio dari perangkat Anda.
    
    **Format yang didukung:** WAV, MP3, M4A, OGG
    **Ukuran maksimum:** 50 MB
    """)
    
    uploaded_file = st.file_uploader("Pilih file audio", type=["wav", "mp3", "m4a", "ogg"])
    
    if uploaded_file is not None:
        # Check if file is valid
        if not is_valid_audio_file(uploaded_file):
            st.error("File tidak valid. Pastikan format dan ukuran file sesuai.")
            return
        
        # Save uploaded file
        with st.spinner("Menyimpan file..."):
            file_path, file_info = save_uploaded_file(uploaded_file)
            
            if file_path and file_info:
                # Add to session state
                st.session_state.audio_files[file_info["id"]] = file_info
                st.session_state.selected_audio = file_info["id"]
                
                st.success(f"File {uploaded_file.name} berhasil diupload!")
                st.audio(file_path)

def render_server_files():
    """
    Render interface for files available on the Flask server
    """
    st.subheader("Audio dari Server")
    
    # Check server connectivity
    server_online = check_server_status()
    
    if not server_online:
        st.error("Tidak dapat terhubung ke server. Pastikan server berjalan dan dapat diakses.")
        return
    
    # Get list of files from server
    with st.spinner("Mengambil daftar file dari server..."):
        files = get_file_list()
    
    if not files:
        st.info("Tidak ada file audio di server. Upload file melalui ESP32 atau tab Upload dari Perangkat.")
        return
    
    # Display file list
    st.write(f"Ditemukan {len(files)} file audio di server:")
    
    for i, file_info in enumerate(files):
        col1, col2, col3 = st.columns([0.6, 0.3, 0.1])
        
        filename = file_info.get('filename', f"file_{i}")
        size = file_info.get('size', 'Unknown')
        date = file_info.get('modified', 'Unknown')
        
        with col1:
            st.write(f"**{filename}**")
            st.caption(f"Modified: {date}")
        
        with col2:
            st.write(f"Size: {size}")
        
        with col3:
            if st.button("Pilih", key=f"select_server_{i}"):
                with st.spinner(f"Mengunduh {filename}..."):
                    # Download the file
                    temp_path = os.path.join("temp", filename)
                    download_path = download_file(filename, temp_path)
                    
                    if download_path:
                        # Create file info
                        file_id = f"server_{i}"
                        file_info = {
                            "id": file_id,
                            "filename": filename,
                            "path": download_path,
                            "size": size,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "duration": "Unknown",  # In a real app, extract this from audio metadata
                            "source": "server"
                        }
                        
                        # Add to session state
                        st.session_state.audio_files[file_id] = file_info
                        st.session_state.selected_audio = file_id
                        
                        st.success(f"File {filename} berhasil diunduh!")
                        st.audio(download_path)
                    else:
                        st.error(f"Gagal mengunduh {filename}")