from django.db.models import Q
from rest_framework import generics, permissions

from api_app.serializers import ParallelLifeSerializer
from parallel_lives.models import ParallelLife


class ParallelLifeApiListView(generics.ListAPIView):
    serializer_class = ParallelLifeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = ParallelLife.objects.select_related("owner").prefetch_related("domains")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(visibility=ParallelLife.VisibilityChoices.PUBLIC) |
                Q(owner=self.request.user)
            ).distinct()

        return queryset.filter(
            visibility=ParallelLife.VisibilityChoices.PUBLIC
        ).distinct()


class ParallelLifeApiDetailView(generics.RetrieveAPIView):
    serializer_class = ParallelLifeSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

    def get_queryset(self):
        queryset = ParallelLife.objects.select_related("owner").prefetch_related("domains")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(visibility=ParallelLife.VisibilityChoices.PUBLIC) |
                Q(owner=self.request.user)
            ).distinct()

        return queryset.filter(
            visibility=ParallelLife.VisibilityChoices.PUBLIC
        ).distinct()


class ParallelLifeApiCreateView(generics.CreateAPIView):
    serializer_class = ParallelLifeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
