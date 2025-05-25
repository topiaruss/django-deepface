"""Face processing utilities for django-deepface."""
from typing import Optional, Dict, Any
from django.conf import settings
from deepface import DeepFace
import logging

logger = logging.getLogger(__name__)


def get_deepface_settings() -> Dict[str, Any]:
    """Get DeepFace settings from Django settings."""
    return {
        'model_name': getattr(settings, 'DEEPFACE_MODEL', 'VGG-Face'),
        'detector_backend': getattr(settings, 'DEEPFACE_DETECTOR', 'retinaface'),
        'enforce_detection': getattr(settings, 'DEEPFACE_ENFORCE_DETECTION', True),
        'align': getattr(settings, 'DEEPFACE_ALIGN', True),
        'normalization': getattr(settings, 'DEEPFACE_NORMALIZATION', 'base'),
    }


def process_face_image(image_path: str) -> Optional[list]:
    """
    Process a face image and return embeddings.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        List of embeddings or None if processing fails
    """
    try:
        deepface_settings = get_deepface_settings()
        embeddings = DeepFace.represent(image_path, **deepface_settings)
        return embeddings[0]["embedding"] if embeddings else None
    except Exception as e:
        logger.error(f"Error processing face image: {str(e)}")
        return None


def get_max_faces_per_user() -> int:
    """Get maximum number of faces allowed per user."""
    return getattr(settings, 'DEEPFACE_MAX_FACES', 4)


def get_similarity_threshold() -> float:
    """Get similarity threshold for face matching."""
    return getattr(settings, 'DEEPFACE_THRESHOLD', 0.3) 