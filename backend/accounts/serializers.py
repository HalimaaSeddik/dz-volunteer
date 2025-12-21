"""
Serializers pour l'API REST
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Organization, Volunteer
from missions.models import Application, Mission, Participation, Review
from odd.models import ODD
from skills.models import Skill, VolunteerSkill

User = get_user_model()


# ========== AUTH SERIALIZERS ==========


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "user_type", "date_joined")
        read_only_fields = ("id", "date_joined")


class RegisterVolunteerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "first_name", "last_name", "phone")

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        validated_data["user_type"] = "VOLUNTEER"
        user = User.objects.create_user(**validated_data)

        # Créer le profil bénévole
        Volunteer.objects.create(user=user)

        return user


class RegisterOrganizationSerializer(serializers.Serializer):
    # User fields
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    # Organization fields
    name = serializers.CharField(max_length=200)
    organization_type = serializers.ChoiceField(choices=Organization.ORG_TYPE_CHOICES)
    registration_number = serializers.CharField(max_length=100, required=False)
    email_org = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    wilaya = serializers.CharField(max_length=2)
    address = serializers.CharField()
    representative_name = serializers.CharField(max_length=200)
    representative_position = serializers.CharField(max_length=100)
    representative_email = serializers.EmailField()
    description = serializers.CharField(min_length=500)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        # Créer l'utilisateur
        user = User.objects.create_user(
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            user_type="ORGANIZATION",
        )

        # Créer l'organisation
        Organization.objects.create(
            user=user, email=validated_data.pop("email_org"), **validated_data
        )

        return user


# ========== VOLUNTEER SERIALIZERS ==========


class VolunteerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Volunteer
        fields = "__all__"


# ========== ORGANIZATION SERIALIZERS ==========


class OrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationPublicSerializer(serializers.ModelSerializer):
    """Version publique (sans infos sensibles)"""

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "organization_type",
            "description",
            "wilaya",
            "logo",
            "cover_photo",
            "is_verified",
            "total_missions",
            "total_volunteers",
            "average_rating",
        )


# ========== SKILL SERIALIZERS ==========


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class VolunteerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = VolunteerSkill
        fields = "__all__"


# ========== ODD SERIALIZERS ==========


class ODDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ODD
        fields = "__all__"


# ========== MISSION SERIALIZERS ==========


class MissionListSerializer(serializers.ModelSerializer):
    """Pour la liste des missions"""

    organization = OrganizationPublicSerializer(read_only=True)
    odd = ODDSerializer(read_only=True)
    remaining_places = serializers.IntegerField(source="get_remaining_places", read_only=True)
    fill_percentage = serializers.IntegerField(source="get_fill_percentage", read_only=True)

    class Meta:
        model = Mission
        fields = (
            "id",
            "title",
            "short_description",
            "date",
            "start_time",
            "end_time",
            "wilaya",
            "commune",
            "organization",
            "odd",
            "required_volunteers",
            "accepted_volunteers",
            "remaining_places",
            "fill_percentage",
            "image",
            "status",
        )


class MissionDetailSerializer(serializers.ModelSerializer):
    """Pour les détails d'une mission"""

    organization = OrganizationPublicSerializer(read_only=True)
    odd = ODDSerializer(read_only=True)
    remaining_places = serializers.IntegerField(source="get_remaining_places", read_only=True)
    fill_percentage = serializers.IntegerField(source="get_fill_percentage", read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = Mission
        fields = "__all__"


class MissionCreateSerializer(serializers.ModelSerializer):
    """Pour créer/modifier une mission"""

    class Meta:
        model = Mission
        exclude = ("organization", "view_count", "application_count", "accepted_volunteers")

    def create(self, validated_data):
        # L'organisation est ajoutée depuis la vue
        return super().create(validated_data)


# ========== APPLICATION SERIALIZERS ==========


class ApplicationSerializer(serializers.ModelSerializer):
    mission = MissionListSerializer(read_only=True)
    volunteer = VolunteerProfileSerializer(read_only=True)

    class Meta:
        model = Application
        fields = "__all__"


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("mission", "message")


# ========== PARTICIPATION SERIALIZERS ==========


class ParticipationSerializer(serializers.ModelSerializer):
    mission = MissionListSerializer(read_only=True)
    volunteer = VolunteerProfileSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = "__all__"


# ========== REVIEW SERIALIZERS ==========


class ReviewSerializer(serializers.ModelSerializer):
    volunteer = VolunteerProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
