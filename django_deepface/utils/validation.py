"""Validation utilities for django-deepface."""
from typing import List, Optional
import numpy as np
from django.core.exceptions import ValidationError
from .face_processing import get_similarity_threshold


def validate_face_embedding(embedding: List[float]) -> None:
    """
    Validate face embedding format and values.
    
    Args:
        embedding: Face embedding vector
        
    Raises:
        ValidationError: If embedding is invalid
    """
    if not embedding:
        raise ValidationError("Empty face embedding")
    
    if not isinstance(embedding, (list, np.ndarray)):
        raise ValidationError("Face embedding must be a list or numpy array")
    
    if len(embedding) != 512:  # VGG-Face embedding size
        raise ValidationError(f"Invalid embedding size: {len(embedding)}")


def validate_similarity_score(score: float) -> None:
    """
    Validate similarity score.
    
    Args:
        score: Similarity score between 0 and 1
        
    Raises:
        ValidationError: If score is invalid
    """
    if not isinstance(score, (int, float)):
        raise ValidationError("Similarity score must be a number")
    
    if not 0 <= score <= 1:
        raise ValidationError("Similarity score must be between 0 and 1")


def is_match(similarity_score: float, threshold: Optional[float] = None) -> bool:
    """
    Check if similarity score indicates a match.
    
    Args:
        similarity_score: Score to check
        threshold: Optional custom threshold
        
    Returns:
        True if score is above threshold
    """
    threshold = threshold or get_similarity_threshold()
    return similarity_score >= threshold 