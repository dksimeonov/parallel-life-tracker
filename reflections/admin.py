from django.contrib import admin
from reflections.models import ReflectionEntry, ComparisonSnapshot


@admin.register(ReflectionEntry)
class ReflectionEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "parallel_life", "mood_score", "is_private")
    list_filter = ("is_private",)


@admin.register(ComparisonSnapshot)
class ComparisonSnapshotAdmin(admin.ModelAdmin):
    list_display = ("parallel_life", "user", "satisfaction_current", "satisfaction_alternate")
