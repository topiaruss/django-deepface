from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
import os
from deepface import DeepFace
import numpy as np
from .forms import FaceLoginForm, FaceImageUploadForm
from .models import UserProfile, Identity
from pgvector.django import CosineDistance


def face_login(request):
    if request.method == "POST":
        form = FaceLoginForm(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            if form.cleaned_data.get("use_face_login") and request.FILES.get(
                "face_image"
            ):
                # Process face login
                face_image = request.FILES["face_image"]
                temp_path = os.path.join(settings.MEDIA_ROOT, "temp", face_image.name)
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)

                with default_storage.open(temp_path, "wb+") as destination:
                    for chunk in face_image.chunks():
                        destination.write(chunk)

                try:
                    # Get face embedding using DeepFace
                    login_embedding = DeepFace.represent(
                        temp_path,
                        model_name="VGG-Face",
                        enforce_detection=True,
                        detector_backend="retinaface",
                        align=True,
                        normalization="base",
                    )[0]["embedding"]

                    # Query using pgvector's cosine distance
                    matches = Identity.objects.annotate(
                        distance=CosineDistance("embedding", login_embedding)
                    ).order_by("distance")
                    dat = [(m.distance, m.image.name) for m in matches]
                    for d in dat:
                        print(d)
                    best_match = matches.first()
                    if best_match:
                        # threshold for cosine similarity (lower is more similar)
                        if best_match.distance < 0.3:  # Cosine similarity threshold
                            user = best_match.user
                            login(request, user)
                            messages.success(request, "Face recognition successful!")
                            # Clean up temp file
                            os.remove(temp_path)
                            return redirect("index")
                        else:
                            messages.error(
                                request,
                                "Face not recognized. Please try again or use password login.",
                            )
                    else:
                        messages.error(
                            request,
                            "No face recognized. Please try again or use password login.",
                        )
                    # Clean up temp file
                    os.remove(temp_path)

                except Exception as e:
                    messages.error(request, f"Error processing face: {str(e)}")
                    # Clean up temp file
                    os.remove(temp_path)

            else:
                # Regular password login
                user = form.get_user()
                login(request, user)
                return redirect("index")
    else:
        form = FaceLoginForm()

    return render(request, "django_deepface/login.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = FaceImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the next available image number
            next_number = Identity.objects.filter(user=request.user).count() + 1
            if next_number <= 4:
                try:
                    # Create Identity record with the uploaded image
                    identity = form.save(commit=False)
                    identity.user = request.user
                    identity.image_number = next_number
                    identity.save()

                    # Generate face embedding using DeepFace
                    embedding = DeepFace.represent(
                        identity.image.path,
                        model_name="VGG-Face",
                        enforce_detection=True,
                        detector_backend="retinaface",
                        align=True,
                        normalization="base",
                    )[0]["embedding"]

                    identity.embedding = embedding

                    identity.save(update_fields=["embedding"])
                    messages.success(request, "Face image uploaded successfully!")
                except Exception as e:
                    messages.error(request, f"Error processing face: {str(e)}")
            else:
                messages.error(request, "Maximum number of face images reached (4)")
        else:
            messages.error(request, f"Form errors: {form.errors}")
    else:
        form = FaceImageUploadForm()

    # Get existing face images
    face_images = Identity.objects.filter(user=request.user)

    return render(
        request,
        "django_deepface/profile.html",
        {"form": form, "face_images": face_images},
    )


@login_required
def delete_face(request, identity_id):
    """Delete a face image and reorder remaining images"""
    identity = get_object_or_404(Identity, id=identity_id, user=request.user)

    # Delete the image file
    if identity.image:
        identity.image.delete()

    # Delete the identity record
    identity.delete()

    # Reorder remaining images
    remaining_images = Identity.objects.filter(user=request.user).order_by(
        "image_number"
    )
    for i, img in enumerate(remaining_images, 1):
        if img.image_number != i:
            img.image_number = i
            img.save(update_fields=["image_number"])

    messages.success(request, "Face image deleted successfully!")
    return redirect("django_deepface:profile")


def logout_view(request):
    """Log out the user and redirect to login page"""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("django_deepface:login")
