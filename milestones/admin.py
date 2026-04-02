from django.contrib import admin
from milestones.models import Milestone


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("title","parallel_life", "status", "progress", "created_by")
    list_filter = ("status",)
    search_fields = ("title", "description")