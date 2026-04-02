from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from parallel_lives.models import ParallelLife


class Milestone(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    parallel_life = models.ForeignKey(
        ParallelLife,
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    title = models.CharField(
        max_length=120,
    )
    description = models.TextField()
    target_date = models.DateField(
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    progress = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text= "Progress percentage from 0 to 100.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_milestones",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.parallel_life})"


