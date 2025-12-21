-- Script SQL pour vérifier la structure de la base de données DZ-Volunteer
-- À exécuter après les migrations : psql -U postgres dzvolunteer < verify_database.sql

\echo '================================================'
\echo '  DZ-Volunteer - Vérification de la Base de Données'
\echo '================================================'
\echo ''

-- 1. Lister toutes les tables
\echo '1. TABLES CRÉÉES'
\echo '----------------'
\dt

\echo ''
\echo '2. STATISTIQUES'
\echo '---------------'

-- Compter les utilisateurs
SELECT 'Utilisateurs' as table_name, COUNT(*) as count FROM accounts_user
UNION ALL
SELECT 'Bénévoles', COUNT(*) FROM accounts_volunteer
UNION ALL
SELECT 'Organisations', COUNT(*) FROM accounts_organization
UNION ALL
SELECT 'Missions', COUNT(*) FROM missions_mission
UNION ALL
SELECT 'Candidatures', COUNT(*) FROM missions_application
UNION ALL
SELECT 'Participations', COUNT(*) FROM missions_participation
UNION ALL
SELECT 'Compétences', COUNT(*) FROM skills_skill
UNION ALL
SELECT 'ODD', COUNT(*) FROM odd_odd;

\echo ''
\echo '3. STRUCTURE DE LA TABLE USERS'
\echo '-------------------------------'
\d accounts_user

\echo ''
\echo '4. STRUCTURE DE LA TABLE MISSIONS'
\echo '----------------------------------'
\d missions_mission

\echo ''
\echo '5. LISTE DES 17 ODD'
\echo '-------------------'
SELECT number, title_fr, color FROM odd_odd ORDER BY number;

\echo ''
\echo '6. COMPÉTENCES DISPONIBLES'
\echo '--------------------------'
SELECT name, icon, requires_verification FROM skills_skill ORDER BY name;

\echo ''
\echo '7. MISSIONS PUBLIÉES'
\echo '--------------------'
SELECT id, title, date, status, wilaya FROM missions_mission WHERE status = 'PUBLISHED';

\echo ''
\echo '8. INDEXES CRÉÉS'
\echo '----------------'
SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public' ORDER BY tablename, indexname;

\echo ''
\echo '9. TAILLE DE LA BASE DE DONNÉES'
\echo '--------------------------------'
SELECT pg_size_pretty(pg_database_size('dzvolunteer')) as database_size;

\echo ''
\echo '================================================'
\echo '  Vérification terminée !'
\echo '================================================'
