from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from parallel_lives.forms import ParallelLifeForm
from parallel_lives.models import ParallelLife


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ParallelLifeListView(ListView):
    model = ParallelLife
    template_name = "parallel_lives/parallel_lives_list.html"
    context_object_name = "parallel_lives"
    paginate_by = 6

    def get_queryset(self):
        queryset = ParallelLife.objects.select_related("owner").prefetch_related("domains")

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(visibility=ParallelLife.VisibilityChoices.PUBLIC) |
                Q(owner=self.request.user)
            )
        else:
            queryset = queryset.filter(
                visibility=ParallelLife.VisibilityChoices.PUBLIC
            )

        queryset = queryset.distinct()

        query = self.request.GET.get("q")
        visibility = self.request.GET.get("visibility")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(starting_choice__icontains=query)
            )

        if visibility in {"private", "public", "unlisted"}:
            queryset = queryset.filter(visibility=visibility)

        return queryset


class ParallelLifeDetailView(DetailView):
    model = ParallelLife
    template_name = "parallel_lives/parallel_lives_detail.html"
    context_object_name = "parallel_life"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = ParallelLife.objects.select_related("owner").prefetch_related(
            "domains", "milestones", "reflections"
        )

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(visibility=ParallelLife.VisibilityChoices.PUBLIC) |
                Q(visibility=ParallelLife.VisibilityChoices.UNLISTED) |
                Q(owner=self.request.user)
            )

        return queryset.filter(
            Q(visibility=ParallelLife.VisibilityChoices.PUBLIC) |
            Q(visibility=ParallelLife.VisibilityChoices.UNLISTED)
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.visibility == ParallelLife.VisibilityChoices.PRIVATE and obj.owner != self.request.user:
            raise Http404("This parallel life is private.")
        return obj

class ParallelLifeCreateView(LoginRequiredMixin, CreateView):
    model = ParallelLife
    form_class = ParallelLifeForm
    template_name = "parallel_lives/parallel_life_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Parallel life created successfully.")
        return super().form_valid(form)


class ParallelLifeUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = ParallelLife
    form_class = ParallelLifeForm
    template_name = "parallel_lives/parallel_life_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        messages.success(self.request, "Parallel life updated successfully.")
        return super().form_valid(form)


class ParallelLifeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = ParallelLife
    template_name = "parallel_lives/parallel_life_confirm_delete.html"
    success_url = reverse_lazy("parallel-lives-list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        messages.success(self.request, "Parallel life deleted successfully.")
        return super().form_valid(form)
