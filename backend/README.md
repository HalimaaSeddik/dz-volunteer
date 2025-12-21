# DZ-Volunteer Backend

Backend Django pour la plateforme de bénévolat DZ-Volunteer.

## 🚀 Installation et Configuration

### Prérequis

- Python 3.10+
- PostgreSQL 12+
- pip

### Installation

1. **Créer un environnement virtuel**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. **Installer les dépendances**

```powershell
pip install -r requirements.txt
```

3. **Configurer la base de données PostgreSQL**

Créer la base de données dans PostgreSQL :

```powershell
# Ouvrir psql
psql -U postgres

# Dans psql, créer la base de données
CREATE DATABASE dzvolunteer;

# Quitter psql
\q
```

4. **Configuration des variables d'environnement**

Le fichier `.env` est déjà configuré avec :
- `DB_PASSWORD=20772077`
- `DB_USER=postgres`
- `DB_NAME=dzvolunteer`

5. **Appliquer les migrations**

```powershell
python manage.py makemigrations
python manage.py migrate
```

6. **Initialiser les données de base (ODD et compétences)**

```powershell
python manage.py init_data
```

7. **Créer un super utilisateur**

```powershell
python manage.py createsuperuser
```

8. **Lancer le serveur**

```powershell
python manage.py runserver
```

Le serveur sera accessible sur : http://127.0.0.1:8000/

## 📚 Structure du Projet

```
backend/
├── dzvolunteer/          # Configuration principale
│   ├── settings.py       # Paramètres Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py
│
├── accounts/             # Gestion des utilisateurs
│   ├── models.py         # User, Volunteer, Organization
│   ├── views.py          # Authentification, profils
│   ├── urls.py
│   └── serializers.py
│
├── missions/             # Gestion des missions
│   ├── models.py         # Mission, Application, Participation, Review
│   ├── views.py          # CRUD missions, candidatures
│   ├── urls.py
│   └── admin.py
│
├── skills/               # Gestion des compétences
│   ├── models.py         # Skill, VolunteerSkill
│   ├── views.py          # Validation des compétences
│   └── urls.py
│
├── odd/                  # Objectifs de Développement Durable
│   ├── models.py         # ODD (17 objectifs ONU)
│   ├── views.py
│   └── urls.py
│
├── media/                # Fichiers uploadés
├── static/               # Fichiers statiques
└── requirements.txt      # Dépendances Python
```

## 🔑 API Endpoints

### Authentification

- `POST /api/auth/register/volunteer/` - Inscription bénévole (Page 5)
- `POST /api/auth/register/organization/` - Inscription organisation (Page 5)
- `POST /api/auth/login/` - Connexion (Page 6)
- `POST /api/auth/token/refresh/` - Rafraîchir le token
- `GET/PUT /api/auth/profile/volunteer/` - Profil bénévole (Page 9)
- `GET/PUT /api/auth/profile/organization/` - Profil organisation (Page 22)

### Pages Publiques

- `GET /api/missions/` - Liste des missions (Page 2)
- `GET /api/missions/{id}/` - Détail mission (Page 3)
- `GET /api/missions/organization/{id}/` - Profil public organisation (Page 4)
- `GET /api/missions/home-stats/` - Statistiques page d'accueil (Page 1)
- `GET /api/odd/` - Liste des 17 ODD

### Espace Bénévole

- `GET /api/missions/volunteer/dashboard/` - Tableau de bord (Page 8)
- `POST /api/missions/volunteer/apply/{mission_id}/` - Postuler
- `GET /api/missions/volunteer/applications/` - Mes candidatures (Page 11)
- `GET /api/missions/volunteer/missions/` - Mes missions (Page 12)
- `GET /api/skills/my-skills/` - Mes compétences (Page 10)
- `POST /api/skills/my-skills/` - Ajouter une compétence
- `DELETE /api/skills/my-skills/{id}/` - Supprimer une compétence

### Espace Organisation

- `GET /api/missions/organization/dashboard/` - Tableau de bord (Page 15)
- `GET /api/missions/organization/missions/` - Mes missions (Page 16)
- `POST /api/missions/organization/missions/` - Créer mission (Page 17)
- `GET /api/missions/organization/mission/{id}/applications/` - Candidatures (Page 18)
- `POST /api/missions/organization/application/{id}/respond/` - Accepter/Refuser
- `POST /api/missions/organization/mission/{id}/validate-hours/` - Valider heures (Page 19)

### Espace Admin

- `GET /api/missions/admin/stats/` - Statistiques (Page 23)
- `GET /api/skills/admin/pending/` - Compétences en attente (Page 25)
- `POST /api/skills/admin/validate/{id}/` - Valider compétence

## 🔐 Types d'utilisateurs et Permissions

### VOLUNTEER (Bénévole)
- Voir et postuler aux missions
- Gérer son profil et ses compétences
- Voir ses candidatures et missions

### ORGANIZATION (Organisation)
- Créer et gérer des missions
- Voir et gérer les candidatures
- Valider les heures des bénévoles
- Évaluer les bénévoles

### ADMIN (Administrateur)
- Accès complet à l'interface admin Django
- Valider les compétences nécessitant vérification
- Gérer les utilisateurs et organisations
- Accès aux statistiques globales

## 📊 Modèles Principaux

### User (Utilisateur de base)
- Email (unique, utilisé pour la connexion)
- Type: VOLUNTEER, ORGANIZATION, ou ADMIN
- Informations de contact

### Volunteer (Bénévole)
- Profil lié à User
- Badge (Bronze/Argent/Or selon heures)
- Total heures, missions complétées
- Compétences avec validation
- Note moyenne

### Organization (Organisation)
- Profil lié à User
- Informations légales
- Vérification admin (badge ✓)
- Statistiques (missions, bénévoles, notes)

### Mission
- Créée par une organisation
- ODD et causes associés
- Localisation (wilaya, commune, coordonnées)
- Date, horaires, durée
- Compétences requises (avec/sans vérification)
- Statuts: DRAFT, PUBLISHED, ONGOING, COMPLETED, ARCHIVED

### Application (Candidature)
- Bénévole postule à une mission
- Statuts: PENDING, ACCEPTED, REJECTED, CANCELLED
- Vérification automatique des compétences

### Participation
- Après acceptation de la candidature
- Validation des heures par l'organisation
- Évaluations mutuelles (organisation ⭐ bénévole, bénévole ⭐ organisation)

### Skill (Compétence)
- Compétences générales (validation automatique)
- Compétences avec vérification (nécessite justificatif + validation admin)

### VolunteerSkill
- Lien bénévole-compétence
- Statuts: PENDING, VALIDATED, REJECTED
- Document justificatif si requis

### ODD (Objectifs de Développement Durable)
- 17 objectifs ONU
- Titres FR et AR
- Couleurs officielles
- Liés aux missions

## ⚠️ Contraintes Métier Importantes

### 1. Compétences avec Vérification Obligatoire
Certaines compétences (Premiers Secours, Langue des signes, etc.) nécessitent :
- Upload d'un justificatif par le bénévole
- Validation manuelle par un administrateur
- Seuls les bénévoles avec compétences **VALIDÉES** peuvent postuler aux missions les requérant

### 2. Gestion des Candidatures
- Un bénévole ne peut postuler qu'une fois par mission
- Vérification automatique si le bénévole possède les compétences requises
- Une mission ne peut pas recevoir plus de candidatures que de places disponibles

### 3. Système de Badges
- 🥉 Bronze : 0-49h
- 🥈 Argent : 50-199h
- 🥇 Or : 200h+
- Mis à jour automatiquement après validation des heures

### 4. Validation des Heures
- Seulement après la date de la mission
- Effectuée par l'organisation
- Heures ajoutées automatiquement au compteur du bénévole
- Badge mis à jour automatiquement

## 🔧 Administration Django

Interface admin accessible sur : http://127.0.0.1:8000/admin/

**Fonctionnalités principales :**
- Gestion complète des utilisateurs
- Validation des organisations (badge vérifié)
- Validation des compétences nécessitant justificatif
- Gestion des missions et candidatures
- Statistiques et rapports
- Gestion des ODD

## 🌍 Wilayas d'Algérie

Les 58 wilayas sont configurées dans `settings.py` :
- Utilisées pour la localisation des missions
- Filtres de recherche
- Statistiques géographiques

## 📧 Configuration Email

Par défaut, les emails s'affichent dans la console (développement).

Pour la production, modifier dans `settings.py` :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe'
```

## 🔒 Sécurité

**Pour la production :**
1. Changer `SECRET_KEY` dans `.env`
2. Mettre `DEBUG=False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser HTTPS
5. Configurer CORS correctement

## 📝 Tests

Les tests peuvent être ajoutés dans chaque app :
```powershell
python manage.py test
```

## 🐳 Docker (Optionnel)

Un `docker-compose.yml` est disponible à la racine du projet pour containeriser l'application.

## 📄 Licence

Ce projet est développé pour DZ-Volunteer © 2025

## 🤝 Support

Pour toute question ou problème, consultez la documentation ou contactez l'équipe de développement.

---

**Note importante :** Ce backend implémente toutes les 34 pages décrites dans les spécifications. Le frontend doit consommer ces API REST pour afficher les interfaces utilisateur.
