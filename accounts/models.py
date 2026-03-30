from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AppUser(AbstractUser):
    display_name = models.CharField(
        max_length=40,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
    )
    birth_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators = [MinValueValidator(1900), MaxValueValidator(2100)],
    )
    current_city = models.CharField(
        max_length=50,
        blank=True,
    )
    is_email_verified = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    occupation = models.CharField(
        max_length=80,
        blank=True,
    )
    personal_motto = models.CharField(
        max_length=80,
        blank=True,
    )
    website = models.URLField(
        blank=True,
    )
    is_profile_public = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"