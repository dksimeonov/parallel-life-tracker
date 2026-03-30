from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AppUser, Profile


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "display_name",
                "avatar",
                "bio",
                "birth_year",
                "current_city",
                "is_email_verified",
            )
        }),
    )

    list_display = (
        "username",
        "email",
        "display_name",
        "is_staff",
        "is_email_verified",
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "is_profile_public")
