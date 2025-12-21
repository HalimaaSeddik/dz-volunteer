"""
Modèles pour la gestion des missions et candidatures
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Organization, Volunteer
from odd.models import ODD
from skills.models import Skill


class Mission(models.Model):
    """
    Mission publiée par une organisation
    """

    STATUS_CHOICES = [
        ("DRAFT", "Brouillon"),
        ("PUBLISHED", "Publiée"),
        ("ONGOING", "En cours"),
        ("COMPLETED", "Terminée"),
        ("CANCELLED", "Annulée"),
        ("ARCHIVED", "Archivée"),
    ]

    TYPE_CHOICES = [
        ("ONE_TIME", "Ponctuelle"),
        ("RECURRING", "Récurrente"),
    ]

    CAUSE_CHOICES = [
        ("ENVIRONMENT", "Environnement"),
        ("EDUCATION", "Éducation"),
        ("HEALTH", "Santé"),
        ("SOCIAL", "Aide sociale"),
        ("CONSTRUCTION", "Construction"),
        ("CULTURE", "Culture"),
        ("ANIMAL", "Protection animale"),
        ("FAMILY", "Famille"),
    ]

    # Informations de base
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="missions"
    )
    title = models.CharField(max_length=100, verbose_name="Titre")
    short_description = models.CharField(max_length=200, verbose_name="Description courte")
    full_description = models.TextField(verbose_name="Description complète")
    mission_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="ONE_TIME", verbose_name="Type"
    )

    # ODD et cause
    odd = models.ForeignKey(
        ODD, on_delete=models.PROTECT, related_name="missions", verbose_name="ODD"
    )
    causes = models.JSONField(default=list, verbose_name="Types de cause")

    # Date et lieu
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    duration_hours = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Durée (heures)", null=True, blank=True
    )

    wilaya = models.CharField(max_length=2, verbose_name="Wilaya")
    commune = models.CharField(max_length=100, verbose_name="Commune")
    full_address = models.TextField(verbose_name="Adresse complète")
    meeting_point = models.TextField(verbose_name="Point de rencontre")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Accessibilité
    accessible_by_car = models.BooleanField(default=False, verbose_name="Accessible en voiture")
    accessible_by_transport = models.BooleanField(default=False, verbose_name="Transport en commun")
    accessible_on_foot = models.BooleanField(default=False, verbose_name="À pied")
    pmr_accessible = models.BooleanField(default=False, verbose_name="PMR")

    # Bénévoles
    required_volunteers = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Bénévoles requis"
    )
    accepted_volunteers = models.IntegerField(default=0, verbose_name="Bénévoles acceptés")

    # Compétences requises
    required_skills = models.ManyToManyField(
        Skill, through="MissionSkillRequirement", related_name="missions"
    )

    # À apporter et équipements
    items_to_bring = models.JSONField(default=list, verbose_name="À apporter", blank=True)
    provided_equipment = models.JSONField(
        default=dict, verbose_name="Équipements fournis", blank=True
    )

    # Prérequis
    additional_requirements = models.TextField(blank=True, verbose_name="Prérequis supplémentaires")
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ("BEGINNER", "Débutant"),
            ("INTERMEDIATE", "Intermédiaire"),
            ("EXPERIENCED", "Expérimenté"),
        ],
        default="BEGINNER",
        verbose_name="Niveau d'expérience",
    )

    # Image
    image = models.ImageField(upload_to="missions/", blank=True, null=True, verbose_name="Image")

    # Statut et visibilité
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="DRAFT", verbose_name="Statut"
    )
    is_public = models.BooleanField(default=True, verbose_name="Public")

    # Contact
    contact_name = models.CharField(max_length=200, verbose_name="Contact", blank=True)
    contact_email = models.EmailField(verbose_name="Email contact", blank=True)
    contact_phone = models.CharField(max_length=15, verbose_name="Téléphone contact", blank=True)

    # Statistiques
    view_count = models.IntegerField(default=0, verbose_name="Vues")
    application_count = models.IntegerField(default=0, verbose_name="Candidatures")

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de publication")

    class Meta:
        verbose_name = "Mission"
        verbose_name_plural = "Missions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "date"]),
            models.Index(fields=["wilaya", "status"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.organization.name}"

    def get_remaining_places(self):
        return self.required_volunteers - self.accepted_volunteers

    def get_fill_percentage(self):
        if self.required_volunteers == 0:
            return 0
        return int((self.accepted_volunteers / self.required_volunteers) * 100)

    def is_full(self):
        return self.accepted_volunteers >= self.required_volunteers


class MissionSkillRequirement(models.Model):
    """
    Compétences requises pour une mission avec indication si vérification obligatoire
    """

    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="skill_requirements"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    verification_required = models.BooleanField(
        default=False, verbose_name="Vérification obligatoire"
    )

    class Meta:
        unique_together = ["mission", "skill"]
        verbose_name = "Compétence requise"
        verbose_name_plural = "Compétences requises"

    def __str__(self):
        req = "✓" if self.verification_required else ""
        return f"{self.mission.title} - {self.skill.name} {req}"


class Application(models.Model):
    """
    Candidature d'un bénévole pour une mission
    """

    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("ACCEPTED", "Acceptée"),
        ("REJECTED", "Refusée"),
        ("CANCELLED", "Annulée"),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="applications")
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Statut"
    )

    message = models.TextField(blank=True, verbose_name="Message du bénévole")
    organization_message = models.TextField(blank=True, verbose_name="Message de l'organisation")

    # Validation
    has_required_skills = models.BooleanField(default=False, verbose_name="Possède les compétences")

    # Dates
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de réponse")

    class Meta:
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        unique_together = ["mission", "volunteer"]
        ordering = ["-applied_at"]
        indexes = [
            models.Index(fields=["status", "applied_at"]),
        ]

    def __str__(self):
        return f"{self.volunteer.user.get_full_name()} -> {self.mission.title} ({self.status})"


class Participation(models.Model):
    """
    Participation effective d'un bénévole à une mission (après acceptation)
    """

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="participations")
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.CASCADE, related_name="participations"
    )
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name="participation", null=True
    )

    # Validation des heures
    was_present = models.BooleanField(default=False, verbose_name="Présent")
    hours_completed = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="Heures effectuées"
    )
    hours_validated = models.BooleanField(default=False, verbose_name="Heures validées")
    validated_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")

    # Évaluation par l'organisation
    organization_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name="Note de l'organisation",
    )
    organization_comment = models.TextField(
        blank=True, verbose_name="Commentaire de l'organisation"
    )

    # Évaluation par le bénévole
    volunteer_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name="Note du bénévole",
    )
    volunteer_comment = models.TextField(blank=True, verbose_name="Commentaire du bénévole")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = ["mission", "volunteer"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.volunteer.user.get_full_name()} - {self.mission.title}"


class Review(models.Model):
    """
    Avis d'un bénévole sur une organisation
    """

    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="reviews")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="reviews")
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="reviews", null=True
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Note"
    )
    comment = models.TextField(verbose_name="Commentaire")

    organization_response = models.TextField(blank=True, verbose_name="Réponse de l'organisation")
    responded_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.volunteer.user.get_full_name()} - {self.organization.name} ({self.rating}★)"


class Report(models.Model):
    """
    Signalement d'une mission ou d'un utilisateur
    """

    TYPE_CHOICES = [
        ("MISSION", "Mission"),
        ("USER", "Utilisateur"),
        ("ORGANIZATION", "Organisation"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("REVIEWED", "Examiné"),
        ("RESOLVED", "Résolu"),
        ("DISMISSED", "Rejeté"),
    ]

    reporter = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="reports_made"
    )
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")

    # Cible du signalement
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, null=True, blank=True, related_name="reports"
    )
    reported_user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received",
    )

    reason = models.TextField(verbose_name="Raison")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Statut"
    )

    admin_notes = models.TextField(blank=True, verbose_name="Notes admin")
    resolved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_resolved",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Signalement {self.report_type} - {self.status}"
