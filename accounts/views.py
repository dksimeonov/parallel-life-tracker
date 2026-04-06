from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from accounts.tasks import send_welcome_email_task
from accounts.forms import CustomLoginForm, ProfileEditForm, UserRegistrationForm
from accounts.models import AppUser, Profile


class RegisterView(CreateView):
    model = AppUser
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        send_welcome_email_task.delay(
            username=self.object.username,
            email=self.object.email,
        )

        messages.success(self.request, "Your account was created successfully.")
        return response


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        context["parallel_lives_count"] = self.request.user.parallel_lives.count()
        context["reflections_count"] = self.request.user.reflections.count()
        context["milestones_count"] = self.request.user.created_milestones.count()
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_details.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


class PublicUserDetailView(DetailView):
    model = Profile
    template_name = "accounts/profile_details.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        user = get_object_or_404(AppUser, username=self.kwargs["username"])
        profile = user.profile

        if not profile.is_profile_public:
            if not self.request.user.is_authenticated or user != self.request.user:
                raise Http404("This profile is private.")

        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile-details")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Your profile was updated successfully.")
        return super().form_valid(form)
