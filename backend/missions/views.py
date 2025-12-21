"""
Vues pour les missions
"""

from django.db.models import Count, F, Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Organization
from accounts.serializers import (
    ApplicationSerializer,
    MissionCreateSerializer,
    MissionDetailSerializer,
    MissionListSerializer,
    ParticipationSerializer,
)

from .models import Application, Mission, Participation


class IsOrganization(permissions.BasePermission):
    """Permission: Utilisateur est une organisation"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "ORGANIZATION"


class IsVolunteer(permissions.BasePermission):
    """Permission: Utilisateur est un bénévole"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "VOLUNTEER"


# ========== PAGES PUBLIQUES ==========


class MissionListView(generics.ListAPIView):
    """
    Liste des missions (Page 2: Catalogue des Missions)
    Accessible sans connexion
    """

    serializer_class = MissionListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["wilaya", "odd", "status", "mission_type"]
    search_fields = ["title", "short_description", "organization__name"]
    ordering_fields = ["date", "created_at", "accepted_volunteers"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Mission.objects.filter(
            status="PUBLISHED", date__gte=timezone.now().date()
        ).select_related("organization", "odd")

        # Filtre par compétences
        skills = self.request.query_params.get("skills", None)
        if skills:
            skill_ids = skills.split(",")
            queryset = queryset.filter(required_skills__id__in=skill_ids).distinct()

        # Filtre places disponibles
        has_places = self.request.query_params.get("has_places", None)
        if has_places == "true":
            queryset = queryset.filter(accepted_volunteers__lt=F("required_volunteers"))

        return queryset


class MissionDetailView(generics.RetrieveAPIView):
    """
    Détail d'une mission (Page 3)
    Accessible sans connexion
    """

    serializer_class = MissionDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Mission.objects.filter(status="PUBLISHED").select_related("organization", "odd")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Incrémenter le compteur de vues
        instance.view_count += 1
        instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrganizationPublicProfileView(generics.RetrieveAPIView):
    """
    Profil public d'une organisation (Page 4)
    """

    from accounts.serializers import OrganizationPublicSerializer

    serializer_class = OrganizationPublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Organization.objects.filter(is_verified=True)


class HomePageStatsView(APIView):
    """
    Statistiques pour la page d'accueil (Page 1)
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from accounts.models import Volunteer

        stats = {
            "total_volunteers": Volunteer.objects.count(),
            "total_missions": Mission.objects.filter(status="PUBLISHED").count(),
            "total_hours": Volunteer.objects.aggregate(total=Sum("total_hours"))["total"]
            or 0,
        }

        # Dernières missions
        latest_missions = Mission.objects.filter(
            status="PUBLISHED", date__gte=timezone.now().date()
        ).select_related("organization", "odd")[:6]

        stats["latest_missions"] = MissionListSerializer(latest_missions, many=True).data

        return Response(stats)


# ========== ESPACE BÉNÉVOLE ==========


class VolunteerDashboardView(APIView):
    """
    Tableau de bord bénévole (Page 8)
    """

    permission_classes = [IsVolunteer]

    def get(self, request):
        volunteer = request.user.volunteer_profile

        # Applications en attente
        pending_applications = Application.objects.filter(
            volunteer=volunteer, status="PENDING"
        ).count()

        # Missions acceptées à venir
        accepted_missions = Application.objects.filter(
            volunteer=volunteer, status="ACCEPTED", mission__date__gte=timezone.now().date()
        ).count()

        # Prochaines missions
        upcoming_missions = Application.objects.filter(
            volunteer=volunteer, status="ACCEPTED", mission__date__gte=timezone.now().date()
        ).select_related("mission__organization")[:3]

        # Candidatures récentes
        recent_applications = Application.objects.filter(volunteer=volunteer).select_related(
            "mission__organization"
        )[:5]

        data = {
            "profile": {
                "total_hours": volunteer.total_hours,
                "badge_level": volunteer.badge_level,
                "completed_missions": volunteer.completed_missions,
                "average_rating": volunteer.average_rating,
            },
            "stats": {
                "pending_applications": pending_applications,
                "accepted_missions": accepted_missions,
            },
            "upcoming_missions": ApplicationSerializer(upcoming_missions, many=True).data,
            "recent_applications": ApplicationSerializer(recent_applications, many=True).data,
        }

        return Response(data)


class ApplyToMissionView(APIView):
    """
    Postuler à une mission
    """

    permission_classes = [IsVolunteer]

    def post(self, request, mission_id):
        try:
            mission = Mission.objects.get(id=mission_id, status="PUBLISHED")
        except Mission.DoesNotExist:
            return Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        volunteer = request.user.volunteer_profile

        # Vérifier si la mission est pleine
        if mission.is_full():
            return Response(
                {"error": "Plus de places disponibles"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si déjà postulé
        if Application.objects.filter(mission=mission, volunteer=volunteer).exists():
            return Response(
                {"error": "Vous avez déjà postulé à cette mission"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifier les compétences requises
        required_skills = mission.skill_requirements.filter(verification_required=True)
        volunteer_skills = volunteer.skills.filter(status="VALIDATED").values_list(
            "skill_id", flat=True
        )

        has_all_skills = all(req.skill_id in volunteer_skills for req in required_skills)

        if not has_all_skills:
            return Response(
                {"error": "Vous ne possédez pas toutes les compétences vérifiées requises"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Créer la candidature
        application = Application.objects.create(
            mission=mission,
            volunteer=volunteer,
            message=request.data.get("message", ""),
            has_required_skills=has_all_skills,
        )

        # Incrémenter le compteur
        mission.application_count += 1
        mission.save(update_fields=["application_count"])

        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


class MyApplicationsView(generics.ListAPIView):
    """
    Liste des candidatures du bénévole (Page 11)
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsVolunteer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return (
            Application.objects.filter(volunteer=self.request.user.volunteer_profile)
            .select_related("mission__organization")
            .order_by("-applied_at")
        )


class MyMissionsView(generics.ListAPIView):
    """
    Missions du bénévole (Page 12)
    """

    serializer_class = ParticipationSerializer
    permission_classes = [IsVolunteer]

    def get_queryset(self):
        status_filter = self.request.query_params.get("status", "all")
        volunteer = self.request.user.volunteer_profile

        queryset = Participation.objects.filter(volunteer=volunteer).select_related(
            "mission__organization"
        )

        if status_filter == "upcoming":
            queryset = queryset.filter(mission__date__gte=timezone.now().date())
        elif status_filter == "completed":
            queryset = queryset.filter(mission__date__lt=timezone.now().date())

        return queryset.order_by("-mission__date")


# ========== ESPACE ORGANISATION ==========


class OrganizationDashboardView(APIView):
    """
    Tableau de bord organisation (Page 15)
    """

    permission_classes = [IsOrganization]

    def get(self, request):
        organization = request.user.organization_profile

        # Statistiques
        total_missions = Mission.objects.filter(organization=organization).count()
        pending_applications = Application.objects.filter(
            mission__organization=organization, status="PENDING"
        ).count()

        # Missions actives
        active_missions = Mission.objects.filter(
            organization=organization, status="PUBLISHED", date__gte=timezone.now().date()
        ).annotate(application_count=Count("applications"))[:5]

        data = {
            "stats": {
                "total_missions": total_missions,
                "pending_applications": pending_applications,
                "total_volunteers": organization.total_volunteers,
                "average_rating": organization.average_rating,
            },
            "active_missions": MissionListSerializer(active_missions, many=True).data,
        }

        return Response(data)


class OrganizationMissionsView(generics.ListCreateAPIView):
    """
    Liste et création des missions de l'organisation (Page 16, 17)
    """

    permission_classes = [IsOrganization]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["title", "short_description"]

    def get_queryset(self):
        return (
            Mission.objects.filter(organization=self.request.user.organization_profile)
            .select_related("odd")
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MissionCreateSerializer
        return MissionListSerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization_profile)


class MissionApplicationsView(generics.ListAPIView):
    """
    Candidatures pour une mission (Page 18)
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsOrganization]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        mission_id = self.kwargs["mission_id"]
        return (
            Application.objects.filter(
                mission_id=mission_id, mission__organization=self.request.user.organization_profile
            )
            .select_related("volunteer__user")
            .order_by("-applied_at")
        )


class RespondToApplicationView(APIView):
    """
    Accepter ou refuser une candidature
    """

    permission_classes = [IsOrganization]

    def post(self, request, application_id):
        try:
            application = Application.objects.select_related("mission").get(
                id=application_id, mission__organization=request.user.organization_profile
            )
        except Application.DoesNotExist:
            return Response({"error": "Candidature non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")  # 'accept' ou 'reject'
        message = request.data.get("message", "")

        if action == "accept":
            # Vérifier si la mission n'est pas pleine
            if application.mission.is_full():
                return Response({"error": "Mission complète"}, status=status.HTTP_400_BAD_REQUEST)

            application.status = "ACCEPTED"
            application.mission.accepted_volunteers += 1
            application.mission.save(update_fields=["accepted_volunteers"])

            # Créer la participation
            Participation.objects.create(
                mission=application.mission,
                volunteer=application.volunteer,
                application=application,
            )

        elif action == "reject":
            application.status = "REJECTED"
        else:
            return Response({"error": "Action invalide"}, status=status.HTTP_400_BAD_REQUEST)

        application.organization_message = message
        application.responded_at = timezone.now()
        application.save()

        return Response(ApplicationSerializer(application).data)


class ValidateHoursView(APIView):
    """
    Valider les heures des bénévoles (Page 19)
    """

    permission_classes = [IsOrganization]

    def post(self, request, mission_id):
        try:
            mission = Mission.objects.get(
                id=mission_id, organization=request.user.organization_profile
            )
        except Mission.DoesNotExist:
            return Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier que la mission est terminée
        if mission.date >= timezone.now().date():
            return Response(
                {"error": "La mission n'est pas encore terminée"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validations = request.data.get("validations", [])

        for validation in validations:
            participation_id = validation.get("participation_id")
            was_present = validation.get("was_present", False)
            hours = validation.get("hours", 0)
            rating = validation.get("rating")
            comment = validation.get("comment", "")

            try:
                participation = Participation.objects.get(id=participation_id, mission=mission)

                participation.was_present = was_present
                participation.hours_completed = hours if was_present else 0
                participation.organization_rating = rating
                participation.organization_comment = comment
                participation.hours_validated = True
                participation.validated_at = timezone.now()
                participation.save()

                # Mettre à jour les statistiques du bénévole
                if was_present and hours > 0:
                    volunteer = participation.volunteer
                    volunteer.total_hours += float(hours)
                    volunteer.completed_missions += 1
                    volunteer.update_badge()

            except Participation.DoesNotExist:
                continue

        return Response({"message": "Heures validées avec succès"})


# ========== ESPACE ADMIN ==========


class AdminStatsView(APIView):
    """
    Statistiques pour l'admin (Page 23)
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from accounts.models import User, Volunteer
        from skills.models import VolunteerSkill

        stats = {
            "total_users": User.objects.count(),
            "total_volunteers": Volunteer.objects.count(),
            "total_organizations": Organization.objects.count(),
            "total_missions": Mission.objects.count(),
            "active_missions": Mission.objects.filter(status="PUBLISHED").count(),
            "pending_skills": VolunteerSkill.objects.filter(status="PENDING").count(),
            "total_hours": Volunteer.objects.aggregate(total=Sum("total_hours"))["total"]
            or 0,
        }

        return Response(stats)
