"""
Configuration Django pour DZ-Volunteer
"""

from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    # Apps locales
    "accounts",
    "missions",
    "skills",
    "odd",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dzvolunteer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dzvolunteer.wsgi.application"

# Database PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Algiers"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Email Configuration (à configurer selon vos besoins)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Wilayas d'Algérie
WILAYAS = [
    ("01", "Adrar"),
    ("02", "Chlef"),
    ("03", "Laghouat"),
    ("04", "Oum El Bouaghi"),
    ("05", "Batna"),
    ("06", "Béjaïa"),
    ("07", "Biskra"),
    ("08", "Béchar"),
    ("09", "Blida"),
    ("10", "Bouira"),
    ("11", "Tamanrasset"),
    ("12", "Tébessa"),
    ("13", "Tlemcen"),
    ("14", "Tiaret"),
    ("15", "Tizi Ouzou"),
    ("16", "Alger"),
    ("17", "Djelfa"),
    ("18", "Jijel"),
    ("19", "Sétif"),
    ("20", "Saïda"),
    ("21", "Skikda"),
    ("22", "Sidi Bel Abbès"),
    ("23", "Annaba"),
    ("24", "Guelma"),
    ("25", "Constantine"),
    ("26", "Médéa"),
    ("27", "Mostaganem"),
    ("28", "M'Sila"),
    ("29", "Mascara"),
    ("30", "Ouargla"),
    ("31", "Oran"),
    ("32", "El Bayadh"),
    ("33", "Illizi"),
    ("34", "Bordj Bou Arreridj"),
    ("35", "Boumerdès"),
    ("36", "El Tarf"),
    ("37", "Tindouf"),
    ("38", "Tissemsilt"),
    ("39", "El Oued"),
    ("40", "Khenchela"),
    ("41", "Souk Ahras"),
    ("42", "Tipaza"),
    ("43", "Mila"),
    ("44", "Aïn Defla"),
    ("45", "Naâma"),
    ("46", "Aïn Témouchent"),
    ("47", "Ghardaïa"),
    ("48", "Relizane"),
    ("49", "Timimoun"),
    ("50", "Bordj Badji Mokhtar"),
    ("51", "Ouled Djellal"),
    ("52", "Béni Abbès"),
    ("53", "In Salah"),
    ("54", "In Guezzam"),
    ("55", "Touggourt"),
    ("56", "Djanet"),
    ("57", "El M'Ghair"),
    ("58", "El Meniaa"),
]
