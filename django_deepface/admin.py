from django.contrib import admin
from django.utils.html import format_html

from .models import Identity, UserProfile


class IdentityAdmin(admin.ModelAdmin):
    list_display = ("user__username", "image_number", "image", "created_at")
    list_filter = ("user__username", "created_at")
    search_fields = ("user__username",)
    list_per_page = 10
    readonly_fields = ("created_at",)
    fields = ("user", "image_number", "image", "embedding", "created_at")

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "No image"

    display_image.short_description = "Preview"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    def save_model(self, request, obj, form, change):
        # Check if user already has 4 images
        if not change:  # Only check on creation
            existing_count = Identity.objects.filter(user=obj.user).count()
            if existing_count >= 4:
                self.message_user(
                    request,
                    "User already has maximum number of images (4)",
                    level="error",
                )
                return
        super().save_model(request, obj, form, change)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)


admin.site.register(Identity, IdentityAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
