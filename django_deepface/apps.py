"""Django DeepFace application configuration."""

from django.apps import AppConfig


class DjangoDeepfaceConfig(AppConfig):
    """Configuration for the Django DeepFace application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_deepface"
    verbose_name = "Django DeepFace"

    def ready(self):
        """Initialize app settings when Django starts."""
        from django.conf import settings

        # Set default settings if not provided
        if not hasattr(settings, "DEEPFACE_MAX_FACES"):
            settings.DEEPFACE_MAX_FACES = 4

        if not hasattr(settings, "DEEPFACE_MODEL"):
            settings.DEEPFACE_MODEL = "VGG-Face"

        if not hasattr(settings, "DEEPFACE_DETECTOR"):
            settings.DEEPFACE_DETECTOR = "retinaface"

        if not hasattr(settings, "DEEPFACE_THRESHOLD"):
            settings.DEEPFACE_THRESHOLD = 0.3

        if not hasattr(settings, "DEEPFACE_ENFORCE_DETECTION"):
            settings.DEEPFACE_ENFORCE_DETECTION = True

        if not hasattr(settings, "DEEPFACE_ALIGN"):
            settings.DEEPFACE_ALIGN = True

        if not hasattr(settings, "DEEPFACE_NORMALIZATION"):
            settings.DEEPFACE_NORMALIZATION = "base"

        # Authentication redirect settings
        if not hasattr(settings, "DEEPFACE_LOGIN_REDIRECT_URL"):
            settings.DEEPFACE_LOGIN_REDIRECT_URL = "index"

        if not hasattr(settings, "DEEPFACE_LOGOUT_REDIRECT_URL"):
            settings.DEEPFACE_LOGOUT_REDIRECT_URL = "django_deepface:login"
