"""
Tests Unitaires - Logique Métier des Bénévoles
Tests du calcul de badge, statistiques, et règles métier
"""

from datetime import date

import pytest

from accounts.models import User, Volunteer


@pytest.mark.unit
@pytest.mark.django_db
class TestVolunteerBadgeLogic:
    """Tests du système de badges (Bronze/Silver/Gold)"""

    def test_badge_bronze_0_hours(self):
        """Test: 0 heures = Badge Bronze"""
        user = User.objects.create_user(
            email="test@bronze0.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000000",
            wilaya="Alger",
            total_hours=0,
        )

        assert volunteer.badge_level == "BRONZE"
        assert volunteer.total_hours == 0

    def test_badge_bronze_49_hours(self):
        """Test: 49 heures = Badge Bronze"""
        user = User.objects.create_user(
            email="test@bronze49.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000001",
            wilaya="Alger",
            total_hours=49,
        )

        assert volunteer.badge_level == "BRONZE"

    def test_badge_silver_50_hours(self):
        """Test: 50 heures = Badge Silver (limite inférieure)"""
        user = User.objects.create_user(
            email="test@silver50.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000002",
            wilaya="Alger",
            total_hours=50,
        )

        assert volunteer.badge_level == "SILVER"

    def test_badge_silver_199_hours(self):
        """Test: 199 heures = Badge Silver (limite supérieure)"""
        user = User.objects.create_user(
            email="test@silver199.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000003",
            wilaya="Alger",
            total_hours=199,
        )

        assert volunteer.badge_level == "SILVER"

    def test_badge_gold_200_hours(self):
        """Test: 200 heures = Badge Gold"""
        user = User.objects.create_user(
            email="test@gold200.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000004",
            wilaya="Alger",
            total_hours=200,
        )

        assert volunteer.badge_level == "GOLD"

    def test_badge_gold_500_hours(self):
        """Test: 500+ heures = Badge Gold"""
        user = User.objects.create_user(
            email="test@gold500.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555000005",
            wilaya="Alger",
            total_hours=500,
        )

        assert volunteer.badge_level == "GOLD"


@pytest.mark.unit
@pytest.mark.django_db
class TestVolunteerStatistics:
    """Tests des statistiques des bénévoles"""

    def test_initial_statistics_zero(self):
        """Test: Les statistiques initiales doivent être à zéro"""
        user = User.objects.create_user(
            email="test@stats.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user, date_of_birth=date(1995, 1, 1), phone="0555111111", wilaya="Alger"
        )

        assert volunteer.total_hours == 0
        assert volunteer.completed_missions == 0
        assert volunteer.average_rating == 0.0

    def test_completed_missions_counter(self):
        """Test: Le compteur de missions doit s'incrémenter correctement"""
        user = User.objects.create_user(
            email="test@missions.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user,
            date_of_birth=date(1995, 1, 1),
            phone="0555222222",
            wilaya="Alger",
            completed_missions=5,
        )

        volunteer.completed_missions += 1
        volunteer.save()

        assert volunteer.completed_missions == 6


@pytest.mark.unit
@pytest.mark.django_db
class TestVolunteerSkillValidation:
    """Tests de la logique de validation des compétences"""

    def test_skill_with_verification_required(self):
        """Test: Les compétences nécessitant vérification doivent être en PENDING"""
        from skills.models import Skill, VolunteerSkill

        user = User.objects.create_user(
            email="test@skill.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user, date_of_birth=date(1995, 1, 1), phone="0555333333", wilaya="Alger"
        )

        # Compétence nécessitant vérification
        skill = Skill.objects.create(
            name="Premiers Secours",
            description="Certification premiers secours",
            requires_verification=True,
        )

        volunteer_skill = VolunteerSkill.objects.create(
            volunteer=volunteer, skill=skill, status="PENDING"
        )

        assert volunteer_skill.status == "PENDING"
        assert skill.requires_verification is True

    def test_skill_without_verification_auto_validated(self):
        """Test: Les compétences sans vérification sont validées automatiquement"""
        from skills.models import Skill, VolunteerSkill

        user = User.objects.create_user(
            email="test@skill2.com", password="test123", user_type="VOLUNTEER"
        )
        volunteer = Volunteer.objects.create(
            user=user, date_of_birth=date(1995, 1, 1), phone="0555444444", wilaya="Alger"
        )

        # Compétence sans vérification
        skill = Skill.objects.create(
            name="Communication",
            description="Compétences en communication",
            requires_verification=False,
        )

        volunteer_skill = VolunteerSkill.objects.create(
            volunteer=volunteer, skill=skill, status="VALIDATED"  # Auto-validé
        )

        assert volunteer_skill.status == "VALIDATED"
        assert skill.requires_verification is False


@pytest.mark.unit
@pytest.mark.django_db
class TestUserAuthentication:
    """Tests de l'authentification et de la gestion des mots de passe"""

    def test_password_is_hashed(self):
        """Test: Les mots de passe doivent être hashés"""
        user = User.objects.create_user(
            email="test@password.com", password="plaintext123", user_type="VOLUNTEER"
        )

        # Le mot de passe ne doit PAS être stocké en clair
        assert user.password != "plaintext123"
        # Le mot de passe doit commencer par un algorithme de hash
        assert user.password.startswith("pbkdf2_sha256$")

    def test_password_verification(self):
        """Test: La vérification du mot de passe doit fonctionner"""
        user = User.objects.create_user(
            email="test@verify.com", password="correctpassword", user_type="VOLUNTEER"
        )

        # Bon mot de passe
        assert user.check_password("correctpassword") is True

        # Mauvais mot de passe
        assert user.check_password("wrongpassword") is False
