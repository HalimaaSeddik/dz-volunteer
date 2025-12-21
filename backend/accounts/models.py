from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Il faut un email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = [
        ("VOLUNTEER", "Bénévole"),
        ("ORGANIZATION", "Organisation"),
        ("ADMIN", "Administrateur"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r"^0[5-7]\d{8}$", message="Numéro invalide")],
        verbose_name="Téléphone",
        blank=True,
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email


class Volunteer(models.Model):

    BADGE_CHOICES = [
        ("BRONZE", "Bronze (0-49h)"),
        ("SILVER", "Argent (50-199h)"),
        ("GOLD", "Or (200h+)"),
    ]

    GENDER_CHOICES = [
        ("M", "Homme"),
        ("F", "Femme"),
        ("O", "Autre"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    wilaya = models.CharField(max_length=2, blank=True)
    commune = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to="volunteers/", blank=True, null=True)
    motivation = models.TextField(blank=True)

    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_missions = models.IntegerField(default=0, verbose_name="Missions complétées")
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, verbose_name="Note moyenne"
    )
    badge_level = models.CharField(
        max_length=10, choices=BADGE_CHOICES, default="BRONZE", verbose_name="Badge"
    )

    # Disponibilités (JSON ou champs séparés)
    availability = models.JSONField(default=dict, verbose_name="Disponibilités", blank=True)

    # Centres d'intérêt
    interests = models.JSONField(default=list, verbose_name="Centres d'intérêt", blank=True)

    # Préférences
    preferred_radius = models.IntegerField(default=50, verbose_name="Rayon de recherche (km)")
    receive_newsletter = models.BooleanField(default=True, verbose_name="Recevoir la newsletter")
    profile_visibility = models.CharField(
        max_length=10,
        choices=[("PUBLIC", "Public"), ("PRIVATE", "Privé")],
        default="PUBLIC",
        verbose_name="Visibilité du profil",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bénévole"
        verbose_name_plural = "Bénévoles"
        ordering = ["-total_hours"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.badge_level}"

    def update_badge(self):
        """Met à jour le badge en fonction des heures"""
        if self.total_hours >= 200:
            self.badge_level = "GOLD"
        elif self.total_hours >= 50:
            self.badge_level = "SILVER"
        else:
            self.badge_level = "BRONZE"
        self.save()


class Organization(models.Model):
    """
    Profil Organisation
    """

    ORG_TYPE_CHOICES = [
        ("ASSOCIATION", "Association"),
        ("NGO", "ONG"),
        ("INITIATIVE", "Initiative"),
        ("OTHER", "Autre"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization_profile")
    name = models.CharField(max_length=200, verbose_name="Nom de l'organisation")
    organization_type = models.CharField(
        max_length=20, choices=ORG_TYPE_CHOICES, verbose_name="Type"
    )
    registration_number = models.CharField(
        max_length=100, verbose_name="Numéro d'enregistrement", blank=True
    )
    creation_date = models.DateField(verbose_name="Date de création", null=True, blank=True)

    # Contact
    email = models.EmailField(verbose_name="Email de l'organisation")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    website = models.URLField(verbose_name="Site web", blank=True)

    # Localisation
    wilaya = models.CharField(max_length=2, verbose_name="Wilaya")
    address = models.TextField(verbose_name="Adresse complète")

    # Représentant légal
    representative_name = models.CharField(max_length=200, verbose_name="Nom du responsable")
    representative_position = models.CharField(max_length=100, verbose_name="Fonction")
    representative_email = models.EmailField(verbose_name="Email du responsable")

    # Présentation
    description = models.TextField(verbose_name="Description", validators=[MinLengthValidator(500)])
    mission_values = models.TextField(verbose_name="Mission et valeurs", blank=True)
    logo = models.ImageField(
        upload_to="organizations/logos/", verbose_name="Logo", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="organizations/covers/", verbose_name="Photo de couverture", blank=True, null=True
    )

    # Vérification
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    verification_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Date de vérification"
    )

    # Statistiques
    total_missions = models.IntegerField(default=0, verbose_name="Total missions")
    total_volunteers = models.IntegerField(default=0, verbose_name="Total bénévoles")
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, verbose_name="Note moyenne"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ["-is_verified", "-created_at"]

    def __str__(self):
        return self.name
