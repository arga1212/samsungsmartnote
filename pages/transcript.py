import streamlit as st
import time
from utils.session_state import change_page
from utils.ai_generator import generate_transcript
from utils.text_processor import compare_texts, generate_highlighted_html, count_words
from components.wizard_progress import render_wizard_progress, render_wizard_nav_buttons

def render_transcript():
    """
    Render transcript editing page
    """
    st.markdown('<h1 class="main-header">Edit Transkrip</h1>', unsafe_allow_html=True)
    
    # Check if we're in the right process path
    if st.session_state.process_path != "transcript":
        st.error("Halaman ini hanya dapat diakses melalui jalur transkrip.")
        st.button("Kembali ke Upload", on_click=lambda: change_page("upload"))
        return
    
    # Ensure we have a selected audio
    if not st.session_state.selected_audio or st.session_state.selected_audio not in st.session_state.audio_files:
        st.error("Tidak ada file audio yang dipilih. Silakan pilih file audio terlebih dahulu.")
        st.button("Kembali ke Upload", on_click=lambda: change_page("upload"))
        return
    
    # Show wizard progress
    step_titles = ["Upload", "Transkrip", "Pilih Output", "Hasil"]
    render_wizard_progress(
        current_step=st.session_state.wizard_step,
        total_steps=4,
        step_titles=step_titles
    )
    
    # Get selected audio info
    audio_info = st.session_state.audio_files[st.session_state.selected_audio]
    
    # Display audio information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### Audio: {audio_info['filename']}")
        st.write(f"Ukuran: {audio_info['size']} | Durasi: {audio_info.get('duration', 'Unknown')}")
    
    with col2:
        st.audio(audio_info['path'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transcript card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Transkripsi Audio")
    
    # If we don't have a transcript yet, generate it
    if not st.session_state.original_transcript:
        if st.button("Mulai Transkripsi", key="start_transcript"):
            with st.spinner("Mentranskripsikan audio... Ini mungkin memerlukan waktu beberapa menit."):
                try:
                    # In a real app, we would call the Gemini API here
                    # For this demo, simulate a delay and use sample text
                    # transcript = generate_transcript(audio_info['path'])
                    
                    # Simulate API call
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.05)
                        progress_bar.progress(i + 1)
                    
                    # Sample transcript (in real app, this would come from the API)
                    transcript = """
                    Selamat datang di pelajaran tentang Fotosintesis. Fotosintesis adalah proses pembuatan makanan oleh tumbuhan hijau dengan bantuan cahaya matahari.

                    Proses ini terjadi di organel sel tumbuhan yang disebut kloroplas, yang mengandung pigmen hijau yang kita kenal sebagai klorofil. Klorofil inilah yang memberikan warna hijau pada tumbuhan dan berperan penting dalam menangkap energi cahaya matahari.

                    Dalam fotosintesis, tumbuhan mengambil karbon dioksida (CO2) dari udara melalui stomata pada daun dan air (H2O) dari tanah melalui akar. Dengan bantuan energi cahaya matahari, tumbuhan mengubah CO2 dan H2O menjadi glukosa (C6H12O6) dan melepaskan oksigen (O2) sebagai produk sampingan.

                    Fotosintesis dapat dirangkum dalam persamaan kimia berikut:
                    6 CO2 + 6 H2O + Energi Cahaya → C6H12O6 + 6 O2

                    Proses fotosintesis terdiri dari dua tahap utama:
                    1. Reaksi terang: Terjadi ketika ada cahaya matahari. Pada tahap ini, energi dari matahari diubah menjadi energi kimia dalam bentuk ATP dan NADPH.
                    2. Reaksi gelap atau siklus Calvin: Tidak memerlukan cahaya langsung. Pada tahap ini, CO2 diubah menjadi glukosa menggunakan ATP dan NADPH yang dihasilkan dari reaksi terang.

                    Fotosintesis sangat penting bagi kehidupan di Bumi karena:
                    - Menyediakan makanan bagi tumbuhan dan secara tidak langsung bagi semua organisme lain
                    - Menghasilkan oksigen yang diperlukan untuk respirasi sebagian besar organisme
                    - Mengurangi kadar CO2 di atmosfer, yang membantu mengurangi efek rumah kaca
                    
                    Faktor-faktor yang memengaruhi laju fotosintesis antara lain:
                    - Intensitas cahaya
                    - Konsentrasi CO2
                    - Suhu
                    - Ketersediaan air
                    - Jumlah klorofil
                    """
                    
                    st.session_state.original_transcript = transcript
                    st.session_state.edited_transcript = transcript
                    st.rerun()
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat mentranskripsikan audio: {str(e)}")
    else:
        # Show both original and edited transcript
        tab1, tab2 = st.tabs(["Edit Transkrip", "Bandingkan Perubahan"])
        
        with tab1:
            edited_transcript = st.text_area(
                "Edit transkrip sesuai kebutuhan:", 
                value=st.session_state.edited_transcript,
                height=400
            )
            
            if edited_transcript != st.session_state.edited_transcript:
                st.session_state.edited_transcript = edited_transcript
                
                # Calculate statistics
                stats, diff = compare_texts(st.session_state.original_transcript, edited_transcript)
                st.session_state.transcript_stats = stats
        
        with tab2:
            if st.session_state.original_transcript == st.session_state.edited_transcript:
                st.info("Belum ada perubahan yang dilakukan pada transkrip.")
            else:
                # Show statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Kata Ditambahkan", st.session_state.transcript_stats['added_words'])
                
                with col2:
                    st.metric("Kata Dihapus", st.session_state.transcript_stats['removed_words'])
                
                with col3:
                    st.metric("Kata Diubah", st.session_state.transcript_stats['changed_words'])
                
                # Show highlighted differences
                st.markdown("### Teks dengan Perubahan")
                highlighted_html = generate_highlighted_html(st.session_state.original_transcript, st.session_state.edited_transcript)
                
                st.markdown("""
                <style>
                .added { background-color: #CCFFCC; padding: 2px; border-radius: 3px; }
                .changed { background-color: #FFFF99; padding: 2px; border-radius: 3px; }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div>{highlighted_html}</div>", unsafe_allow_html=True)
        
        # Navigation buttons
        render_wizard_nav_buttons(
            back_callback=lambda: back_to_upload(),
            next_callback=lambda: proceed_to_generate(),
            current_step=2,
            total_steps=4
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def back_to_upload():
    """Go back to upload page"""
    st.session_state.wizard_step = 1
    change_page("upload")

def proceed_to_generate():
    """Proceed to generate page"""
    st.session_state.wizard_step = 3
    change_page("generate")