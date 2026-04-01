from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse


class LifeDomain(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    icon_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: briefcase, heart, globe, book",
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ParallelLife(models.Model):
    class VisibilityChoices(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"
        UNLISTED = "unlisted", "Unlisted"

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parallel_lives",
    )
    title = models.CharField(
        max_length=120,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    divergence_date = models.DateField()
    starting_choice = models.CharField(
        max_length = 200,
        help_text = "The key decision that changed this life path.",
    )
    summary = models.TextField()
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PRIVATE,
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    realism_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rate how realistic this path feels from 1 to 10.",
    )
    domains = models.ManyToManyField(
        LifeDomain,
        related_name="parallel_lives",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if len(self.title.strip()) < 5:
            raise ValidationError({"title": "Title must be at least 5 characters long."})

        if len(self.title.strip()) < 20:
            raise ValidationError({"summary": "Summary must be at least 20 characters long."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ParallelLife.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return self.title


class DivergenceDecision(models.Model):
    parallel_life = models.OneToOneField(
        ParallelLife,
        on_delete=models.CASCADE,
        related_name="decision",
    )
    decision_title = models.CharField(
        max_length=120,
    )
    real_world_path = models.TextField()
    alternate_path = models.TextField()
    reasoning = models.TextField()
    emotional_weight = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="How emotionally important is this divergence?",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Decision for {self.parallel_life.title}"


class PathFollow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_paths",
    )
    parallel_life = models.ForeignKey(
        ParallelLife,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "parallel_life"],
                name="unique_user_path_follow",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} follows {self.parallel_life.title}"














