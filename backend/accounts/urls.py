"""
URLs pour l'authentification et les comptes
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    OrganizationProfileView,
    RegisterOrganizationView,
    RegisterVolunteerView,
    VolunteerProfileView,
)

app_name = "accounts"

urlpatterns = [
    # Authentification
    path("register/volunteer/", RegisterVolunteerView.as_view(), name="register_volunteer"),
    path(
        "register/organization/", RegisterOrganizationView.as_view(), name="register_organization"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Profils
    path("profile/volunteer/", VolunteerProfileView.as_view(), name="volunteer_profile"),
    path("profile/organization/", OrganizationProfileView.as_view(), name="organization_profile"),
]
