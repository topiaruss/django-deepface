"""Utility functions for django-deepface."""

import logging
import os
from typing import Any

from deepface import DeepFace
from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


def get_deepface_settings() -> dict[str, Any]:
    """Get DeepFace settings from Django settings."""
    return {
        "model_name": getattr(settings, "DEEPFACE_MODEL", "VGG-Face"),
        "detector_backend": getattr(settings, "DEEPFACE_DETECTOR", "retinaface"),
        "enforce_detection": getattr(settings, "DEEPFACE_ENFORCE_DETECTION", True),
        "align": getattr(settings, "DEEPFACE_ALIGN", True),
        "normalization": getattr(settings, "DEEPFACE_NORMALIZATION", "base"),
    }


def process_face_image(image_path: str) -> list | None:
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
        logger.error(f"Error processing face image: {e!s}")
        return None


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
        logger.warning(f"Failed to remove temporary file {file_path}: {e!s}")


def get_max_faces_per_user() -> int:
    """Get maximum number of faces allowed per user."""
    return getattr(settings, "DEEPFACE_MAX_FACES", 4)


def get_similarity_threshold() -> float:
    """Get similarity threshold for face matching."""
    return getattr(settings, "DEEPFACE_THRESHOLD", 0.3)
