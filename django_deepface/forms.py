from typing import ClassVar

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import FileExtensionValidator

from .models import Identity


class FaceLoginForm(AuthenticationForm):
    use_face_login = forms.BooleanField(required=False)
    face_image = forms.FileField(required=False)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,  # Make password optional
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Please provide a username.")
        return username

    def clean_password(self):
        # Skip password validation if using face login
        # Check raw data since cleaned_data might not have use_face_login yet
        if self.data.get("use_face_login"):
            return self.cleaned_data.get("password")
        # For traditional login, ensure password is provided
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Please provide a password.")
        return password

    def clean(self):
        # Don't call super().clean() to prevent parent validation
        cleaned_data = self.cleaned_data
        use_face_login = cleaned_data.get("use_face_login")
        face_image = cleaned_data.get("face_image")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # If using face login, skip password validation
        if use_face_login:
            if not face_image:
                raise forms.ValidationError(
                    "Please capture a face image for face login."
                )
            # Don't validate password for face login
            return cleaned_data

        # Traditional login validation
        if not password:
            raise forms.ValidationError("Please provide a password.")

        # Authenticate user
        self.user_cache = authenticate(
            self.request, username=username, password=password
        )
        if self.user_cache is None:
            raise forms.ValidationError("Please enter a correct username and password.")
        else:
            self.confirm_login_allowed(self.user_cache)

        return cleaned_data

    def get_user(self):
        return self.user_cache

    def confirm_login_allowed(self, user):
        # Override to prevent parent class from adding validation errors
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code="inactive",
            )


class FaceImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
        help_text="Upload a clear face image",
    )

    class Meta:
        model: ClassVar = Identity
        fields: ClassVar = ["image"]
