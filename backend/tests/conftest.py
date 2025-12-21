"""
Fichier de configuration pour pytest-django
"""

import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    """
    Configuration de la base de données de test
    """
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dzvolunteer_test",
        "USER": "postgres",
        "PASSWORD": "20772077",
        "HOST": "localhost",
        "PORT": "5432",
    }


@pytest.fixture
def api_client():
    """
    Fixture pour créer un client API REST Framework
    """
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def admin_user(db):
    """
    Fixture pour créer un utilisateur administrateur
    """
    from accounts.models import User

    return User.objects.create_superuser(
        email="admin@test.com", password="testpass123", first_name="Admin", last_name="Test"
    )


@pytest.fixture
def volunteer_user(db):
    """
    Fixture pour créer un utilisateur bénévole
    """
    from accounts.models import User, Volunteer

    user = User.objects.create_user(
        email="volunteer@test.com",
        password="testpass123",
        first_name="Bénévole",
        last_name="Test",
        user_type="VOLUNTEER",
    )
    Volunteer.objects.create(
        user=user, date_of_birth="1995-01-01", phone="0555123456", wilaya="Alger"
    )
    return user


@pytest.fixture
def organization_user(db):
    """
    Fixture pour créer un utilisateur organisation
    """
    from accounts.models import Organization, User

    user = User.objects.create_user(
        email="org@test.com",
        password="testpass123",
        first_name="Organisation",
        last_name="Test",
        user_type="ORGANIZATION",
    )
    Organization.objects.create(
        user=user,
        organization_name="Test ONG",
        organization_type="NGO",
        phone="0555654321",
        wilaya="Alger",
        address="123 Rue Test",
        description="Organisation de test",
        representative_first_name="Rep",
        representative_last_name="Test",
        representative_position="Directeur",
    )
    return user


@pytest.fixture
def authenticated_client(api_client, volunteer_user):
    """
    Fixture pour un client authentifié comme bénévole
    """
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(volunteer_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def sample_skill(db):
    """
    Fixture pour créer une compétence
    """
    from skills.models import Skill

    return Skill.objects.create(
        name="Informatique",
        description="Compétences informatiques générales",
        requires_verification=False,
    )


@pytest.fixture
def sample_odd(db):
    """
    Fixture pour créer un ODD
    """
    from odd.models import ODD

    return ODD.objects.create(
        number=1,
        title_fr="Pas de pauvreté",
        title_ar="القضاء على الفقر",
        description_fr="Éliminer la pauvreté sous toutes ses formes",
        color="#E5243B",
    )


@pytest.fixture
def sample_mission(db, organization_user, sample_odd):
    """
    Fixture pour créer une mission
    """
    from accounts.models import Organization
    from missions.models import Mission

    org = Organization.objects.get(user=organization_user)
    return Mission.objects.create(
        organization=org,
        title="Mission Test",
        description="Description de la mission de test",
        cause="SOCIAL",
        type="ONE_TIME",
        status="PUBLISHED",
        wilaya="Alger",
        address="123 Rue Mission",
        start_date="2025-12-25",
        end_date="2025-12-26",
        max_volunteers=10,
        odd=sample_odd,
    )
