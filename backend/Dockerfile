# Dockerfile pour Backend Django - DZ-Volunteer

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="DZ-Volunteer Team"
LABEL description="Backend Django pour la plateforme de volontariat DZ-Volunteer"

# Variables d'environnement pour Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 django && \
    chown -R django:django /app

USER django

# Collecter les fichiers statiques (sera exécuté au démarrage)
RUN python manage.py collectstatic --noinput || true

# Exposer le port
EXPOSE 8000

# Script de démarrage
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
