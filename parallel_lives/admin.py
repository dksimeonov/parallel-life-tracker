from django.contrib import admin

from parallel_lives.models import DivergenceDecision, LifeDomain, ParallelLife, PathFollow


@admin.register(LifeDomain)
class LifeDomainAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ParallelLife)
class ParallelLifeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "visibility", "status", "realism_score", "created_at")
    list_filter = ("visibility", "status", "domains")
    search_fields = ("title", "starting_choice", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("domains",)


@admin.register(DivergenceDecision)
class DivergenceDecisionAdmin(admin.ModelAdmin):
    list_display = ("decision_title", "parallel_life", "emotional_weight", "created_at")


@admin.register(PathFollow)
class PathFollowAdmin(admin.ModelAdmin):
    list_display = ("user", "parallel_life", "created_at")
