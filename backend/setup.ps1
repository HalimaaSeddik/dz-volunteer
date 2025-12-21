# Script de configuration et démarrage du backend DZ-Volunteer

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  DZ-Volunteer Backend Setup     " -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 1. Vérifier si l'environnement virtuel existe
if (-Not (Test-Path "venv")) {
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Environnement virtuel créé" -ForegroundColor Green
} else {
    Write-Host "✓ Environnement virtuel existe déjà" -ForegroundColor Green
}

# 2. Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# 3. Installer les dépendances
Write-Host "Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt

# 4. Vérifier la connexion PostgreSQL
Write-Host ""
Write-Host "Vérification de la connexion PostgreSQL..." -ForegroundColor Yellow
Write-Host "Base de données: dzvolunteer" -ForegroundColor Cyan
Write-Host "Utilisateur: postgres" -ForegroundColor Cyan
Write-Host "Mot de passe: 20772077" -ForegroundColor Cyan
Write-Host ""

# 5. Créer la base de données si elle n'existe pas
Write-Host "IMPORTANT: Assurez-vous que PostgreSQL est démarré" -ForegroundColor Yellow
Write-Host "et que la base de données 'dzvolunteer' existe." -ForegroundColor Yellow
Write-Host ""
$continue = Read-Host "Continuer? (O/N)"

if ($continue -ne "O" -and $continue -ne "o") {
    Write-Host "Installation annulée" -ForegroundColor Red
    exit
}

# 6. Créer les migrations
Write-Host ""
Write-Host "Création des migrations..." -ForegroundColor Yellow
python manage.py makemigrations

# 7. Appliquer les migrations
Write-Host "Application des migrations..." -ForegroundColor Yellow
python manage.py migrate

# 8. Initialiser les données de base
Write-Host ""
Write-Host "Initialisation des données (ODD, compétences)..." -ForegroundColor Yellow
python manage.py init_data

# 9. Créer un superutilisateur
Write-Host ""
Write-Host "Voulez-vous créer un superutilisateur (admin)? (O/N)" -ForegroundColor Yellow
$createSuperuser = Read-Host

if ($createSuperuser -eq "O" -or $createSuperuser -eq "o") {
    python manage.py createsuperuser
}

# 10. Succès
Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "  Installation terminée! ✓       " -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Pour démarrer le serveur:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "URLs importantes:" -ForegroundColor Cyan
Write-Host "  API: http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host "  Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""

# Demander si on lance le serveur
$runServer = Read-Host "Lancer le serveur maintenant? (O/N)"

if ($runServer -eq "O" -or $runServer -eq "o") {
    Write-Host ""
    Write-Host "Démarrage du serveur..." -ForegroundColor Green
    Write-Host "Appuyez sur CTRL+C pour arrêter" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver
}
