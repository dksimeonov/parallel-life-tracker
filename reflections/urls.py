from django.urls import path
from reflections.views import (
    ReflectionCreateView,
    ReflectionDeleteView,
    ReflectionUpdateView,
)

urlpatterns = [
    path("life/<slug:slug>/create/", ReflectionCreateView.as_view(), name="reflection-create"),
    path("<int:pk>/edit/", ReflectionUpdateView.as_view(), name="reflection-edit"),
    path("<int:pk>/delete/", ReflectionDeleteView.as_view(), name="reflection-delete"),
]