# Script de démarrage rapide
Write-Host "Démarrage du serveur DZ-Volunteer..." -ForegroundColor Cyan

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Lancer le serveur
python manage.py runserver
