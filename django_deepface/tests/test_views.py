import contextlib
import io

import numpy as np
import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from django_deepface.forms import FaceLoginForm
from django_deepface.models import Identity


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")  # nosec


@pytest.fixture
def authenticated_client(client, user):
    client.login(username="testuser", password="testpass123")  # nosec
    return client


@pytest.mark.django_db
class TestProfileView:
    def test_profile_view_get(self, authenticated_client):
        """Test GET request to profile view"""
        url = reverse("django_deepface:profile")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert "face_images" in response.context
        assert len(response.context["face_images"]) == 0

    def test_profile_view_post_valid_image(
        self, authenticated_client, real_face_image, monkeypatch
    ):
        """Test POST request with valid image upload"""

        # Mock DeepFace.represent to return a fake embedding
        def mock_represent(*args, **kwargs):
            return [{"embedding": np.random.rand(Identity.vector_dimensions).tolist()}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        url = reverse("django_deepface:profile")

        # Simply use the test client's post method with files
        response = authenticated_client.post(url, {"image": real_face_image})

        assert response.status_code == 200
        assert Identity.objects.filter(user__username="testuser").count() == 1

        # Check if the file was saved
        identity = Identity.objects.get(user__username="testuser")
        assert identity.image is not None
        assert identity.image_number == 1
        assert identity.user.username == "testuser"

    def test_profile_view_post_max_images(
        self, authenticated_client, real_face_image, monkeypatch, user
    ):
        """Test POST request when user has reached maximum images"""

        # Mock DeepFace.represent
        def mock_represent(*args, **kwargs):
            return [{"embedding": np.random.rand(Identity.vector_dimensions).tolist()}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        # Create 4 existing images
        for i in range(4):
            # Create a fresh file object for each Identity
            test_file = SimpleUploadedFile(
                name=f"test_face_{i}.webp",
                content=real_face_image.read(),
                content_type="image/webp",
            )
            real_face_image.seek(0)  # Reset file pointer

            Identity.objects.create(
                user=user,
                image_number=i + 1,
                image=test_file,
                embedding=np.random.rand(Identity.vector_dimensions).tolist(),
            )

        url = reverse("django_deepface:profile")

        # Create a fresh file for the POST request
        real_face_image.seek(0)  # Reset file pointer
        response = authenticated_client.post(url, {"image": real_face_image})

        assert response.status_code == 200
        assert Identity.objects.filter(user__username="testuser").count() == 4
        assert b"Maximum number of face images reached" in response.content

    def test_profile_view_post_invalid_image(self, authenticated_client):
        """Test POST request with invalid image"""
        url = reverse("django_deepface:profile")

        response = authenticated_client.post(
            url,
            {
                "image": SimpleUploadedFile(
                    name="test.txt", content=b"not an image", content_type="text/plain"
                )
            },
        )

        assert response.status_code == 200
        assert Identity.objects.filter(user__username="testuser").count() == 0

    def test_profile_view_unauthenticated(self, client):
        """Test profile view when user is not authenticated"""
        url = reverse("django_deepface:profile")
        response = client.get(url)

        assert response.status_code == 302  # Redirects to login


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_view_authenticated(self, authenticated_client):
        """Test logout when user is authenticated"""
        url = reverse("django_deepface:logout")
        response = authenticated_client.get(url)

        assert response.status_code == 302  # Redirects to login
        assert response.url == reverse("django_deepface:login")

        # Check if user is actually logged out
        response = authenticated_client.get(reverse("django_deepface:profile"))
        assert response.status_code == 302  # Should redirect to login

    def test_logout_view_unauthenticated(self, client):
        """Test logout when user is not authenticated"""
        url = reverse("django_deepface:logout")
        response = client.get(url)

        assert response.status_code == 302  # Redirects to login
        assert response.url == reverse("django_deepface:login")


@pytest.mark.django_db
class TestFaceLoginView:
    def test_face_login_get(self, client):
        """Test GET request to face login view"""
        url = reverse("django_deepface:login")
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert isinstance(response.context["form"], FaceLoginForm)

    def test_face_login_password_success(self, client, user):
        """Test successful password login"""
        url = reverse("django_deepface:login")
        response = client.post(
            url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )

        assert response.status_code == 302  # Redirects to index
        assert response.url == reverse("django_deepface:index")

    def test_face_login_password_invalid(self, client):
        """Test invalid password login"""
        url = reverse("django_deepface:login")
        response = client.post(
            url,
            {
                "username": "testuser",
                "password": "wrongpass",
            },
        )

        assert response.status_code == 200
        form = response.context["form"]
        assert form.errors["__all__"]  # Check for non-field errors
        assert any(
            "username and password" in str(error) for error in form.errors["__all__"]
        )

    def test_face_login_face_success(self, client, user, real_face_image, monkeypatch):
        """Test successful face login"""
        # Create an identity for the user with a specific embedding
        stored_embedding = np.random.rand(Identity.vector_dimensions).tolist()

        Identity.objects.create(
            user=user,
            image_number=1,
            image=real_face_image,
            embedding=stored_embedding,
        )

        # Mock DeepFace.represent to return the same embedding
        def mock_represent(*args, **kwargs):
            return [{"embedding": stored_embedding}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        # Mock os.remove to avoid file system errors
        def mock_remove(*args, **kwargs):
            pass

        monkeypatch.setattr("os.remove", mock_remove)

        # Mock os.makedirs to avoid file system errors
        def mock_makedirs(*args, **kwargs):
            pass

        monkeypatch.setattr("os.makedirs", mock_makedirs)

        # Mock default_storage.open to avoid file system errors
        @contextlib.contextmanager
        def mock_storage_open(*args, **kwargs):
            yield io.BytesIO()

        monkeypatch.setattr(
            "django.core.files.storage.default_storage.open", mock_storage_open
        )

        # Reset the file pointer before sending
        real_face_image.seek(0)

        url = reverse("django_deepface:login")
        response = client.post(
            url,
            {
                "username": "testuser",
                "use_face_login": "on",  # "on" is correct for checkboxes
                "face_image": real_face_image,
            },
        )

        # Check for redirect
        assert response.status_code == 302
        assert response.url == reverse("django_deepface:index")

    def test_face_login_face_no_match(self, client, user, real_face_image, monkeypatch):
        """Test face login with no matching face"""
        # Create identity record with a specific embedding
        stored_embedding = np.ones(Identity.vector_dimensions).tolist()  # All ones

        Identity.objects.create(
            user=user,
            image_number=1,
            image=real_face_image,
            embedding=stored_embedding,
        )

        # Mock DeepFace.represent to return a very different embedding
        def mock_represent(*args, **kwargs):
            # Return all zeros - maximally different from all ones
            return [{"embedding": np.zeros(Identity.vector_dimensions).tolist()}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        # Mock os.remove to avoid file system errors
        def mock_remove(*args, **kwargs):
            pass

        monkeypatch.setattr("os.remove", mock_remove)

        # Mock os.makedirs to avoid file system errors
        def mock_makedirs(*args, **kwargs):
            pass

        monkeypatch.setattr("os.makedirs", mock_makedirs)

        # Mock default_storage.open to avoid file system errors
        @contextlib.contextmanager
        def mock_storage_open(*args, **kwargs):
            yield io.BytesIO()

        monkeypatch.setattr(
            "django.core.files.storage.default_storage.open", mock_storage_open
        )

        # Reset the file pointer before sending
        real_face_image.seek(0)

        url = reverse("django_deepface:login")
        response = client.post(
            url,
            {
                "username": "testuser",
                "use_face_login": "on",  # "on" is correct for checkboxes
                "face_image": real_face_image,
            },
            follow=True,
        )  # Follow redirects to see messages

        assert response.status_code == 200
        # Check for error message in the messages
        messages = list(response.context["messages"])
        assert any("Face not recognized" in str(msg) for msg in messages)

    def test_face_login_face_error(self, client, user, real_face_image, monkeypatch):
        """Test face login with DeepFace error"""

        def mock_represent(*args, **kwargs):
            raise Exception("Face detection failed")

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        # Mock os.remove to avoid file system errors
        def mock_remove(*args, **kwargs):
            pass

        monkeypatch.setattr("os.remove", mock_remove)

        # Mock os.makedirs to avoid file system errors
        def mock_makedirs(*args, **kwargs):
            pass

        monkeypatch.setattr("os.makedirs", mock_makedirs)

        # Mock default_storage.open to avoid file system errors
        @contextlib.contextmanager
        def mock_storage_open(*args, **kwargs):
            yield io.BytesIO()

        monkeypatch.setattr(
            "django.core.files.storage.default_storage.open", mock_storage_open
        )

        # Reset the file pointer before sending
        real_face_image.seek(0)

        url = reverse("django_deepface:login")
        response = client.post(
            url,
            {
                "username": "testuser",
                "use_face_login": "on",  # "on" is correct for checkboxes
                "face_image": real_face_image,
            },
            follow=True,
        )  # Follow redirects to see messages

        assert response.status_code == 200
        # Check for error message in the messages
        messages = list(response.context["messages"])
        assert any("Error processing face" in str(msg) for msg in messages)


@pytest.mark.django_db
class TestDeleteFaceView:
    def test_delete_face_success(
        self, authenticated_client, user, real_face_image, monkeypatch
    ):
        """Test successful face deletion"""

        # Create an identity for the user
        def mock_represent(*args, **kwargs):
            return [{"embedding": np.random.rand(Identity.vector_dimensions).tolist()}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        identity = Identity.objects.create(
            user=user,
            image_number=1,
            image=real_face_image,
            embedding=np.random.rand(Identity.vector_dimensions).tolist(),
        )

        url = reverse("django_deepface:delete_face", args=[identity.id])
        response = authenticated_client.post(url)

        assert response.status_code == 302  # Redirects to profile
        assert response.url == reverse("django_deepface:profile")
        assert not Identity.objects.filter(id=identity.id).exists()

    def test_delete_face_unauthorized(self, client, user, real_face_image, monkeypatch):
        """Test face deletion by unauthorized user"""

        # Create an identity for another user
        def mock_represent(*args, **kwargs):
            return [{"embedding": np.random.rand(Identity.vector_dimensions).tolist()}]

        monkeypatch.setattr("deepface.DeepFace.represent", mock_represent)

        identity = Identity.objects.create(
            user=user,
            image_number=1,
            image=real_face_image,
            embedding=np.random.rand(Identity.vector_dimensions).tolist(),
        )

        url = reverse("django_deepface:delete_face", args=[identity.id])
        response = client.post(url)

        assert response.status_code == 302  # Redirects to login
        assert Identity.objects.filter(
            id=identity.id
        ).exists()  # Identity should still exist

    def test_delete_face_nonexistent(self, authenticated_client):
        """Test deletion of nonexistent face"""
        url = reverse("django_deepface:delete_face", args=[999])
        response = authenticated_client.post(url)

        assert response.status_code == 404
