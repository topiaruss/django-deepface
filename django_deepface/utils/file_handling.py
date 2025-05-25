"""File handling utilities for django-deepface."""
import os
from django.conf import settings
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)


def save_temp_file(uploaded_file) -> str:
    """
    Save uploaded file to temporary location.
    
    Args:
        uploaded_file: Django UploadedFile instance
        
    Returns:
        Path to saved temporary file
    """
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp", uploaded_file.name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    
    with default_storage.open(temp_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
            
    return temp_path


def cleanup_temp_file(file_path: str) -> None:
    """
    Remove temporary file.
    
    Args:
        file_path: Path to file to remove
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}") 