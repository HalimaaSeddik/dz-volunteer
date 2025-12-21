# Configuration de la Base de Données PostgreSQL

## 🗄️ Création de la Base de Données

### Option 1 : Via psql (Ligne de commande)

1. **Ouvrir PostgreSQL**

```powershell
psql -U postgres
```

Entrez le mot de passe : `20772077`

2. **Créer la base de données**

```sql
CREATE DATABASE dzvolunteer;
```

3. **Vérifier la création**

```sql
\l
```

Vous devriez voir `dzvolunteer` dans la liste.

4. **Quitter psql**

```sql
\q
```

### Option 2 : Via pgAdmin (Interface graphique)

1. Ouvrir **pgAdmin 4**
2. Se connecter au serveur PostgreSQL (mot de passe: `20772077`)
3. Clic droit sur "Databases" → "Create" → "Database..."
4. Nom : `dzvolunteer`
5. Owner : `postgres`
6. Cliquer sur "Save"

### Option 3 : Via le Terminal PowerShell

```powershell
# Se connecter et créer la base en une commande
psql -U postgres -c "CREATE DATABASE dzvolunteer;"
```

## ✅ Vérification de la Connexion

Pour tester si Django peut se connecter à la base :

```powershell
cd backend
python manage.py check --database default
```

Si tout est correct, vous verrez :
```
System check identified no issues (0 silenced).
```

## 🔧 Configuration dans Django

Le fichier `.env` est déjà configuré :

```env
DB_NAME=dzvolunteer
DB_USER=postgres
DB_PASSWORD=20772077
DB_HOST=localhost
DB_PORT=5432
```

Ces paramètres sont automatiquement chargés dans `settings.py`.

## 📊 Structure de la Base de Données

Après les migrations, Django créera automatiquement les tables suivantes :

### Tables Principales

- **accounts_user** : Utilisateurs (email, type, mot de passe)
- **accounts_volunteer** : Profils bénévoles (heures, badge, statistiques)
- **accounts_organization** : Profils organisations (infos légales, vérification)
- **missions_mission** : Missions (titre, date, lieu, ODD)
- **missions_application** : Candidatures (bénévole → mission)
- **missions_participation** : Participations effectives (validation heures)
- **skills_skill** : Compétences disponibles
- **skills_volunteerskill** : Compétences des bénévoles (avec validation)
- **odd_odd** : 17 Objectifs de Développement Durable

### Tables de Liaison

- **missions_missionskillrequirement** : Compétences requises par mission
- **missions_review** : Avis des bénévoles sur les organisations
- **missions_report** : Signalements

### Tables Django Standard

- **auth_permission**, **auth_group** : Permissions
- **django_session** : Sessions
- **django_admin_log** : Logs admin
- **django_content_type** : Types de contenu

## 🚀 Migrations

### Créer les migrations

```powershell
python manage.py makemigrations
```

Cela crée les fichiers de migration dans chaque app :
- `accounts/migrations/0001_initial.py`
- `missions/migrations/0001_initial.py`
- `skills/migrations/0001_initial.py`
- `odd/migrations/0001_initial.py`

### Appliquer les migrations

```powershell
python manage.py migrate
```

Résultat attendu :
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying missions.0001_initial... OK
  Applying skills.0001_initial... OK
  Applying odd.0001_initial... OK
  Applying sessions.0001_initial... OK
  ...
```

### Voir les migrations appliquées

```powershell
python manage.py showmigrations
```

## 📥 Initialisation des Données

Après les migrations, initialisez les données de base :

```powershell
python manage.py init_data
```

Cela va créer :
- ✅ Les 17 ODD avec leurs couleurs officielles
- ✅ Les compétences de base (27 compétences)
- ✅ Les compétences nécessitant vérification

## 🔍 Inspection de la Base de Données

### Via psql

```powershell
psql -U postgres dzvolunteer
```

Commandes utiles :

```sql
-- Liste des tables
\dt

-- Structure d'une table
\d accounts_user

-- Nombre d'utilisateurs
SELECT COUNT(*) FROM accounts_user;

-- Liste des ODD
SELECT number, title_fr, color FROM odd_odd ORDER BY number;

-- Missions publiées
SELECT title, date FROM missions_mission WHERE status = 'PUBLISHED';
```

### Via Django Shell

```powershell
python manage.py shell
```

```python
# Compter les utilisateurs
from accounts.models import User
User.objects.count()

# Voir les ODD
from odd.models import ODD
ODD.objects.all()

# Voir les compétences
from skills.models import Skill
Skill.objects.filter(requires_verification=True)
```

## 🔄 Réinitialisation de la Base de Données

Si vous voulez repartir de zéro :

```powershell
# Supprimer la base
psql -U postgres -c "DROP DATABASE dzvolunteer;"

# Recréer la base
psql -U postgres -c "CREATE DATABASE dzvolunteer;"

# Réappliquer les migrations
python manage.py migrate

# Réinitialiser les données
python manage.py init_data
```

## 🛡️ Backup et Restore

### Créer un backup

```powershell
pg_dump -U postgres -F c dzvolunteer > backup.dump
```

### Restaurer un backup

```powershell
pg_restore -U postgres -d dzvolunteer backup.dump
```

## ⚠️ Problèmes Courants

### Erreur : "database does not exist"

**Solution :** Créer la base avec `CREATE DATABASE dzvolunteer;`

### Erreur : "password authentication failed"

**Solution :** Vérifier le mot de passe dans `.env` (doit être `20772077`)

### Erreur : "could not connect to server"

**Solution :** Vérifier que PostgreSQL est démarré :

```powershell
# Windows Service
Get-Service -Name postgresql*
```

Si arrêté :
```powershell
Start-Service postgresql-x64-XX
```

### Erreur : "role postgres does not exist"

**Solution :** Le superuser `postgres` doit exister. Vérifier avec pgAdmin.

### Port 5432 déjà utilisé

**Solution :** Modifier le port dans `.env` et relancer PostgreSQL sur un autre port.

## 📊 Indexes et Optimisations

Django crée automatiquement des indexes sur :
- Clés primaires (id)
- Clés étrangères
- Champs avec `unique=True`
- Champs avec `db_index=True`

Des indexes personnalisés sont définis dans les modèles :

```python
class Meta:
    indexes = [
        models.Index(fields=['status', 'date']),
        models.Index(fields=['wilaya', 'status']),
    ]
```

## 🔒 Sécurité

### En Production

1. **Changer le mot de passe** : Utiliser un mot de passe fort
2. **Restreindre les connexions** : Modifier `pg_hba.conf`
3. **SSL** : Activer les connexions SSL
4. **Backup réguliers** : Automatiser les backups

### Permissions

```sql
-- Créer un utilisateur spécifique pour l'app (recommandé en production)
CREATE USER dzv_app WITH PASSWORD 'motdepasse_securise';
GRANT ALL PRIVILEGES ON DATABASE dzvolunteer TO dzv_app;
```

Puis mettre à jour `.env` :
```env
DB_USER=dzv_app
DB_PASSWORD=motdepasse_securise
```

## 📈 Monitoring

Pour voir les connexions actives :

```sql
SELECT * FROM pg_stat_activity WHERE datname = 'dzvolunteer';
```

Pour voir la taille de la base :

```sql
SELECT pg_size_pretty(pg_database_size('dzvolunteer'));
```

---

La base de données est maintenant prête pour DZ-Volunteer ! 🎉
