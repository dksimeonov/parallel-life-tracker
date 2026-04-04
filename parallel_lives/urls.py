from django.urls import path

from parallel_lives.views import (
    ParallelLifeCreateView,
    ParallelLifeDeleteView,
    ParallelLifeDetailView,
    ParallelLifeListView,
    ParallelLifeUpdateView,
)
urlpatterns = [
    path("", ParallelLifeListView.as_view(), name="parallel-lives-list"),
    path("create/", ParallelLifeCreateView.as_view(), name="parallel-life-create"),
    path("<slug:slug>/", ParallelLifeDetailView.as_view(), name="parallel-life-detail"),
    path("<slug:slug>/edit/", ParallelLifeUpdateView.as_view(), name="parallel-life-edit"),
    path("<slug:slug>/delete/", ParallelLifeDeleteView.as_view(), name="parallel-life-delete"),
]