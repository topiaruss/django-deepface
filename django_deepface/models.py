from django.db import models
from pgvector.django import VectorField, HnswIndex
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "faces/user_{0}/{1}".format(instance.user.id, filename)


class Identity(models.Model):
    vector_dimensions = 4096
    image = models.ImageField(upload_to=user_directory_path)
    embedding = VectorField(
        dimensions=vector_dimensions,
        help_text="Embedding vector for the image",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="identities")
    image_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "image_number")
        ordering = ["user__username", "image_number"]
        # indexes = [
        #     HnswIndex(
        #         name="identity_embedding_index",
        #         fields=["embedding"],
        #         opclasses=["vector_l2_ops"],
        #     )
        # ]
        verbose_name = "Identity"
        verbose_name_plural = "Identities"

    def __str__(self):
        return f"{self.user.username}'s face image {self.image_number}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
