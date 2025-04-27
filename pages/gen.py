import streamlit as st
import time
import uuid
from datetime import datetime
from utils.session_state import change_page
from utils.ai_generator import generate_summary, generate_module, generate_quiz
from components.wizard_progress import render_wizard_progress, render_wizard_nav_buttons

def render_generate():
    """
    Render the generate output selection page
    """
    st.markdown('<h1 class="main-header">Pilih Output</h1>', unsafe_allow_html=True)
    
    # Check if we have a selected audio
    if not st.session_state.selected_audio or st.session_state.selected_audio not in st.session_state.audio_files:
        st.error("Tidak ada file audio yang dipilih. Silakan pilih file audio terlebih dahulu.")
        st.button("Kembali ke Upload", on_click=lambda: change_page("upload"))
        return
    
    # Ensure we're in the right process path
    if not st.session_state.process_path:
        st.error("Proses tidak valid. Silakan kembali ke halaman Upload.")
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
    
    # If we're in transcript path, show the transcript
    if st.session_state.process_path == "transcript" and st.session_state.edited_transcript:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Transkrip yang Digunakan")
        
        with st.expander("Lihat Transkrip", expanded=False):
            st.markdown(st.session_state.edited_transcript)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Output selection
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Pilih Jenis Output")
    st.markdown("Pilih satu atau lebih jenis output yang ingin dihasilkan dari audio/transkrip:")
    
    # Initialize output types list if empty
    if not hasattr(st.session_state, 'output_types') or st.session_state.output_types is None:
        st.session_state.output_types = []
    
    # Output selection checkboxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.checkbox("📝 Ringkasan", value="summary" in st.session_state.output_types):
            if "summary" not in st.session_state.output_types:
                st.session_state.output_types.append("summary")
        else:
            if "summary" in st.session_state.output_types:
                st.session_state.output_types.remove("summary")
    
    with col2:
        if st.checkbox("📚 Modul Pembelajaran", value="module" in st.session_state.output_types):
            if "module" not in st.session_state.output_types:
                st.session_state.output_types.append("module")
        else:
            if "module" in st.session_state.output_types:
                st.session_state.output_types.remove("module")
    
    with col3:
        if st.checkbox("❓ Quiz", value="quiz" in st.session_state.output_types):
            if "quiz" not in st.session_state.output_types:
                st.session_state.output_types.append("quiz")
        else:
            if "quiz" in st.session_state.output_types:
                st.session_state.output_types.remove("quiz")
    
    # If quiz is selected, show quiz options
    if "quiz" in st.session_state.output_types:
        st.markdown("#### Opsi Quiz")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input("Jumlah Soal:", min_value=1, max_value=20, value=5, key="quiz_num_questions")
        
        with col2:
            st.selectbox("Tingkat Kesulitan:", ["Mudah", "Sedang", "Sulit"], index=1, key="quiz_difficulty")
    
    # Generate button
    if st.session_state.output_types:
        if st.button("Proses & Hasilkan Output", use_container_width=True):
            with st.spinner("Memproses... Mohon tunggu, ini mungkin memerlukan waktu beberapa menit."):
                try:
                    # Process each selected output type
                    if st.session_state.process_path == "transcript":
                        # Use edited transcript for generation
                        content = st.session_state.edited_transcript
                        is_audio = False
                        audio_path = None
                    else:  # direct path
                        # Use audio directly
                        content = None
                        is_audio = True
                        audio_path = audio_info['path']
                    
                    # Process each output type with progress bar
                    progress_bar = st.progress(0)
                    total_outputs = len(st.session_state.output_types)
                    
                    for i, output_type in enumerate(st.session_state.output_types):
                        progress_text = f"Memproses {output_type}... ({i+1}/{total_outputs})"
                        st.write(progress_text)
                        
                        if output_type == "summary":
                            # In a real app, call the actual Gemini API
                            # For demo, simulate delay and use sample content
                            time.sleep(2)
                            
                            # Sample summary (in real app, would be generated by AI)
                            summary = """
                            # Ringkasan: Fotosintesis
                            
                            ## Definisi dan Proses Dasar
                            - **Fotosintesis**: Proses pembuatan makanan oleh tumbuhan hijau menggunakan cahaya matahari
                            - **Lokasi**: Terjadi di kloroplas yang mengandung klorofil
                            - **Bahan**: CO₂ dari udara, H₂O dari tanah, dan energi cahaya matahari
                            - **Hasil**: Glukosa (C₆H₁₂O₆) dan oksigen (O₂)
                            - **Persamaan**: 6 CO₂ + 6 H₂O + Energi Cahaya → C₆H₁₂O₆ + 6 O₂
                            
                            ## Tahapan Fotosintesis
                            1. **Reaksi Terang**: Mengubah energi cahaya menjadi ATP dan NADPH
                            2. **Siklus Calvin**: Menggunakan ATP dan NADPH untuk mengubah CO₂ menjadi glukosa
                            
                            ## Faktor yang Mempengaruhi
                            - Intensitas cahaya
                            - Konsentrasi CO₂
                            - Suhu
                            - Ketersediaan air
                            - Jumlah klorofil
                            
                            ## Pentingnya Fotosintesis
                            - Menyediakan makanan bagi seluruh rantai kehidupan
                            - Menghasilkan oksigen untuk respirasi organisme
                            - Mengurangi kadar CO₂ atmosfer (mengurangi efek rumah kaca)
                            """
                            
                            st.session_state.summary_result = summary
                        
                        elif output_type == "module":
                            # In a real app, call the actual Gemini API
                            # For demo, simulate delay and use sample content
                            time.sleep(3)
                            
                            # Sample module (in real app, would be generated by AI)
                            module = """
                            # FOTOSINTESIS: PROSES KIMIA UTAMA DALAM KEHIDUPAN
                            
                            ## 1. Pendahuluan
                            
                            Fotosintesis merupakan salah satu proses metabolisme terpenting di planet Bumi. Proses ini memungkinkan tumbuhan hijau, alga, dan beberapa jenis bakteri untuk mengubah energi cahaya matahari menjadi energi kimia yang tersimpan dalam bentuk glukosa. Fotosintesis bukan hanya penting bagi organisme yang melakukannya, tetapi juga menjadi dasar bagi hampir seluruh kehidupan di Bumi melalui produksi oksigen dan penyediaan makanan.
                            
                            ## 2. Tujuan Pembelajaran
                            
                            Setelah mempelajari modul ini, diharapkan siswa dapat:
                            1. Menjelaskan konsep dasar dan pentingnya fotosintesis
                            2. Mengidentifikasi lokasi dan struktur sel tempat terjadinya fotosintesis
                            3. Mendeskripsikan reaksi kimia yang terjadi dalam fotosintesis
                            4. Membedakan antara reaksi terang dan siklus Calvin
                            5. Menganalisis faktor-faktor yang mempengaruhi laju fotosintesis
                            6. Menjelaskan hubungan fotosintesis dengan kehidupan di Bumi
                            
                            ## 3. Materi
                            
                            ### 3.1 Konsep Dasar Fotosintesis
                            
                            Fotosintesis berasal dari kata "foto" yang berarti cahaya dan "sintesis" yang berarti menyusun. Secara harfiah, fotosintesis berarti menyusun atau membuat sesuatu dengan bantuan cahaya. Dalam konteks biologi, fotosintesis adalah proses pembuatan makanan oleh tumbuhan hijau dan organisme autotrof lainnya menggunakan energi cahaya matahari.
                            
                            Secara umum, fotosintesis dapat dirangkum dalam persamaan kimia berikut:
                            
                            6 CO₂ + 6 H₂O + Energi Cahaya → C₆H₁₂O₆ + 6 O₂
                            
                            Persamaan ini menunjukkan bahwa karbon dioksida (CO₂) dan air (H₂O) diubah menjadi glukosa (C₆H₁₂O₆) dan oksigen (O₂) dengan bantuan energi cahaya matahari. Proses ini bersifat endergonis, artinya membutuhkan energi untuk berlangsung.
                            
                            ### 3.2 Struktur dan Lokasi Fotosintesis
                            
                            Pada tumbuhan tingkat tinggi, fotosintesis terutama terjadi di daun, meskipun semua bagian hijau tumbuhan juga dapat melakukan fotosintesis. Daun memiliki adaptasi struktural yang mendukung efisiensi fotosintesis:
                            
                            1. **Lapisan kutikula** yang tipis dan transparan untuk melindungi daun sekaligus memungkinkan cahaya masuk
                            2. **Epidermis** yang transparan untuk memungkinkan cahaya mencapai jaringan fotosintetik
                            3. **Mesofil palisade** dengan sel-sel yang tersusun rapat dan mengandung banyak kloroplas
                            4. **Mesofil spons** dengan struktur berongga untuk pertukaran gas
                            5. **Stomata** untuk mengatur pertukaran gas (CO₂ masuk dan O₂ keluar)
                            6. **Sistem pembuluh** untuk transportasi air dan hasil fotosintesis
                            
                            Pada tingkat seluler, fotosintesis terjadi di organel khusus yang disebut **kloroplas**. Kloroplas memiliki struktur kompleks dengan komponen-komponen berikut:
                            
                            1. **Membran luar dan dalam** yang membentuk amplop kloroplas
                            2. **Stroma** - matriks semi-cair tempat terjadinya siklus Calvin
                            3. **Tilakoid** - struktur membran berbentuk cakram
                            4. **Grana** - tumpukan tilakoid tempat terjadinya reaksi terang
                            5. **Pigmen fotosintesis** - terutama klorofil a dan b, serta karotenoid
                            
                            ### 3.3 Pigmen Fotosintesis
                            
                            Klorofil adalah pigmen utama dalam fotosintesis yang memberikan warna hijau pada tumbuhan. Ada beberapa jenis klorofil, dengan klorofil a dan b yang paling umum pada tumbuhan tingkat tinggi.
                            
                            1. **Klorofil a** (C₅₅H₇₂O₅N₄Mg) - berwarna biru-hijau, menyerap cahaya merah dan biru-ungu
                            2. **Klorofil b** (C₅₅H₇₀O₆N₄Mg) - berwarna kuning-hijau, menyerap cahaya biru dan oranye-merah
                            
                            Selain klorofil, tumbuhan juga memiliki pigmen aksesori, seperti:
                            
                            1. **Karotenoid** - berwarna oranye-kuning, menyerap cahaya biru-hijau
                            2. **Xantofil** - berwarna kuning, menyerap cahaya biru
                            3. **Fikobilin** - ditemukan pada alga dan sianobakteri
                            
                            Pigmen aksesori memperluas spektrum cahaya yang dapat digunakan untuk fotosintesis dan juga berfungsi melindungi klorofil dari kerusakan oksidatif.
                            
                            ### 3.4 Tahapan Fotosintesis
                            
                            Fotosintesis terdiri dari dua tahap utama: reaksi terang (fotokimia) dan reaksi gelap (siklus Calvin atau reaksi independen cahaya).
                            
                            #### 3.4.1 Reaksi Terang
                            
                            Reaksi terang terjadi pada membran tilakoid kloroplas dan membutuhkan cahaya matahari. Tujuan utama reaksi terang adalah:
                            
                            1. Menghasilkan ATP (Adenosin Trifosfat) melalui fotofosforilasi
                            2. Menghasilkan NADPH melalui reduksi NADP⁺
                            3. Menghasilkan oksigen sebagai produk sampingan
                            
                            Proses ini melibatkan beberapa langkah:
                            
                            1. **Penangkapan cahaya** - Klorofil dan pigmen lainnya menyerap foton, mengakibatkan elektron tereksitasi
                            2. **Transfer elektron** - Elektron berenergi tinggi memasuki rantai transport elektron
                            3. **Fotosistem II** - Mengkatalisasi pemecahan molekul air (fotolisis), melepaskan elektron, ion H⁺, dan O₂
                            4. **Rantai transport elektron** - Elektron mengalir dari PSII ke PSI, menghasilkan gradien proton
                            5. **Fotosistem I** - Menerima elektron dan mentransfernya ke NADP⁺ untuk membentuk NADPH
                            6. **Kemiosmosis** - Gradien H⁺ mendorong sintesis ATP melalui ATP sintase
                            
                            #### 3.4.2 Siklus Calvin (Reaksi Gelap)
                            
                            Siklus Calvin terjadi di stroma kloroplas dan tidak memerlukan cahaya secara langsung, tetapi menggunakan produk dari reaksi terang (ATP dan NADPH). Siklus ini terdiri dari tiga tahap utama:
                            
                            1. **Fiksasi karbon** - CO₂ berikatan dengan ribulosa-1,5-bisfosfat (RuBP) dengan bantuan enzim RuBisCO, membentuk dua molekul 3-fosfogliserat (3-PGA)
                            2. **Reduksi** - 3-PGA diubah menjadi gliseraldehida-3-fosfat (G3P) menggunakan ATP dan NADPH
                            3. **Regenerasi** - Sebagian G3P digunakan untuk membentuk kembali RuBP, memungkinkan siklus berlanjut
                            
                            Untuk setiap 3 molekul CO₂ yang memasuki siklus Calvin, dihasilkan 1 molekul G3P yang dapat digunakan untuk sintesis glukosa (diperlukan 2 G3P untuk 1 glukosa) atau senyawa organik lainnya.
                            
                            ### 3.5 Faktor yang Mempengaruhi Fotosintesis
                            
                            Laju fotosintesis dipengaruhi oleh berbagai faktor lingkungan:
                            
                            1. **Intensitas cahaya** - Meningkatkan laju fotosintesis hingga mencapai titik jenuh cahaya
                            2. **Konsentrasi CO₂** - Membatasi laju fotosintesis pada konsentrasi rendah
                            3. **Suhu** - Memengaruhi aktivitas enzim, optimal pada 25-35°C untuk sebagian besar tumbuhan
                            4. **Ketersediaan air** - Diperlukan sebagai substrat dan untuk menjaga stomata tetap terbuka
                            5. **Ketersediaan nutrisi** - Terutama nitrogen untuk sintesis klorofil dan enzim
                            
                            Faktor-faktor ini saling berinteraksi dan dapat membatasi laju fotosintesis sesuai dengan Hukum Minimum Liebig, yang menyatakan bahwa pertumbuhan dibatasi oleh faktor yang paling rendah jumlahnya.
                            
                            ### 3.6 Variasi dalam Fotosintesis
                            
                            Tumbuhan telah mengembangkan adaptasi untuk meningkatkan efisiensi fotosintesis, terutama dalam kondisi lingkungan yang ekstrem:
                            
                            1. **Tumbuhan C3** - Menggunakan siklus Calvin standar, dengan RuBP sebagai akseptor CO₂ pertama
                            2. **Tumbuhan C4** - Memiliki adaptasi anatomis dan biokimia untuk mengikat CO₂ melalui PEP karboksilase, meningkatkan efisiensi pada suhu tinggi dan kondisi kering
                            3. **Tumbuhan CAM** - Memisahkan fiksasi CO₂ (malam) dan siklus Calvin (siang) secara temporal, adaptasi untuk lingkungan arid
                            
                            ### 3.7 Pentingnya Fotosintesis dalam Ekosistem
                            
                            Fotosintesis memiliki dampak yang luas pada ekosistem global:
                            
                            1. **Dasar rantai makanan** - Menyediakan energi kimia untuk hampir semua kehidupan
                            2. **Produksi oksigen** - Menghasilkan sekitar 50-80% oksigen atmosfer Bumi
                            3. **Siklus karbon** - Mengambil CO₂ dari atmosfer, berperan dalam mitigasi perubahan iklim
                            4. **Sumber bahan bakar fosil** - Hasil akumulasi biomassa fotosintetik selama jutaan tahun
                            
                            ## 4. Rangkuman
                            
                            Fotosintesis adalah proses biokimia fundamental di mana tumbuhan hijau dan organisme fotosintetik lainnya mengubah energi cahaya menjadi energi kimia, menghasilkan karbohidrat dan oksigen dari karbon dioksida dan air. Proses ini terjadi di kloroplas dan melibatkan dua tahap utama: reaksi terang (menghasilkan ATP dan NADPH) dan siklus Calvin (menggunakan ATP dan NADPH untuk membuat gula).
                            
                            Fotosintesis dipengaruhi oleh berbagai faktor lingkungan seperti intensitas cahaya, konsentrasi CO₂, suhu, dan ketersediaan air. Tumbuhan telah mengembangkan berbagai adaptasi (seperti jalur C4 dan CAM) untuk memaksimalkan efisiensi fotosintesis dalam berbagai kondisi lingkungan.
                            
                            Signifikansi fotosintesis melampaui organisme yang melakukannya, membentuk dasar bagi hampir semua jaringan makanan terestrial, menghasilkan oksigen atmosfer, dan berperan penting dalam siklus karbon global serta mitigasi perubahan iklim.
                            
                            ## 5. Latihan
                            
                            1. Jelaskan perbedaan antara reaksi terang dan siklus Calvin dalam proses fotosintesis.
                            
                            2. Gambarkan dan beri label struktur kloroplas, serta jelaskan peran dari tiap komponennya dalam fotosintesis.
                            
                            3. Jika tumbuhan dipindahkan dari lingkungan dengan intensitas cahaya rendah ke lingkungan dengan intensitas cahaya tinggi, bagaimana perubahan ini akan memengaruhi laju fotosintesis? Jelaskan.
                            
                            4. Bandingkan dan kontraskan adaptasi fotosintesis pada tumbuhan C3, C4, dan CAM. Dalam kondisi lingkungan seperti apa masing-masing adaptasi ini paling menguntungkan?
                            
                            5. Diskusikan bagaimana peningkatan konsentrasi CO₂ atmosfer dapat memengaruhi laju fotosintesis global dan implikasinya terhadap produksi pangan di masa depan.
                            
                            6. Hitung jumlah molekul ATP dan NADPH yang dibutuhkan untuk menghasilkan satu molekul glukosa melalui fotosintesis.
                            
                            7. Rancang eksperimen untuk menginvestigasi pengaruh salah satu faktor lingkungan terhadap laju fotosintesis.
                            """
                            
                            st.session_state.module_result = module
                        
                        elif output_type == "quiz":
                            # In a real app, call the actual Gemini API
                            # For demo, simulate delay and use sample content
                            time.sleep(3)
                            
                            # Get quiz settings
                            num_questions = st.session_state.get("quiz_num_questions", 5)
                            difficulty_map = {"Mudah": "Easy", "Sedang": "Medium", "Sulit": "Hard"}
                            difficulty = difficulty_map.get(st.session_state.get("quiz_difficulty", "Sedang"), "Medium")
                            
                            # Sample quiz (in real app, would be generated by AI)
                            quiz = {
                                "quiz": [
                                    {
                                        "question": "Apa yang dimaksud dengan fotosintesis?",
                                        "options": {
                                            "a": "Proses pernapasan pada tumbuhan",
                                            "b": "Proses pembuatan makanan oleh tumbuhan hijau dengan bantuan cahaya matahari",
                                            "c": "Proses perkembangbiakan tumbuhan",
                                            "d": "Proses pengambilan nutrisi dari tanah"
                                        },
                                        "correct_answer": "b",
                                        "correct_text": "Proses pembuatan makanan oleh tumbuhan hijau dengan bantuan cahaya matahari",
                                        "explanation": "Fotosintesis adalah proses di mana tumbuhan hijau membuat makanan mereka sendiri menggunakan cahaya matahari, air, dan karbon dioksida, menghasilkan glukosa dan oksigen."
                                    },
                                    {
                                        "question": "Di bagian sel tumbuhan manakah fotosintesis terjadi?",
                                        "options": {
                                            "a": "Mitokondria",
                                            "b": "Nukleus",
                                            "c": "Kloroplas",
                                            "d": "Ribosom"
                                        },
                                        "correct_answer": "c",
                                        "correct_text": "Kloroplas",
                                        "explanation": "Fotosintesis terjadi di kloroplas, organel sel yang mengandung klorofil dan enzim yang diperlukan untuk reaksi fotosintesis."
                                    },
                                    {
                                        "question": "Manakah dari berikut ini yang merupakan persamaan kimia yang benar untuk fotosintesis?",
                                        "options": {
                                            "a": "6 CO₂ + 6 H₂O + Energi Cahaya → C₆H₁₂O₆ + 6 O₂",
                                            "b": "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + Energi",
                                            "c": "6 CO₂ + 12 H₂O + Energi Cahaya → C₆H₁₂O₆ + 6 H₂O + 6 O₂",
                                            "d": "C₆H₁₂O₆ + 6 H₂O → 6 CO₂ + 12 O₂ + Energi Cahaya"
                                        },
                                        "correct_answer": "a",
                                        "correct_text": "6 CO₂ + 6 H₂O + Energi Cahaya → C₆H₁₂O₆ + 6 O₂",
                                        "explanation": "Persamaan kimia yang benar untuk fotosintesis adalah: 6 CO₂ (karbon dioksida) + 6 H₂O (air) + Energi Cahaya → C₆H₁₂O₆ (glukosa) + 6 O₂ (oksigen)."
                                    },
                                    {
                                        "question": "Apa yang dihasilkan dalam reaksi terang fotosintesis?",
                                        "options": {
                                            "a": "Glukosa dan oksigen",
                                            "b": "Karbon dioksida dan air",
                                            "c": "ATP, NADPH, dan oksigen",
                                            "d": "RuBP dan 3-PGA"
                                        },
                                        "correct_answer": "c",
                                        "correct_text": "ATP, NADPH, dan oksigen",
                                        "explanation": "Reaksi terang menghasilkan ATP (energi) dan NADPH (daya reduksi) yang digunakan dalam siklus Calvin, serta melepaskan oksigen sebagai produk sampingan dari pemecahan molekul air."
                                    },
                                    {
                                        "question": "Faktor apa yang tidak mempengaruhi laju fotosintesis?",
                                        "options": {
                                            "a": "Intensitas cahaya",
                                            "b": "Konsentrasi CO₂",
                                            "c": "Ketersediaan air",
                                            "d": "Kelembaban tanah malam hari"
                                        },
                                        "correct_answer": "d",
                                        "correct_text": "Kelembaban tanah malam hari",
                                        "explanation": "Kelembaban tanah malam hari tidak langsung mempengaruhi laju fotosintesis karena fotosintesis terutama terjadi pada siang hari ketika ada cahaya. Faktor-faktor yang mempengaruhi termasuk intensitas cahaya, konsentrasi CO₂, suhu, dan ketersediaan air saat fotosintesis berlangsung."
                                    }
                                ]
                            }
                            
                            # Create a unique quiz ID
                            quiz_id = str(uuid.uuid4())[:8]
                            
                            # Save to session state
                            st.session_state.quizzes[quiz_id] = {
                                "data": quiz,
                                "material": st.session_state.edited_transcript if st.session_state.process_path == "transcript" else f"Audio: {audio_info['filename']}",
                                "difficulty": difficulty,
                                "num_questions": num_questions,
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            st.session_state.quiz_result = quiz
                        
                        # Update progress bar
                        progress_bar.progress((i + 1) / total_outputs)
                    
                    # Move to results page
                    st.session_state.wizard_step = 4
                    change_page("dashboard")  # Redirect to dashboard to show results
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses: {str(e)}")
    else:
        st.warning("Pilih minimal satu jenis output untuk dilanjutkan.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    back_page = "transcript" if st.session_state.process_path == "transcript" else "upload"
    
    render_wizard_nav_buttons(
        back_callback=lambda: back_to_previous(back_page),
        next_callback=None,  # We're using the generate button instead
        current_step=3,
        total_steps=4
    )

def back_to_previous(page):
    """Go back to previous page"""
    st.session_state.wizard_step -= 1
    change_page(page)