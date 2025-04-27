import streamlit as st
import pandas as pd
from datetime import datetime

def render_module():
    """
    Render the module page to display generated learning modules
    """
    st.markdown('<h1 class="main-header">Modul Pembelajaran</h1>', unsafe_allow_html=True)
    
    # Module card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if not st.session_state.module_result:
        st.info("Belum ada modul yang dibuat. Silakan buat modul terlebih dahulu melalui proses upload audio.")
    else:
        # Display the module
        st.markdown(st.session_state.module_result)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Modul (MD)",
                data=st.session_state.module_result,
                file_name=f"modul_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )
        
        with col2:
            # Convert markdown to PDF (simplified for demo)
            st.button("📥 Download Modul (PDF)", disabled=True, 
                     help="Fitur ini akan tersedia dalam versi mendatang")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Previous modules (history)
    if st.session_state.user_type == "teacher":
        render_module_history()

def render_module_history():
    """
    Render history of previously generated modules
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Riwayat Modul")
    
    # In a real app, this would be stored in a database
    # For demo, we'll create sample data
    
    # If we have actual data in session state, use that
    if len(st.session_state.audio_files) > 0:
        history_data = []
        
        for audio_id, audio_info in st.session_state.audio_files.items():
            # Only show entries that would have modules (in a real app)
            if "module" in st.session_state.output_types:
                history_data.append({
                    "title": audio_info.get("filename", "").replace(".mp3", "").replace(".wav", ""),
                    "tanggal": audio_info.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    "panjang": "~1500 kata",  # In a real app, calculate this
                    "id": audio_id
                })
        
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df[["title", "tanggal", "panjang"]], use_container_width=True)
        else:
            st.info("Belum ada riwayat modul.")
    else:
        # Sample data for demonstration
        sample_data = [
            {"title": "Fotosintesis", "tanggal": "2025-04-22 09:30", "panjang": "1520 kata"},
            {"title": "Hukum Newton", "tanggal": "2025-04-20 14:15", "panjang": "1230 kata"},
            {"title": "Sistem Peredaran Darah", "tanggal": "2025-04-18 10:45", "panjang": "1810 kata"}
        ]
        
        df = pd.DataFrame(sample_data)
        st.dataframe(df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Module templates (for teachers)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Template Modul")
    
    st.write("Gunakan template berikut untuk membuat modul baru:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📚 Modul Standar
        
        Template modul pembelajaran lengkap dengan pendahuluan, materi, dan latihan.
        """)