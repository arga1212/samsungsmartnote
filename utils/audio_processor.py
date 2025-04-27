import os
import tempfile
import uuid
from datetime import datetime
import shutil
from config import TEMP_FOLDER, ALLOWED_AUDIO_EXTENSIONS, MAX_UPLOAD_SIZE_MB

def is_valid_audio_file(file):
    """
    Check if the file is a valid audio file
    """
    if file is None:
        return False
    
    # Check file extension
    file_ext = file.name.split(".")[-1].lower() if "." in file.name else ""
    if file_ext not in ALLOWED_AUDIO_EXTENSIONS:
        return False
    
    # Check file size
    if file.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:  # Convert MB to bytes
        return False
    
    return True

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to disk
    """
    try:
        if not is_valid_audio_file(uploaded_file):
            return None, None
        
        # Create a unique filename
        file_id = str(uuid.uuid4())[:8]
        file_ext = uploaded_file.name.split(".")[-1] if "." in uploaded_file.name else "wav"
        filename = f"{file_id}.{file_ext}"
        
        # Create full path
        file_path = os.path.join(TEMP_FOLDER, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create file info
        file_info = {
            "id": file_id,
            "filename": uploaded_file.name,
            "path": file_path,
            "size": f"{uploaded_file.size / 1024:.1f} KB",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": "Unknown"  # In a real app, extract this from audio metadata
        }
        
        return file_path, file_info
    
    except Exception as e:
        print(f"Error saving uploaded file: {str(e)}")
        return None, None