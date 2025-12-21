# Guide d'Utilisation de l'API DZ-Volunteer

## 📖 Vue d'ensemble

Cette API REST permet de gérer une plateforme de bénévolat complète avec :
- Gestion des utilisateurs (bénévoles, organisations, admins)
- Gestion des missions
- Système de candidatures
- Validation des compétences
- Système de badges et heures
- 17 Objectifs de Développement Durable (ODD)

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### 1. Inscription Bénévole

```http
POST /api/auth/register/volunteer/
Content-Type: application/json

{
  "email": "benoit@example.com",
  "password": "motdepasse123",
  "password_confirm": "motdepasse123",
  "first_name": "Benoît",
  "last_name": "Dupont",
  "phone": "0555123456"
}
```

**Réponse :**
```json
{
  "user": {
    "id": 1,
    "email": "benoit@example.com",
    "first_name": "Benoît",
    "last_name": "Dupont",
    "user_type": "VOLUNTEER"
  },
  "message": "Inscription réussie !",
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Inscription Organisation

```http
POST /api/auth/register/organization/
Content-Type: application/json

{
  "email": "contact@organisation.dz",
  "password": "motdepasse123",
  "password_confirm": "motdepasse123",
  "name": "Croissant Rouge Algérien",
  "organization_type": "ASSOCIATION",
  "registration_number": "123456",
  "email_org": "info@cra.dz",
  "phone": "0555987654",
  "wilaya": "16",
  "address": "12 Rue Larbi Ben M'hidi, Alger",
  "representative_name": "Ahmed Benali",
  "representative_position": "Président",
  "representative_email": "ahmed@cra.dz",
  "description": "Le Croissant Rouge Algérien est une association humanitaire qui œuvre pour... (min 500 caractères)"
}
```

### 3. Connexion

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "benoit@example.com",
  "password": "motdepasse123"
}
```

**Réponse :**
```json
{
  "user": {
    "id": 1,
    "email": "benoit@example.com",
    "user_type": "VOLUNTEER"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

### 4. Utiliser le Token

Pour toutes les requêtes authentifiées :

```http
GET /api/missions/volunteer/dashboard/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 5. Rafraîchir le Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 🏠 Pages Publiques (Sans Authentification)

### Page d'Accueil - Statistiques

```http
GET /api/missions/home-stats/
```

**Réponse :**
```json
{
  "total_volunteers": 247,
  "total_missions": 56,
  "total_hours": 12450,
  "latest_missions": [
    {
      "id": 1,
      "title": "Distribution alimentaire",
      "organization": {
        "id": 1,
        "name": "Croissant Rouge Algérien",
        "is_verified": true
      },
      "date": "2025-03-15",
      "wilaya": "19",
      "remaining_places": 3,
      "fill_percentage": 70
    }
  ]
}
```

### Liste des Missions (avec filtres)

```http
GET /api/missions/?wilaya=19&odd=1&has_places=true&search=distribution
```

**Paramètres de filtre :**
- `wilaya` : Code wilaya (01-58)
- `odd` : ID de l'ODD
- `mission_type` : ONE_TIME ou RECURRING
- `has_places` : true (missions avec places disponibles)
- `search` : Recherche textuelle
- `ordering` : date, -date, created_at, -created_at

### Détail d'une Mission

```http
GET /api/missions/1/
```

**Réponse :**
```json
{
  "id": 1,
  "title": "Distribution alimentaire - Ramadan 2025",
  "short_description": "Distribution de colis alimentaires...",
  "full_description": "Nous organisons une distribution...",
  "date": "2025-03-15",
  "start_time": "09:00:00",
  "end_time": "13:00:00",
  "duration_hours": "4.00",
  "wilaya": "19",
  "commune": "Sétif",
  "full_address": "Place centrale, El Eulma",
  "organization": {
    "id": 1,
    "name": "Croissant Rouge Algérien",
    "is_verified": true
  },
  "odd": {
    "number": 1,
    "title_fr": "Pas de pauvreté",
    "color": "#E5243B"
  },
  "required_volunteers": 10,
  "accepted_volunteers": 7,
  "remaining_places": 3,
  "fill_percentage": 70,
  "is_full": false,
  "required_skills": [
    {
      "skill": {
        "id": 1,
        "name": "Animation",
        "requires_verification": false
      },
      "verification_required": false
    },
    {
      "skill": {
        "id": 21,
        "name": "Premiers Secours",
        "requires_verification": true
      },
      "verification_required": true
    }
  ]
}
```

### Profil Public Organisation

```http
GET /api/missions/organization/1/
```

### Liste des ODD

```http
GET /api/odd/
```

## 👤 Espace Bénévole

### Tableau de Bord

```http
GET /api/missions/volunteer/dashboard/
Authorization: Bearer {token}
```

**Réponse :**
```json
{
  "profile": {
    "total_hours": 67.5,
    "badge_level": "SILVER",
    "completed_missions": 12,
    "average_rating": 4.8
  },
  "stats": {
    "pending_applications": 2,
    "accepted_missions": 3
  },
  "upcoming_missions": [...],
  "recent_applications": [...]
}
```

### Mon Profil

```http
GET /api/auth/profile/volunteer/
Authorization: Bearer {token}
```

```http
PUT /api/auth/profile/volunteer/
Authorization: Bearer {token}
Content-Type: application/json

{
  "date_of_birth": "1995-05-15",
  "wilaya": "19",
  "commune": "Sétif",
  "motivation": "Je veux aider...",
  "interests": ["ENVIRONMENT", "EDUCATION"],
  "availability": {
    "monday": ["morning", "afternoon"],
    "tuesday": ["evening"]
  }
}
```

### Mes Compétences

```http
GET /api/skills/my-skills/
Authorization: Bearer {token}
```

**Ajouter une compétence :**
```http
POST /api/skills/my-skills/
Authorization: Bearer {token}
Content-Type: multipart/form-data

skill_id=21
document=@certificat_premiers_secours.pdf
```

**Supprimer une compétence :**
```http
DELETE /api/skills/my-skills/5/
Authorization: Bearer {token}
```

### Postuler à une Mission

```http
POST /api/missions/volunteer/apply/1/
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Bonjour, je suis très motivé pour cette mission..."
}
```

**Réponses possibles :**
- ✅ 201 Created : Candidature créée
- ❌ 400 Bad Request : Mission pleine / Compétences manquantes / Déjà postulé
- ❌ 404 Not Found : Mission introuvable

### Mes Candidatures

```http
GET /api/missions/volunteer/applications/?status=PENDING
Authorization: Bearer {token}
```

Filtres : `status=PENDING|ACCEPTED|REJECTED|CANCELLED`

### Mes Missions

```http
GET /api/missions/volunteer/missions/?status=upcoming
Authorization: Bearer {token}
```

Filtres : `status=upcoming|completed|all`

## 🏢 Espace Organisation

### Tableau de Bord

```http
GET /api/missions/organization/dashboard/
Authorization: Bearer {token}
```

### Mes Missions

```http
GET /api/missions/organization/missions/?status=PUBLISHED
Authorization: Bearer {token}
```

### Créer une Mission

```http
POST /api/missions/organization/missions/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Nettoyage de plage",
  "short_description": "Nettoyage de la plage de...",
  "full_description": "Description complète...",
  "mission_type": "ONE_TIME",
  "odd": 14,
  "causes": ["ENVIRONMENT"],
  "date": "2025-04-20",
  "start_time": "08:00:00",
  "end_time": "12:00:00",
  "wilaya": "31",
  "commune": "Oran",
  "full_address": "Plage des Andalouses",
  "meeting_point": "Parking principal",
  "required_volunteers": 20,
  "experience_level": "BEGINNER",
  "status": "PUBLISHED"
}
```

### Candidatures d'une Mission

```http
GET /api/missions/organization/mission/1/applications/?status=PENDING
Authorization: Bearer {token}
```

### Accepter/Refuser une Candidature

```http
POST /api/missions/organization/application/5/respond/
Authorization: Bearer {token}
Content-Type: application/json

{
  "action": "accept",
  "message": "Bienvenue ! Rendez-vous à 9h..."
}
```

ou

```json
{
  "action": "reject",
  "message": "Désolé, toutes les places sont prises."
}
```

### Valider les Heures

```http
POST /api/missions/organization/mission/1/validate-hours/
Authorization: Bearer {token}
Content-Type: application/json

{
  "validations": [
    {
      "participation_id": 1,
      "was_present": true,
      "hours": 4.0,
      "rating": 5,
      "comment": "Excellent travail !"
    },
    {
      "participation_id": 2,
      "was_present": false,
      "hours": 0
    }
  ]
}
```

## 👨‍💼 Espace Admin

### Statistiques Globales

```http
GET /api/missions/admin/stats/
Authorization: Bearer {admin_token}
```

### Compétences en Attente de Validation

```http
GET /api/skills/admin/pending/
Authorization: Bearer {admin_token}
```

### Valider une Compétence

```http
POST /api/skills/admin/validate/5/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "action": "validate"
}
```

ou

```json
{
  "action": "reject",
  "reason": "Document expiré"
}
```

## 📊 Codes d'État HTTP

- `200 OK` : Succès
- `201 Created` : Ressource créée
- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Non authentifié
- `403 Forbidden` : Accès refusé
- `404 Not Found` : Ressource introuvable
- `500 Internal Server Error` : Erreur serveur

## 🔍 Exemples de Scénarios Complets

### Scénario 1 : Bénévole s'inscrit et postule

1. Inscription : `POST /api/auth/register/volunteer/`
2. Connexion : `POST /api/auth/login/`
3. Voir les missions : `GET /api/missions/`
4. Détail d'une mission : `GET /api/missions/1/`
5. Ajouter une compétence : `POST /api/skills/my-skills/`
6. Postuler : `POST /api/missions/volunteer/apply/1/`
7. Voir mes candidatures : `GET /api/missions/volunteer/applications/`

### Scénario 2 : Organisation crée une mission

1. Inscription : `POST /api/auth/register/organization/`
2. Connexion : `POST /api/auth/login/`
3. Créer mission : `POST /api/missions/organization/missions/`
4. Voir candidatures : `GET /api/missions/organization/mission/1/applications/`
5. Accepter candidature : `POST /api/missions/organization/application/1/respond/`
6. Après la mission, valider heures : `POST /api/missions/organization/mission/1/validate-hours/`

### Scénario 3 : Admin valide une compétence

1. Connexion admin : `POST /api/auth/login/`
2. Voir compétences en attente : `GET /api/skills/admin/pending/`
3. Valider : `POST /api/skills/admin/validate/5/`

## 📝 Notes Importantes

1. **Compétences avec vérification** : Le bénévole doit uploader un document ET attendre la validation admin avant de pouvoir postuler aux missions nécessitant cette compétence.

2. **Badges automatiques** : Les badges (Bronze/Argent/Or) sont mis à jour automatiquement après validation des heures.

3. **Pagination** : Par défaut, les listes retournent 10 éléments. Utilisez `?page=2` pour la page suivante.

4. **CORS** : En développement, CORS est activé pour tous les domaines. En production, configurer correctement.

5. **Fichiers** : Pour upload de fichiers (images, documents), utiliser `multipart/form-data`.

## 🐛 Debugging

Pour voir les requêtes et réponses détaillées, activer les logs Django :
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

Pour plus d'informations, consultez le [README.md](README.md) principal.
