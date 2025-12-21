"""
URLs pour les missions
"""

from django.urls import path

from .views import (
    # Admin
    AdminStatsView,
    ApplyToMissionView,
    HomePageStatsView,
    MissionApplicationsView,
    MissionDetailView,
    # Pages publiques
    MissionListView,
    MyApplicationsView,
    MyMissionsView,
    # Espace Organisation
    OrganizationDashboardView,
    OrganizationMissionsView,
    OrganizationPublicProfileView,
    RespondToApplicationView,
    ValidateHoursView,
    # Espace Bénévole
    VolunteerDashboardView,
)

app_name = "missions"

urlpatterns = [
    # ========== PAGES PUBLIQUES ==========
    path("", MissionListView.as_view(), name="mission_list"),  # Page 2
    path("<int:pk>/", MissionDetailView.as_view(), name="mission_detail"),  # Page 3
    path(
        "organization/<int:pk>/",
        OrganizationPublicProfileView.as_view(),
        name="organization_profile",
    ),  # Page 4
    path("home-stats/", HomePageStatsView.as_view(), name="home_stats"),  # Page 1
    # ========== ESPACE BÉNÉVOLE ==========
    path(
        "volunteer/dashboard/", VolunteerDashboardView.as_view(), name="volunteer_dashboard"
    ),  # Page 8
    path("volunteer/apply/<int:mission_id>/", ApplyToMissionView.as_view(), name="apply"),
    path(
        "volunteer/applications/", MyApplicationsView.as_view(), name="my_applications"
    ),  # Page 11
    path("volunteer/missions/", MyMissionsView.as_view(), name="my_missions"),  # Page 12
    # ========== ESPACE ORGANISATION ==========
    path(
        "organization/dashboard/",
        OrganizationDashboardView.as_view(),
        name="organization_dashboard",
    ),  # Page 15
    path(
        "organization/missions/", OrganizationMissionsView.as_view(), name="organization_missions"
    ),  # Page 16, 17
    path(
        "organization/mission/<int:mission_id>/applications/",
        MissionApplicationsView.as_view(),
        name="mission_applications",
    ),  # Page 18
    path(
        "organization/application/<int:application_id>/respond/",
        RespondToApplicationView.as_view(),
        name="respond_application",
    ),
    path(
        "organization/mission/<int:mission_id>/validate-hours/",
        ValidateHoursView.as_view(),
        name="validate_hours",
    ),  # Page 19
    # ========== ADMIN ==========
    path("admin/stats/", AdminStatsView.as_view(), name="admin_stats"),  # Page 23
]
