import requests
import os
import json
from config import FLASK_SERVER_URL

def get_file_list():
    """
    Get list of files from Flask server
    
    Returns:
    -------
    list
        List of file information dictionaries
    """
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/files")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting file list: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"Error communicating with Flask server: {str(e)}")
        return []

def download_file(filename, save_path=None):
    """
    Download file from Flask server
    
    Parameters:
    ----------
    filename : str
        Name of the file to download
    save_path : str
        Path to save the file (if None, returns file content)
        
    Returns:
    -------
    bytes or str
        File content (bytes) or path to saved file (str)
    """
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/uploads/{filename}", stream=True)
        
        if response.status_code == 200:
            if save_path:
                # Save to file
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return save_path
            else:
                # Return content
                return response.content
        else:
            print(f"Error downloading file: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return None

def upload_file(file_path, filename=None):
    """
    Upload file to Flask server
    
    Parameters:
    ----------
    file_path : str
        Path to the file to upload
    filename : str
        Custom filename (if None, uses original filename)
        
    Returns:
    -------
    bool
        Success status
    """
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        # If no custom filename provided, use original
        if not filename:
            filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            response = requests.post(f"{FLASK_SERVER_URL}/upload", files=files)
        
        if response.status_code == 200:
            return True
        else:
            print(f"Error uploading file: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False

def delete_file(filename):
    """
    Delete file from Flask server
    
    Parameters:
    ----------
    filename : str
        Name of the file to delete
        
    Returns:
    -------
    bool
        Success status
    """
    try:
        response = requests.delete(f"{FLASK_SERVER_URL}/uploads/{filename}")
        
        if response.status_code == 200:
            return True
        else:
            print(f"Error deleting file: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False

def check_server_status():
    """
    Check if Flask server is online
    
    Returns:
    -------
    bool
        Server status (True = online)
    """
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/status")
        return response.status_code == 200
    except:
        return False