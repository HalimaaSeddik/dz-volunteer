# DZ-Volunteer 🇩🇿

Plateforme algérienne de bénévolat connectant des bénévoles avec des organisations pour des missions alignées aux 17 Objectifs de Développement Durable de l'ONU.

## 🌟 À Propos

DZ-Volunteer est une plateforme web complète permettant de :
- Mettre en relation des **bénévoles** avec des **organisations** 
- Publier et rechercher des **missions de bénévolat**
- Gérer les **candidatures** et **participations**
- Valider les **compétences** (avec système de vérification)
- Suivre les **heures de bénévolat** et attribuer des **badges**
- Contribuer aux **17 ODD de l'ONU**

## 🏗️ Architecture

```
dz-volunteer/
├── backend/          # API Django REST Framework + PostgreSQL
├── frontend/         # Interface utilisateur (à développer)
├── docs/            # Documentation
└── docker-compose.yml
```

## 🚀 Démarrage Rapide

### Backend (Django)

```powershell
cd backend

# Installation automatique
.\setup.ps1

# OU installation manuelle
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py init_data
python manage.py runserver
```

📖 **Documentation complète** : [backend/README.md](backend/README.md)

### Frontend (En cours de développement)

```powershell
cd frontend/dz-volunter
npm install
npm run dev
```

## 📊 Fonctionnalités Principales

### 👤 Pour les Bénévoles
- ✅ Inscription et profil personnalisé
- 🔍 Recherche de missions (par localisation, ODD, compétences)
- 📝 Candidature en 1 clic
- ⏰ Suivi des heures et badges (Bronze, Argent, Or)
- 🛠️ Gestion des compétences avec validation
- 📅 Calendrier des missions

### 🏢 Pour les Organisations
- ✅ Inscription et vérification
- ➕ Publication de missions
- 👥 Gestion des candidatures
- ✅ Validation des heures
- ⭐ Système d'évaluation
- 📊 Statistiques et rapports

### 👨‍💼 Pour les Administrateurs
- 🔐 Interface d'administration complète
- ✅ Validation des compétences vérifiées
- 🏢 Vérification des organisations
- 📊 Statistiques globales
- 🎯 Gestion des 17 ODD

## 🎯 Objectifs de Développement Durable

La plateforme intègre les **17 ODD de l'ONU** :
- 🎨 Couleurs officielles
- 🌍 Traductions FR/AR
- 📊 Statistiques par ODD
- 🔗 Liaison avec les missions

## 🔐 Système de Compétences

### Compétences Standard
Validation automatique : Animation, Informatique, Cuisine, etc.

### Compétences Vérifiées ⚠️
Nécessitent un justificatif + validation admin :
- 🚑 Premiers Secours
- 🧏 Langue des signes
- 🧠 Psychologie
- 💉 Soins infirmiers
- etc.

## 🏆 Système de Badges

- 🥉 **Bronze** : 0-49 heures
- 🥈 **Argent** : 50-199 heures
- 🥇 **Or** : 200+ heures

Mise à jour automatique après validation des heures.

## 🌍 Couverture Géographique

**58 wilayas d'Algérie** intégrées avec :
- Filtres de recherche
- Localisation des missions
- Statistiques par wilaya

## 🛠️ Technologies

### Backend
- **Framework** : Django 5.0 + Django REST Framework
- **Base de données** : PostgreSQL 12+
- **Authentification** : JWT (JSON Web Tokens)
- **API** : REST
- **Langage** : Python 3.10+

### Frontend (À intégrer)
- React / Vue / Angular
- Consommation API REST
- Responsive design

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](backend/QUICKSTART.md) | Guide de démarrage rapide |
| [README.md](backend/README.md) | Documentation technique backend |
| [API_GUIDE.md](backend/API_GUIDE.md) | Guide complet de l'API |
| [DATABASE_SETUP.md](backend/DATABASE_SETUP.md) | Configuration PostgreSQL |

## 🔗 API Endpoints

Base URL : `http://127.0.0.1:8000/api/`

### Principales routes
```
POST   /auth/register/volunteer/                  # Inscription bénévole
POST   /auth/register/organization/               # Inscription organisation
POST   /auth/login/                              # Connexion
GET    /missions/                                 # Liste des missions
GET    /missions/{id}/                            # Détail mission
POST   /missions/volunteer/apply/{id}/            # Postuler
GET    /missions/volunteer/dashboard/             # Dashboard bénévole
POST   /missions/organization/missions/           # Créer mission
GET    /odd/                                      # Liste des 17 ODD
```

📖 **Documentation complète** : [API_GUIDE.md](backend/API_GUIDE.md)

## 🧪 Tests

### Données de test incluses

```powershell
cd backend
python manage.py shell < create_test_data.py
```

Crée :
- 1 admin : `admin@dzvolunteer.dz` / `admin123`
- 3 bénévoles (Bronze, Argent, Or)
- 2 organisations vérifiées
- 3 missions publiées

## 📄 Pages Implémentées (34 pages)

### Pages Publiques (7)
- Page d'accueil avec statistiques
- Catalogue des missions avec filtres avancés
- Détail d'une mission
- Profil public d'une organisation
- Inscription (bénévole/organisation)
- Connexion
- Récupération mot de passe

### Espace Bénévole (7)
- Tableau de bord
- Rechercher des missions
- Mes candidatures
- Mes missions
- Mon calendrier
- Mon profil
- Mes compétences

### Espace Organisation (8)
- Tableau de bord
- Mes missions
- Créer/Modifier une mission
- Candidatures d'une mission
- Validation des heures
- Statistiques
- Avis et notes
- Profil public

### Espace Admin (6)
- Dashboard
- Gestion des utilisateurs
- Validation des compétences ⚠️
- Gestion des organisations
- Gestion des missions
- Statistiques globales

### Autres (3)
- CGU / Mentions légales
- FAQ / Aide
- Contact

## 🔒 Sécurité

- ✅ Authentification JWT
- ✅ Permissions par rôle (Bénévole, Organisation, Admin)
- ✅ Validation des données
- ✅ Protection CSRF
- ✅ Hashage des mots de passe (PBKDF2)
- ✅ CORS configurable

## 🚀 Déploiement

### Développement
```powershell
python manage.py runserver
```

### Production
Voir [backend/README.md](backend/README.md) pour :
- Configuration HTTPS
- Variables d'environnement
- Gunicorn/uWSGI
- Nginx
- Docker

## 📈 Roadmap

- [x] Backend API complet
- [x] Authentification et permissions
- [x] Gestion des utilisateurs
- [x] Système de missions et candidatures
- [x] Validation des compétences
- [x] Système de badges
- [x] 17 ODD intégrés
- [ ] Frontend React/Vue
- [ ] Système de messagerie
- [ ] Notifications email/push
- [ ] Export PDF des certificats
- [ ] Application mobile
- [ ] Paiement pour dons

## 🤝 Contribution

Ce projet est en cours de développement. Les contributions sont les bienvenues !

## 📞 Contact

- **Email** : contact@dz-volunteer.dz
- **Site web** : www.dz-volunteer.dz

## 📄 Licence

© 2025 DZ-Volunteer. Tous droits réservés.

## 🙏 Remerciements

- ONU pour les 17 Objectifs de Développement Durable
- Django et Django REST Framework
- PostgreSQL
- Toutes les organisations de bénévolat en Algérie

---

**Fait avec ❤️ pour l'Algérie 🇩🇿**
