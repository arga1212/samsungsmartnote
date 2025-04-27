import google.generativeai as genai
import re
import json
import os
from config import (
    GOOGLE_API_KEY, 
    GEMINI_MODEL, 
    GEMINI_CONFIG_SUMMARY, 
    GEMINI_CONFIG_TRANSCRIBE,
    GEMINI_CONFIG_MODULE,
    GEMINI_CONFIG_QUIZ
)

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def generate_transcript(audio_file_path):
    """
    Generate transcript from audio file using Gemini AI
    
    Parameters:
    ----------
    audio_file_path : str
        Path to the audio file
        
    Returns:
    -------
    str
        Transcripted text
    """
    try:
        # Check if file exists
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"File not found: {audio_file_path}")
        
        # Upload the audio file to Gemini
        audio_file = genai.upload_file(path=audio_file_path)
        
        # Initialize model with appropriate configuration
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=GEMINI_CONFIG_TRANSCRIBE
        )
        
        # Generate transcript
        response = model.generate_content([
            {"role": "user", "parts": ["Transkripsi audio ini kata per kata dengan akurat"]},
            {"role": "user", "parts": [audio_file]}
        ])
        
        return response.text
    
    except Exception as e:
        print(f"Error generating transcript: {str(e)}")
        raise e

def generate_summary(content, is_audio=False, audio_file_path=None):
    """
    Generate summary from content (text or audio)
    
    Parameters:
    ----------
    content : str
        Text content to summarize or audio file path
    is_audio : bool
        Whether the content is an audio file path
    audio_file_path : str
        Path to the audio file (if is_audio is True)
        
    Returns:
    -------
    str
        Summary text
    """
    try:
        # Initialize model with appropriate configuration
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=GEMINI_CONFIG_SUMMARY
        )
        
        if is_audio:
            if not audio_file_path or not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Upload audio file
            audio_file = genai.upload_file(path=audio_file_path)
            
            # Generate summary from audio
            response = model.generate_content([
                {"role": "user", "parts": ["Ringkas audio ini dan berikan poin-poin penting yang harus diketahui dalam format markdown rapi"]},
                {"role": "user", "parts": [audio_file]}
            ])
        else:
            # Generate summary from text
            response = model.generate_content([
                {"role": "user", "parts": ["Ringkas teks berikut dan berikan poin-poin penting yang harus diketahui dalam format markdown rapi"]},
                {"role": "user", "parts": [content]}
            ])
        
        return response.text
    
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        raise e

def generate_module(content, is_audio=False, audio_file_path=None):
    """
    Generate learning module from content (text or audio)
    
    Parameters:
    ----------
    content : str
        Text content to process or audio file path
    is_audio : bool
        Whether the content is an audio file path
    audio_file_path : str
        Path to the audio file (if is_audio is True)
        
    Returns:
    -------
    str
        Module text in markdown format
    """
    try:
        # Initialize model with appropriate configuration
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=GEMINI_CONFIG_MODULE
        )
        
        module_prompt = """
        Buatkan modul pelajaran yang lengkap dan terstruktur berdasarkan teks atau audio berikut.

        Kriteria:
        - Gunakan gaya bahasa buku pelajaran yang formal namun mudah dipahami
        - Sertakan struktur:
          1. Pendahuluan
          2. Tujuan Pembelajaran
          3. Materi
             3.1 Sub-bab 1
             3.2 Sub-bab 2
             ...
          4. Rangkuman
          5. Latihan (tanpa jawaban)
        - Gunakan paragraf panjang dan penjelasan mendalam
        - Format dalam markdown yang rapi
        - Langsung mulai dengan heading utama modul (tanpa kalimat pembuka)
        """
        
        if is_audio:
            if not audio_file_path or not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Upload audio file
            audio_file = genai.upload_file(path=audio_file_path)
            
            # Generate module from audio
            response = model.generate_content([
                {"role": "user", "parts": [module_prompt]},
                {"role": "user", "parts": [audio_file]}
            ])
        else:
            # Generate module from text
            response = model.generate_content([
                {"role": "user", "parts": [module_prompt]},
                {"role": "user", "parts": [content]}
            ])
        
        return response.text
    
    except Exception as e:
        print(f"Error generating module: {str(e)}")
        raise e

def generate_quiz(content, difficulty="Medium", num_questions=5, is_audio=False, audio_file_path=None):
    """
    Generate quiz from content (text or audio)
    
    Parameters:
    ----------
    content : str
        Text content to process or audio file path
    difficulty : str
        Difficulty level (Easy, Medium, Hard)
    num_questions : int
        Number of questions to generate
    is_audio : bool
        Whether the content is an audio file path
    audio_file_path : str
        Path to the audio file (if is_audio is True)
        
    Returns:
    -------
    dict
        Quiz data in JSON format
    """
    try:
        # Initialize model with appropriate configuration
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=GEMINI_CONFIG_QUIZ
        )
        
        quiz_prompt = f"""
        Buat {num_questions} soal kuis pilihan ganda berdasarkan konten berikut:

        *Format Output (HARUS JSON):*
        {{
            "quiz": [
                {{
                    "question": "pertanyaan",
                    "options": {{
                        "a": "teks opsi a",
                        "b": "teks opsi b", 
                        "c": "teks opsi c",
                        "d": "teks opsi d"
                    }},
                    "correct_answer": "a",  # Pilih dari a/b/c/d
                    "correct_text": "teks opsi a",  # Teks jawaban benar yang sesuai dengan salah satu opsi
                    "explanation": "penjelasan terkait jawaban benar"
                }}
            ]
        }}
        
        *Aturan:*
        1. Tingkat kesulitan: {difficulty}
        2. Pastikan 'correct_text' sama persis dengan salah satu opsi
        3. Format output HARUS JSON dan valid, tanpa komentar atau teks tambahan
        4. Hindari pertanyaan trivial atau terlalu umum
        5. Gunakan pertanyaan yang menguji pemahaman konsep
        """
        
        if is_audio:
            if not audio_file_path or not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Upload audio file
            audio_file = genai.upload_file(path=audio_file_path)
            
            # Generate quiz from audio
            response = model.generate_content([
                {"role": "user", "parts": [quiz_prompt]},
                {"role": "user", "parts": [audio_file]}
            ])
        else:
            # Generate quiz from text
            response = model.generate_content([
                {"role": "user", "parts": [quiz_prompt]},
                {"role": "user", "parts": [content]}
            ])
        
        # Extract JSON from response
        json_str = re.search(r'\{[\s\S]*\}', response.text)
        
        if json_str:
            json_str = json_str.group()
            quiz_data = json.loads(json_str)
            
            # Validate the quiz data
            for question in quiz_data["quiz"]:
                if question["correct_answer"] not in ['a', 'b', 'c', 'd']:
                    raise ValueError("Jawaban benar harus salah satu dari opsi: a, b, c, d")
                if question["correct_text"] != question["options"].get(question["correct_answer"]):
                    raise ValueError("Teks jawaban benar tidak cocok dengan opsi yang dipilih")
            
            return quiz_data
        else:
            raise ValueError("Tidak ditemukan format JSON yang valid dalam response.")
    
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        raise e