# 🚀 GUIDE DE DÉMARRAGE RAPIDE - DZ-Volunteer Backend

## ⚡ Installation en 5 Minutes

### 1️⃣ Prérequis
- ✅ Python 3.10+ installé
- ✅ PostgreSQL installé (mot de passe: `20772077`)
- ✅ PostgreSQL démarré

### 2️⃣ Installation Automatique

```powershell
cd backend
.\setup.ps1
```

Le script va automatiquement :
- Créer l'environnement virtuel
- Installer les dépendances
- Appliquer les migrations
- Initialiser les données (17 ODD + compétences)
- Créer un superutilisateur
- Lancer le serveur

### 3️⃣ Installation Manuelle (Alternative)

```powershell
# 1. Créer la base de données
psql -U postgres -c "CREATE DATABASE dzvolunteer;"

# 2. Environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# 3. Dépendances
pip install -r requirements.txt

# 4. Migrations
python manage.py migrate

# 5. Données de base
python manage.py init_data

# 6. Superutilisateur
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

## 🎯 URLs Importantes

- **API** : http://127.0.0.1:8000/api/
- **Admin** : http://127.0.0.1:8000/admin/
- **Missions** : http://127.0.0.1:8000/api/missions/
- **ODD** : http://127.0.0.1:8000/api/odd/

## 🧪 Données de Test (Optionnel)

Pour tester rapidement l'application :

```powershell
python manage.py shell < create_test_data.py
```

Cela crée :
- 1 admin
- 3 bénévoles (Bronze, Argent, Or)
- 2 organisations vérifiées
- 3 missions publiées

**Comptes créés :**
- Admin : `admin@dzvolunteer.dz` / `admin123`
- Bénévole : `amira.benali@email.dz` / `password123`
- Organisation : `contact@cra.dz` / `password123`

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| [README.md](README.md) | Documentation complète du projet |
| [API_GUIDE.md](API_GUIDE.md) | Guide d'utilisation de l'API avec exemples |
| [DATABASE_SETUP.md](DATABASE_SETUP.md) | Configuration PostgreSQL détaillée |

## 🏗️ Structure du Projet

```
backend/
├── dzvolunteer/          # Configuration Django
├── accounts/             # Utilisateurs, bénévoles, organisations
├── missions/             # Missions, candidatures, participations
├── skills/               # Compétences avec validation
├── odd/                  # 17 Objectifs de Développement Durable
├── media/                # Fichiers uploadés
├── requirements.txt      # Dépendances
├── manage.py            # Commandes Django
├── setup.ps1            # Installation automatique
└── start.ps1            # Démarrage rapide
```

## 🔑 API Endpoints Principaux

### Authentification
```
POST /api/auth/register/volunteer/      # Inscription bénévole
POST /api/auth/register/organization/   # Inscription organisation
POST /api/auth/login/                   # Connexion
```

### Pages Publiques
```
GET /api/missions/                      # Liste des missions
GET /api/missions/{id}/                 # Détail mission
GET /api/missions/home-stats/           # Statistiques accueil
GET /api/odd/                           # Liste des ODD
```

### Espace Bénévole
```
GET /api/missions/volunteer/dashboard/           # Tableau de bord
POST /api/missions/volunteer/apply/{id}/         # Postuler
GET /api/missions/volunteer/applications/        # Mes candidatures
GET /api/skills/my-skills/                       # Mes compétences
```

### Espace Organisation
```
GET /api/missions/organization/dashboard/                    # Tableau de bord
POST /api/missions/organization/missions/                    # Créer mission
GET /api/missions/organization/mission/{id}/applications/    # Candidatures
POST /api/missions/organization/application/{id}/respond/    # Accepter/Refuser
```

### Espace Admin
```
GET /api/missions/admin/stats/              # Statistiques
GET /api/skills/admin/pending/              # Compétences en attente
POST /api/skills/admin/validate/{id}/       # Valider compétence
```

## 📊 Modèles de Données

### User (Utilisateur)
- Types : VOLUNTEER, ORGANIZATION, ADMIN
- Authentification par email

### Volunteer (Bénévole)
- Badge : Bronze (0-49h), Argent (50-199h), Or (200h+)
- Compétences avec validation
- Statistiques : heures, missions, notes

### Organization (Organisation)
- Vérification admin (badge ✓)
- Statistiques : missions, bénévoles

### Mission
- Statuts : DRAFT, PUBLISHED, ONGOING, COMPLETED
- ODD associé
- Compétences requises (avec/sans vérification)
- Localisation (58 wilayas)

### Application (Candidature)
- Statuts : PENDING, ACCEPTED, REJECTED
- Vérification automatique des compétences

### Skill (Compétence)
- Compétences générales (validation auto)
- Compétences vérifiées (justificatif + validation admin)

## ⚙️ Commandes Utiles

```powershell
# Démarrer le serveur
python manage.py runserver

# Créer un admin
python manage.py createsuperuser

# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell Django
python manage.py shell

# Initialiser les données
python manage.py init_data

# Tests
python manage.py test
```

## 🔒 Sécurité

Pour la production :
1. Changer `SECRET_KEY` dans `.env`
2. Mettre `DEBUG=False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser un mot de passe PostgreSQL fort
5. Activer HTTPS
6. Configurer CORS correctement

## 🐛 Dépannage

### Erreur : "database does not exist"
```powershell
psql -U postgres -c "CREATE DATABASE dzvolunteer;"
```

### Erreur : "password authentication failed"
Vérifier le mot de passe dans `.env` : `20772077`

### Erreur : "could not connect to server"
Vérifier que PostgreSQL est démarré :
```powershell
Get-Service postgresql*
```

### Port 8000 déjà utilisé
```powershell
python manage.py runserver 8001
```

## 📖 Exemples d'Utilisation

### 1. S'inscrire et postuler (Bénévole)

```bash
# Inscription
curl -X POST http://127.0.0.1:8000/api/auth/register/volunteer/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@email.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Connexion
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@email.com",
    "password": "password123"
  }'

# Voir les missions
curl http://127.0.0.1:8000/api/missions/

# Postuler (avec token)
curl -X POST http://127.0.0.1:8000/api/missions/volunteer/apply/1/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Je suis motivé!"}'
```

### 2. Créer une mission (Organisation)

```bash
# Connexion
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "contact@cra.dz",
    "password": "password123"
  }'

# Créer mission
curl -X POST http://127.0.0.1:8000/api/missions/organization/missions/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nouvelle mission",
    "short_description": "Description courte",
    "full_description": "Description complète...",
    "mission_type": "ONE_TIME",
    "odd": 1,
    "date": "2025-04-01",
    "start_time": "09:00:00",
    "end_time": "13:00:00",
    "wilaya": "16",
    "commune": "Alger",
    "full_address": "Adresse complète",
    "required_volunteers": 10,
    "status": "PUBLISHED"
  }'
```

## 🎉 C'est Prêt !

Le backend est maintenant fonctionnel et prêt à être utilisé par le frontend.

**Prochaines étapes :**
1. Développer le frontend (React/Vue/Angular)
2. Consommer les API REST
3. Tester les fonctionnalités
4. Déployer en production

**Support :**
- Documentation complète : [README.md](README.md)
- Guide API : [API_GUIDE.md](API_GUIDE.md)
- Configuration BDD : [DATABASE_SETUP.md](DATABASE_SETUP.md)

---

**DZ-Volunteer © 2025** - Plateforme algérienne de bénévolat
