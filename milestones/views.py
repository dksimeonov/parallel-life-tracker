from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import get_object_or_404

from milestones.forms import MilestoneForm
from milestones.models import Milestone
from parallel_lives.models import ParallelLife


class MilestoneOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.parallel_life.owner == self.request.user


class MilestoneListView(LoginRequiredMixin, ListView):
    model = Milestone
    template_name = "milestones/milestone_list.html"
    context_object_name = "milestones"

    def get_parallel_life(self):
        return get_object_or_404(ParallelLife, slug=self.kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        parallel_life = self.get_parallel_life()
        if parallel_life.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_parallel_life().milestones.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parallel_life"] = self.get_parallel_life()
        return context


class MilestoneCreateView(LoginRequiredMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = "milestones/milestone_form.html"

    def get_parallel_life(self):
        return get_object_or_404(ParallelLife, slug=self.kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        parallel_life = self.get_parallel_life()
        if parallel_life.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parallel_life = self.get_parallel_life()
        form.instance.parallel_life = parallel_life
        form.instance.created_by = self.request.user
        messages.success(self.request, "Milestone created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("milestone-list", kwargs={"slug": self.get_parallel_life().slug})


class MilestoneUpdateView(LoginRequiredMixin, MilestoneOwnerRequiredMixin, UpdateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = "milestones/milestone_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Milestone updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("milestone-list", kwargs={"slug": self.object.parallel_life.slug})


class MilestoneDeleteView(LoginRequiredMixin, MilestoneOwnerRequiredMixin, DeleteView):
    model = Milestone
    template_name = "milestones/milestone_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Milestone deleted successfully.")
        return reverse_lazy("milestone-list", kwargs={"slug": self.object.parallel_life.slug})
