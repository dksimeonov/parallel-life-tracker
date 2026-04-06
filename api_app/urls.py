from django.urls import path

from api_app.views import (
    ParallelLifeApiCreateView,
    ParallelLifeApiDetailView,
    ParallelLifeApiListView,
)

urlpatterns = [
    path("parallel-lives/", ParallelLifeApiListView.as_view(), name="api-parallel-life-list"),
    path("parallel-lives/<int:pk>/", ParallelLifeApiDetailView.as_view(), name="api-parallel-life-detail"),
    path("parallel-lives/create/", ParallelLifeApiCreateView.as_view(), name="api-parallel-life-create"),
]