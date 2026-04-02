from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from parallel_lives.models import ParallelLife


class ReflectionEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reflections",
    )
    parallel_life = models.ForeignKey(
        ParallelLife,
        on_delete=models.CASCADE,
        related_name="reflections",
    )
    title = models.CharField(
        max_length=120,
    )
    content = models.TextField()
    mood_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    is_private = models.BooleanField(
        default= True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user}"


class ComparisonSnapshot(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )
    parallel_life = models.ForeignKey(
        ParallelLife,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )
    current_life_description = models.TextField()
    alternate_life_projection = models.TextField()
    satisfaction_current = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    satisfaction_alternate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Snapshot for {self.parallel_life} by {self.user}"
