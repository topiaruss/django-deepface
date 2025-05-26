from pathlib import Path

from deepface import DeepFace
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from django_deepface.models import Identity


class Command(BaseCommand):
    help = (
        "Add face images from a directory structure where subdirectories are usernames"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "directory", type=str, help="Root directory containing user subdirectories"
        )
        parser.add_argument(
            "-c",
            "--clear",
            action="store_true",
            help="Clear all existing Identity records before processing new images",
        )

    def handle(self, *args, **options):
        root_dir = Path(options["directory"])
        if not root_dir.exists():
            raise CommandError(f"Directory {root_dir} does not exist")

        # Clear existing records if requested
        if options["clear"]:
            count = Identity.objects.count()
            Identity.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"Cleared {count} existing Identity records")
            )

        # Valid image extensions
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

        # Process each subdirectory (username)
        for user_dir in root_dir.iterdir():
            if not user_dir.is_dir():
                continue

            username = user_dir.name
            self.stdout.write(f"Processing user directory: {username}")

            # Get or create user
            user, created = User.objects.get_or_create(
                username=username, defaults={"is_active": True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

            # Get existing image count for this user
            existing_count = Identity.objects.filter(user=user).count()
            if existing_count >= 4:
                self.stdout.write(
                    self.style.WARNING(
                        f"User {username} already has maximum number of images (4). Skipping."
                    )
                )
                continue

            # Process images in the directory
            image_number = existing_count + 1
            for image_path in user_dir.iterdir():
                if (
                    not image_path.is_file()
                    or image_path.suffix.lower() not in valid_extensions
                ):
                    continue

                if image_number > 4:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Maximum images reached for {username}. Skipping remaining images."
                        )
                    )
                    break

                try:
                    # Generate face embedding
                    embedding = DeepFace.represent(
                        str(image_path),
                        model_name="VGG-Face",
                        enforce_detection=True,
                        detector_backend="retinaface",
                        align=True,
                        normalization="base",
                    )[0]["embedding"]

                    # Create Identity record
                    with open(image_path, "rb") as f:
                        identity = Identity(
                            user=user, image_number=image_number, embedding=embedding
                        )
                        identity.image.save(image_path.name, File(f), save=False)
                        identity.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added image {image_number} for {username}: {image_path.name}"
                        )
                    )
                    image_number += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error processing {image_path.name} for {username}: {e!s}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Successfully processed all directories"))
