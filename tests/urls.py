"""
URL configuration for tests.
"""

from django.urls import path, include
from django.views.generic import TemplateView

# Create a simple index view for tests
index_view = TemplateView.as_view(template_name="django_deepface/index.html")

urlpatterns = [
    path("", index_view, name="index"),
    path("", include("django_deepface.urls")),
]
