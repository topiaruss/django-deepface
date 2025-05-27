from django.urls import path

from . import views

app_name = "django_deepface"

urlpatterns = [
    path("login/", views.face_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/delete/<int:identity_id>/", views.delete_face, name="delete_face"),
    path("", views.index, name="index"),
]
