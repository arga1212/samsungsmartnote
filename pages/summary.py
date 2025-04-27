import streamlit as st
import pandas as pd
from datetime import datetime

def render_summary():
    """
    Render the summary page to display generated summaries
    """
    st.markdown('<h1 class="main-header">Ringkasan Materi</h1>', unsafe_allow_html=True)
    
    # Summary card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if not st.session_state.summary_result:
        st.info("Belum ada ringkasan yang dibuat. Silakan buat ringkasan terlebih dahulu melalui proses upload audio.")
    else:
        # Display the summary
        st.markdown(st.session_state.summary_result)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Ringkasan (MD)",
                data=st.session_state.summary_result,
                file_name=f"ringkasan_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )
        
        with col2:
            # Convert markdown to PDF (simplified for demo)
            st.button("📥 Download Ringkasan (PDF)", disabled=True, 
                     help="Fitur ini akan tersedia dalam versi mendatang")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Previous summaries (history)
    if st.session_state.user_type == "teacher":
        render_summary_history()

def render_summary_history():
    """
    Render history of previously generated summaries
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Riwayat Ringkasan")
    
    # In a real app, this would be stored in a database
    # For demo, we'll create sample data
    
    # If we have actual data in session state, use that
    if len(st.session_state.audio_files) > 0:
        history_data = []
        
        for audio_id, audio_info in st.session_state.audio_files.items():
            # Only show entries that would have summaries (in a real app)
            if "summary" in st.session_state.output_types:
                history_data.append({
                    "title": audio_info.get("filename", "").replace(".mp3", "").replace(".wav", ""),
                    "date": audio_info.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    "words": "~500 kata",  # In a real app, calculate this
                    "id": audio_id
                })
        
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df[["title", "date", "words"]], use_container_width=True)
        else:
            st.info("Belum ada riwayat ringkasan.")
    else:
        # Sample data for demonstration
        sample_data = [
            {"title": "Fotosintesis", "date": "2025-04-22 09:30", "words": "520 kata"},
            {"title": "Hukum Newton", "date": "2025-04-20 14:15", "words": "430 kata"},
            {"title": "Sistem Peredaran Darah", "date": "2025-04-18 10:45", "words": "610 kata"}
        ]
        
        df = pd.DataFrame(sample_data)
        st.dataframe(df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)