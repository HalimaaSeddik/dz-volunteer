# 🔗 Mapping Frontend → Backend API

Ce document facilite l'intégration entre le frontend et le backend en mappant chaque page aux endpoints API correspondants.

## Base URL
```
http://127.0.0.1:8000/api
```

---

## 📄 PAGES PUBLIQUES

### Page 1 : Page d'Accueil
**Endpoint :** `GET /missions/home-stats/`
```javascript
// Récupère : total_volunteers, total_missions, total_hours, latest_missions
fetch('http://127.0.0.1:8000/api/missions/home-stats/')
```

### Page 2 : Catalogue des Missions
**Endpoint :** `GET /missions/?wilaya=19&odd=1&search=...`
```javascript
// Filtres disponibles : wilaya, odd, mission_type, has_places, search, ordering
fetch('http://127.0.0.1:8000/api/missions/?wilaya=19&has_places=true')
```

### Page 3 : Détail d'une Mission
**Endpoint :** `GET /missions/{id}/`
```javascript
fetch('http://127.0.0.1:8000/api/missions/1/')
```

### Page 4 : Profil Public Organisation
**Endpoint :** `GET /missions/organization/{id}/`
```javascript
fetch('http://127.0.0.1:8000/api/missions/organization/1/')
```

### Page 5 : Inscription
**Bénévole :** `POST /auth/register/volunteer/`
```javascript
fetch('http://127.0.0.1:8000/api/auth/register/volunteer/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@email.com',
    password: 'password123',
    password_confirm: 'password123',
    first_name: 'John',
    last_name: 'Doe',
    phone: '0555123456'
  })
})
```

**Organisation :** `POST /auth/register/organization/`

### Page 6 : Connexion
**Endpoint :** `POST /auth/login/`
```javascript
fetch('http://127.0.0.1:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@email.com',
    password: 'password123'
  })
})
.then(res => res.json())
.then(data => {
  // Stocker le token
  localStorage.setItem('token', data.tokens.access);
  localStorage.setItem('userType', data.user.user_type);
})
```

---

## 👤 ESPACE BÉNÉVOLE

**Note :** Toutes ces requêtes nécessitent le token JWT :
```javascript
headers: {
  'Authorization': `Bearer ${localStorage.getItem('token')}`
}
```

### Page 8 : Tableau de Bord
**Endpoint :** `GET /missions/volunteer/dashboard/`
```javascript
// Retourne : profile, stats, upcoming_missions, recent_applications
```

### Page 9 : Mon Profil
**GET/PUT :** `/auth/profile/volunteer/`
```javascript
// GET : Récupérer le profil
fetch('http://127.0.0.1:8000/api/auth/profile/volunteer/', {
  headers: { 'Authorization': `Bearer ${token}` }
})

// PUT : Modifier le profil
fetch('http://127.0.0.1:8000/api/auth/profile/volunteer/', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    wilaya: '19',
    commune: 'Sétif',
    motivation: 'Je veux aider...'
  })
})
```

### Page 10 : Mes Compétences
**Liste :** `GET /skills/my-skills/`
**Ajouter :** `POST /skills/my-skills/`
**Supprimer :** `DELETE /skills/my-skills/{id}/`
```javascript
// Ajouter une compétence
const formData = new FormData();
formData.append('skill_id', 21); // Premiers Secours
formData.append('document', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/skills/my-skills/', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
})
```

### Page 11 : Mes Candidatures
**Endpoint :** `GET /missions/volunteer/applications/?status=PENDING`
```javascript
// Filtres : status=PENDING|ACCEPTED|REJECTED|CANCELLED
```

### Page 12 : Mes Missions
**Endpoint :** `GET /missions/volunteer/missions/?status=upcoming`
```javascript
// Filtres : status=upcoming|completed|all
```

### Postuler à une Mission
**Endpoint :** `POST /missions/volunteer/apply/{mission_id}/`
```javascript
fetch('http://127.0.0.1:8000/api/missions/volunteer/apply/1/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Je suis très motivé !'
  })
})
```

---

## 🏢 ESPACE ORGANISATION

### Page 15 : Tableau de Bord
**Endpoint :** `GET /missions/organization/dashboard/`

### Page 16 : Mes Missions
**Liste :** `GET /missions/organization/missions/?status=PUBLISHED`
**Filtres :** status=DRAFT|PUBLISHED|ONGOING|COMPLETED|ARCHIVED

### Page 17 : Créer une Mission
**Endpoint :** `POST /missions/organization/missions/`
```javascript
fetch('http://127.0.0.1:8000/api/missions/organization/missions/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Nouvelle mission',
    short_description: 'Description courte',
    full_description: 'Description complète',
    mission_type: 'ONE_TIME',
    odd: 1,
    causes: ['SOCIAL'],
    date: '2025-04-01',
    start_time: '09:00:00',
    end_time: '13:00:00',
    wilaya: '16',
    commune: 'Alger',
    full_address: 'Adresse',
    meeting_point: 'Point de rencontre',
    required_volunteers: 10,
    status: 'PUBLISHED'
  })
})
```

### Page 18 : Candidatures d'une Mission
**Endpoint :** `GET /missions/organization/mission/{mission_id}/applications/?status=PENDING`

### Accepter/Refuser une Candidature
**Endpoint :** `POST /missions/organization/application/{application_id}/respond/`
```javascript
// Accepter
fetch('http://127.0.0.1:8000/api/missions/organization/application/5/respond/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    action: 'accept',
    message: 'Bienvenue !'
  })
})

// Refuser
body: JSON.stringify({
  action: 'reject',
  message: 'Désolé...'
})
```

### Page 19 : Valider les Heures
**Endpoint :** `POST /missions/organization/mission/{mission_id}/validate-hours/`
```javascript
fetch('http://127.0.0.1:8000/api/missions/organization/mission/1/validate-hours/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    validations: [
      {
        participation_id: 1,
        was_present: true,
        hours: 4.0,
        rating: 5,
        comment: 'Excellent !'
      },
      {
        participation_id: 2,
        was_present: false
      }
    ]
  })
})
```

---

## 👨‍💼 ESPACE ADMIN

### Page 23 : Statistiques
**Endpoint :** `GET /missions/admin/stats/`

### Page 25 : Validation des Compétences
**Liste en attente :** `GET /skills/admin/pending/`
**Valider :** `POST /skills/admin/validate/{skill_id}/`
```javascript
// Valider
fetch('http://127.0.0.1:8000/api/skills/admin/validate/5/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ action: 'validate' })
})

// Refuser
body: JSON.stringify({
  action: 'reject',
  reason: 'Document invalide'
})
```

---

## 🔐 Gestion des Tokens

### Rafraîchir le Token
**Endpoint :** `POST /auth/token/refresh/`
```javascript
fetch('http://127.0.0.1:8000/api/auth/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh: localStorage.getItem('refreshToken')
  })
})
.then(res => res.json())
.then(data => {
  localStorage.setItem('token', data.access);
})
```

### Intercepteur Axios (Exemple)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

// Ajouter le token à chaque requête
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Gérer l'expiration du token
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Token expiré, essayer de le rafraîchir
      const refresh = localStorage.getItem('refreshToken');
      if (refresh) {
        try {
          const { data } = await axios.post(
            'http://127.0.0.1:8000/api/auth/token/refresh/',
            { refresh }
          );
          localStorage.setItem('token', data.access);
          // Réessayer la requête
          error.config.headers.Authorization = `Bearer ${data.access}`;
          return axios(error.config);
        } catch {
          // Refresh invalide, déconnecter
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🎯 ODD et Compétences

### Liste des ODD
**Endpoint :** `GET /odd/`
```javascript
// Retourne les 17 ODD avec numéro, titre_fr, titre_ar, color
```

### Liste des Compétences
**Endpoint :** `GET /skills/`
```javascript
// Retourne toutes les compétences avec requires_verification
```

---

## 📤 Upload de Fichiers

Pour les photos de profil, logos, documents :
```javascript
const formData = new FormData();
formData.append('profile_picture', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/auth/profile/volunteer/', {
  method: 'PUT',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData // Pas de Content-Type, le navigateur le définit automatiquement
})
```

---

## ⚠️ Gestion des Erreurs

### Structure des erreurs
```json
{
  "error": "Message d'erreur",
  "detail": "Détails supplémentaires"
}
```

### Codes HTTP courants
- `200` : Succès (GET)
- `201` : Créé (POST)
- `400` : Données invalides
- `401` : Non authentifié
- `403` : Accès refusé
- `404` : Introuvable
- `500` : Erreur serveur

---

## 🔄 Pagination

Les listes sont paginées (10 éléments par page par défaut) :
```javascript
fetch('http://127.0.0.1:8000/api/missions/?page=2')
```

**Réponse :**
```json
{
  "count": 42,
  "next": "http://127.0.0.1:8000/api/missions/?page=3",
  "previous": "http://127.0.0.1:8000/api/missions/?page=1",
  "results": [...]
}
```

---

## 🧪 Tests

Collection Postman disponible : `DZ-Volunteer.postman_collection.json`

---

Ce mapping complet facilite le développement du frontend en fournissant tous les endpoints nécessaires pour chaque page.
