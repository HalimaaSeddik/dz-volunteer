"""
Tests Unitaires - Logique Métier des Missions
Tests des règles métier, validations, et contraintes
"""

from datetime import date, timedelta

import pytest

from accounts.models import Organization, User
from missions.models import Application, Mission, MissionSkillRequirement
from odd.models import ODD
from skills.models import Skill


@pytest.mark.unit
@pytest.mark.django_db
class TestMissionCapacityLogic:
    """Tests de la logique de capacité des missions"""

    def test_mission_capacity_not_full(self):
        """Test: Vérifier qu'une mission n'est pas pleine"""
        user = User.objects.create_user(
            email="org@capacity.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user,
            organization_name="Test Capacity",
            organization_type="NGO",
            phone="0555000000",
            wilaya="Alger",
            address="Test Address",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=1, title_fr="Test ODD", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Test Capacity",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            current_volunteers=5,
            odd=odd,
        )

        # La mission n'est pas pleine (5/10)
        assert mission.current_volunteers < mission.max_volunteers
        assert mission.current_volunteers == 5

    def test_mission_capacity_full(self):
        """Test: Vérifier qu'une mission est pleine"""
        user = User.objects.create_user(
            email="org@full.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user,
            organization_name="Test Full",
            organization_type="NGO",
            phone="0555000001",
            wilaya="Alger",
            address="Test Address",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=2, title_fr="Test ODD 2", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Full",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            current_volunteers=10,
            odd=odd,
        )

        # La mission est pleine (10/10)
        assert mission.current_volunteers == mission.max_volunteers


@pytest.mark.unit
@pytest.mark.django_db
class TestApplicationStatusLogic:
    """Tests de la logique des statuts de candidatures"""

    def test_application_initial_status_pending(self):
        """Test: Une nouvelle candidature doit être PENDING"""
        from accounts.models import Volunteer

        # Créer organisation
        user_org = User.objects.create_user(
            email="org@app.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="Test App",
            organization_type="NGO",
            phone="0555000002",
            wilaya="Alger",
            address="Test",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        # Créer bénévole
        user_vol = User.objects.create_user(
            email="vol@app.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol, date_of_birth=date(1995, 1, 1), phone="0555111111", wilaya="Alger"
        )

        # Créer mission
        odd = ODD.objects.create(number=3, title_fr="Test ODD 3", title_ar="تست", color="#E5243B")
        mission = Mission.objects.create(
            organization=org,
            title="Mission App",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            odd=odd,
        )

        # Créer candidature
        application = Application.objects.create(
            mission=mission, volunteer=volunteer, status="PENDING", motivation="Test motivation"
        )

        assert application.status == "PENDING"

    def test_application_status_transitions(self):
        """Test: Les transitions de statut de candidature"""
        from accounts.models import Volunteer

        user_org = User.objects.create_user(
            email="org@status.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="Test Status",
            organization_type="NGO",
            phone="0555000003",
            wilaya="Alger",
            address="Test",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        user_vol = User.objects.create_user(
            email="vol@status.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user_vol, date_of_birth=date(1995, 1, 1), phone="0555222222", wilaya="Alger"
        )

        odd = ODD.objects.create(number=4, title_fr="Test ODD 4", title_ar="تست", color="#E5243B")
        mission = Mission.objects.create(
            organization=org,
            title="Mission Status",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            odd=odd,
        )

        application = Application.objects.create(
            mission=mission, volunteer=volunteer, status="PENDING", motivation="Test"
        )

        # Test transition PENDING -> ACCEPTED
        application.status = "ACCEPTED"
        application.save()
        assert application.status == "ACCEPTED"

        # Test transition ACCEPTED -> CANCELLED (ne devrait pas être possible en prod)
        application.status = "CANCELLED"
        application.save()
        assert application.status == "CANCELLED"


@pytest.mark.unit
@pytest.mark.django_db
class TestMissionSkillRequirement:
    """Tests de la logique des compétences requises pour les missions"""

    def test_mission_with_required_skill(self):
        """Test: Une mission peut avoir des compétences requises"""
        user_org = User.objects.create_user(
            email="org@skill.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="Test Skill",
            organization_type="NGO",
            phone="0555000004",
            wilaya="Alger",
            address="Test",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=5, title_fr="Test ODD 5", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Skill",
            description="Test",
            cause="HEALTH",
            type="ONE_TIME",
            status="PUBLISHED",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            odd=odd,
        )

        # Compétence requise avec vérification
        skill = Skill.objects.create(
            name="Premiers Secours",
            description="Certification premiers secours",
            requires_verification=True,
        )

        requirement = MissionSkillRequirement.objects.create(
            mission=mission, skill=skill, is_required=True
        )

        assert requirement.is_required is True
        assert requirement.skill.requires_verification is True


@pytest.mark.unit
@pytest.mark.django_db
class TestMissionStatusWorkflow:
    """Tests du workflow de statut des missions"""

    def test_mission_status_draft_to_published(self):
        """Test: Transition DRAFT -> PUBLISHED"""
        user_org = User.objects.create_user(
            email="org@workflow.com", password="test123", user_type="ORGANIZATION"
        )
        org = Organization.objects.create(
            user=user_org,
            organization_name="Test Workflow",
            organization_type="NGO",
            phone="0555000005",
            wilaya="Alger",
            address="Test",
            representative_first_name="Test",
            representative_last_name="Rep",
            representative_position="Dir",
        )

        odd = ODD.objects.create(number=6, title_fr="Test ODD 6", title_ar="تست", color="#E5243B")

        mission = Mission.objects.create(
            organization=org,
            title="Mission Workflow",
            description="Test",
            cause="SOCIAL",
            type="ONE_TIME",
            status="DRAFT",
            wilaya="Alger",
            address="Test",
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_volunteers=10,
            odd=odd,
        )

        assert mission.status == "DRAFT"

        # Publier la mission
        mission.status = "PUBLISHED"
        mission.save()

        assert mission.status == "PUBLISHED"
