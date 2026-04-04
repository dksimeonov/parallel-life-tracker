from django.urls import path

from milestones.views import (
    MilestoneCreateView,
    MilestoneDeleteView,
    MilestoneListView,
    MilestoneUpdateView
)
urlpatterns = [
    path("life/<slug:slug>/", MilestoneListView.as_view(), name="milestone-list"),
    path("life/<slug:slug>/create/", MilestoneCreateView.as_view(), name="milestone-create"),
    path("<int:pk>/edit/", MilestoneUpdateView.as_view(), name="milestone-edit"),
    path("<int:pk>/delete/", MilestoneDeleteView.as_view(), name="milestone-delete"),
]