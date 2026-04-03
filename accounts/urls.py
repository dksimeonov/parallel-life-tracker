from django.urls import path

from accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    ProfileDetailView,
    ProfileUpdateView,
    PublicUserDetailView,
    RegisterView,
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileDetailView.as_view(), name="profile-details"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path("users/<str:username>/", PublicUserDetailView.as_view(), name="public-user-details"),
]