from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404

from parallel_lives.models import ParallelLife
from reflections.forms import ReflectionForm
from reflections.models import ReflectionEntry


class ReflectionOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ReflectionCreateView(LoginRequiredMixin, CreateView):
    model = ReflectionEntry
    form_class = ReflectionForm
    template_name = "reflections/reflection_form.html"

    def get_parallel_life(self):
        return get_object_or_404(ParallelLife, slug=self.kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        parallel_life = self.get_parallel_life()
        if parallel_life.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parallel_life = self.get_parallel_life()
        form.instance.user = self.request.user
        form.instance.parallel_life = parallel_life
        messages.success(self.request, "Reflection created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("parallel-life-detail", kwargs={"slug": self.get_parallel_life().slug})

class ReflectionUpdateView(LoginRequiredMixin, ReflectionOwnerRequiredMixin, UpdateView):
    model = ReflectionEntry
    form_class = ReflectionForm
    template_name = "reflections/reflection_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Reflection updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("parallel-life-detail", kwargs={"slug": self.object.parallel_life.slug})


class ReflectionDeleteView(LoginRequiredMixin, ReflectionOwnerRequiredMixin, DeleteView):
    model = ReflectionEntry
    template_name = "reflections/reflection_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Reflection deleted successfully.")
        return reverse("parallel-life-detail", kwargs={"slug": self.object.parallel_life.slug})















