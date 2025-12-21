"""
Tests d'Intégration - API RESTful
Tests end-to-end des endpoints API avec base de données
"""

from datetime import date, timedelta

import pytest
from rest_framework import status

from accounts.models import Organization, User, Volunteer
from missions.models import Application, Mission
from odd.models import ODD
from skills.models import Skill, VolunteerSkill


@pytest.mark.integration
@pytest.mark.django_db
class TestApplicationAPI:
    """
    Tests d'intégration pour le endpoint de candidature
    Scénario: Un bénévole postule à une mission
    """

    def test_apply_to_mission_success(self, api_client):
        """
        Test Intégration 1: Candidature complète réussie

        Scénario:
        1. Créer organisation + mission publiée
        2. Créer bénévole avec compétences requises validées
        3. POST /api/missions/volunteer/apply/ avec token JWT
        4. Vérifier: Application créée avec status PENDING
        """
        # 1. Créer organisation
        user_org = User.objects.create_user(
            email="org@integration.com", password="testpass123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="ONG Integration Test",
            organization_type="NGO",
            phone="0555000000",
            wilaya="Alger",
            address="123 Rue Test",
            representative_first_name="Rep",
            representative_last_name="Test",
            representative_position="Directeur",
        )

        # Créer ODD
        odd = ODD.objects.create(
            number=1, title_fr="Pas de pauvreté", title_ar="القضاء على الفقر", color="#E5243B"
        )

        # Créer mission publiée
        mission = Mission.objects.create(
            organization=org,
            title="Mission Test Intégration",
            description="Mission pour tester la candidature",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="123 Rue Mission",
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_volunteers=10,
            current_volunteers=0,
            odd=odd,
        )

        # Créer compétence requise
        skill = Skill.objects.create(
            name="Communication",
            description="Compétences en communication",
            requires_verification=False,
        )

        # 2. Créer bénévole
        user_vol = User.objects.create_user(
            email="volunteer@integration.com", password="testpass123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol, date_of_birth=date(1995, 1, 1), phone="0555111111", wilaya="Alger"
        )

        # Ajouter compétence au bénévole
        VolunteerSkill.objects.create(volunteer=volunteer, skill=skill, status="VALIDATED")

        # 3. Authentifier le bénévole
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user_vol)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # 4. POST Candidature
        url = "/api/missions/volunteer/apply/"
        data = {"mission": mission.id, "motivation": "Je suis très motivé pour cette mission!"}

        response = api_client.post(url, data, format="json")

        # Vérifications
        assert response.status_code == status.HTTP_201_CREATED
        assert Application.objects.count() == 1

        application = Application.objects.first()
        assert application.volunteer == volunteer
        assert application.mission == mission
        assert application.status == "PENDING"
        assert application.motivation == "Je suis très motivé pour cette mission!"

    def test_apply_to_mission_already_applied(self, api_client):
        """Test: Impossible de postuler deux fois à la même mission"""
        # Créer organisation + mission
        user_org = User.objects.create_user(
            email="org@duplicate.com", password="testpass123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="ONG Duplicate",
            organization_type="NGO",
            phone="0555000001",
            wilaya="Alger",
            address="Test",
            representative_first_name="Rep",
            representative_last_name="Test",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=2, title_fr="Test ODD", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Duplicate",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_volunteers=10,
            odd=odd,
        )

        # Créer bénévole
        user_vol = User.objects.create_user(
            email="vol@duplicate.com", password="testpass123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol, date_of_birth=date(1995, 1, 1), phone="0555222222", wilaya="Alger"
        )

        # Première candidature
        Application.objects.create(
            mission=mission,
            volunteer=volunteer,
            status="PENDING",
            motivation="Première candidature",
        )

        # Authentifier
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user_vol)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Tentative de deuxième candidature
        url = "/api/missions/volunteer/apply/"
        data = {"mission": mission.id, "motivation": "Deuxième candidature (devrait échouer)"}

        response = api_client.post(url, data, format="json")

        # Vérification: devrait échouer (400 Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Application.objects.count() == 1  # Une seule candidature


@pytest.mark.integration
@pytest.mark.django_db
class TestValidateHoursAPI:
    """
    Tests d'intégration pour la validation des heures
    Scénario: Organisation valide les heures après une mission
    """

    def test_validate_hours_and_update_badge(self, api_client):
        """
        Test Intégration 2: Validation heures + mise à jour badge automatique

        Scénario:
        1. Créer organisation + mission COMPLETED
        2. Créer bénévole Bronze (45h) avec participation acceptée
        3. POST /api/missions/organization/validate-hours/ pour valider 10h
        4. Vérifier: total_hours = 55h, badge_level = SILVER
        """
        # 1. Créer organisation
        user_org = User.objects.create_user(
            email="org@hours.com", password="testpass123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="ONG Validation Heures",
            organization_type="NGO",
            phone="0555000002",
            wilaya="Alger",
            address="Test",
            representative_first_name="Rep",
            representative_last_name="Test",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=3, title_fr="Test ODD", title_ar="تست", color="#E5243B")

        # Mission COMPLETED (terminée)
        mission = Mission.objects.create(
            organization=org,
            title="Mission Validation Heures",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="COMPLETED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            max_volunteers=10,
            odd=odd,
        )

        # 2. Créer bénévole Bronze (45h)
        user_vol = User.objects.create_user(
            email="vol@hours.com", password="testpass123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol,
            date_of_birth=date(1995, 1, 1),
            phone="0555333333",
            wilaya="Alger",
            total_hours=45,  # Bronze
            completed_missions=5,
        )

        # Vérifier badge initial = Bronze
        assert volunteer.badge_level == "BRONZE"

        # Créer participation acceptée
        from missions.models import Participation

        participation = Participation.objects.create(
            mission=mission, volunteer=volunteer, hours_completed=10, status="PENDING_VALIDATION"
        )

        # 3. Authentifier organisation
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user_org)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # 4. POST Validation heures
        url = "/api/missions/organization/validate-hours/"
        data = {"participation_id": participation.id, "hours_completed": 10}

        response = api_client.post(url, data, format="json")

        # Vérifications
        assert response.status_code == status.HTTP_200_OK

        # Recharger le bénévole depuis la BDD
        volunteer.refresh_from_db()

        # Vérifier mise à jour des heures: 45 + 10 = 55
        assert volunteer.total_hours == 55

        # Vérifier mise à jour du badge: 55h = SILVER
        assert volunteer.badge_level == "SILVER"

        # Vérifier incrément des missions complétées
        assert volunteer.completed_missions == 6

    def test_validate_hours_bronze_to_gold(self, api_client):
        """Test: Validation de 50h pour un bénévole à 195h (Silver -> Gold)"""
        # Créer organisation
        user_org = User.objects.create_user(
            email="org@gold.com", password="testpass123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="ONG Gold",
            organization_type="NGO",
            phone="0555000003",
            wilaya="Alger",
            address="Test",
            representative_first_name="Rep",
            representative_last_name="Test",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=4, title_fr="Test ODD", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Gold",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="COMPLETED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            max_volunteers=10,
            odd=odd,
        )

        # Bénévole Silver avec 195h
        user_vol = User.objects.create_user(
            email="vol@gold.com", password="testpass123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol,
            date_of_birth=date(1995, 1, 1),
            phone="0555444444",
            wilaya="Alger",
            total_hours=195,  # Silver (limite supérieure)
            completed_missions=20,
        )

        assert volunteer.badge_level == "SILVER"

        # Participation de 50h
        from missions.models import Participation

        participation = Participation.objects.create(
            mission=mission, volunteer=volunteer, hours_completed=50, status="PENDING_VALIDATION"
        )

        # Authentifier organisation
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user_org)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Valider 50h
        url = "/api/missions/organization/validate-hours/"
        data = {"participation_id": participation.id, "hours_completed": 50}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        volunteer.refresh_from_db()

        # 195 + 50 = 245h -> Gold
        assert volunteer.total_hours == 245
        assert volunteer.badge_level == "GOLD"


@pytest.mark.integration
@pytest.mark.django_db
class TestAuthenticationAPI:
    """Tests d'intégration pour l'authentification JWT"""

    def test_login_get_jwt_token(self, api_client):
        """Test: Login réussi retourne un token JWT valide"""
        # Créer utilisateur
        User.objects.create_user(
            email="test@jwt.com",
            password="testpass123",
            user_type="VOLUNTEER",
            first_name="Test",
            last_name="User",
        )

        # Login
        url = "/api/auth/login/"
        data = {"email": "test@jwt.com", "password": "testpass123"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data

        # Vérifier que le token fonctionne
        token = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test endpoint protégé
        protected_url = "/api/missions/volunteer/dashboard/"
        protected_response = api_client.get(protected_url)

        # Devrait être accessible avec le token
        assert protected_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
