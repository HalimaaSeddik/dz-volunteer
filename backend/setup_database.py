"""
Script d'initialisation de la base de données PostgreSQL pour DZ-Volunteer
Ce script crée la base de données et initialise les données de base
"""
import os
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dz_volunteer.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from odds.models import ODD
from competences.models import Competence

def create_database():
    """Créer la base de données PostgreSQL"""
    print("1. Création de la base de données PostgreSQL...")
    
    try:
        # Connexion à PostgreSQL (sans spécifier de DB)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="20772077"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Créer la base de données
        try:
            cursor.execute("CREATE DATABASE dz_volunteer;")
            print("✅ Base de données 'dz_volunteer' créée")
        except psycopg2.errors.DuplicateDatabase:
            print("📝 Base de données 'dz_volunteer' existe déjà")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"❌ Erreur création base de données: {e}")
        print("💡 Vérifiez que PostgreSQL est installé et démarré")
        return False

def migrate_database():
    """Appliquer les migrations Django"""
    print("2. Application des migrations...")
    
    try:
        # Créer les migrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
        execute_from_command_line(['manage.py', 'makemigrations', 'missions'])
        execute_from_command_line(['manage.py', 'makemigrations', 'applications'])
        execute_from_command_line(['manage.py', 'makemigrations', 'competences'])
        execute_from_command_line(['manage.py', 'makemigrations', 'odds'])
        
        # Appliquer les migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations appliquées")
        return True
    except Exception as e:
        print(f"❌ Erreur migrations: {e}")
        return False

def create_superuser():
    """Créer un super utilisateur pour l'admin Django"""
    print("3. Création du super utilisateur...")
    
    User = get_user_model()
    
    if not User.objects.filter(email='admin@dzvolunteer.dz').exists():
        User.objects.create_user(
            email='admin@dzvolunteer.dz',
            password='admin123',
            full_name='Administrateur DZ Volunteer',
            user_type='admin',
            is_staff=True,
            is_superuser=True,
            is_verified=True
        )
        print("✅ Super utilisateur créé: admin@dzvolunteer.dz / admin123")
    else:
        print("📝 Super utilisateur existe déjà")

def initialize_odds():
    """Initialiser les 17 ODD (Objectifs de Développement Durable)"""
    print("4. Initialisation des ODD...")
    
    odds_data = [
        (1, "Pas de pauvreté", "لا فقر", "#E5243B", "Éliminer la pauvreté sous toutes ses formes et partout dans le monde"),
        (2, "Faim zéro", "القضاء التام على الجوع", "#DDA63A", "Éliminer la faim, assurer la sécurité alimentaire"),
        (3, "Bonne santé et bien-être", "الصحة الجيدة والرفاه", "#4C9F38", "Permettre à tous de vivre en bonne santé"),
        (4, "Éducation de qualité", "التعليم الجيد", "#C5192D", "Assurer une éducation inclusive et équitable"),
        (5, "Égalité entre les sexes", "المساواة بين الجنسين", "#FF3A21", "Parvenir à l'égalité des sexes"),
        (6, "Eau propre et assainissement", "المياه النظيفة والنظافة الصحية", "#26BDE2", "Garantir l'accès à l'eau et à l'assainissement"),
        (7, "Énergie propre et d'un coût abordable", "طاقة نظيفة وبأسعار معقولة", "#FCC30B", "Garantir l'accès à une énergie abordable"),
        (8, "Travail décent et croissance économique", "العمل اللائق ونمو الاقتصاد", "#A21942", "Promouvoir une croissance économique soutenue"),
        (9, "Industrie, innovation et infrastructure", "الصناعة والابتكار والهياكل الأساسية", "#FD6925", "Bâtir une infrastructure résiliente"),
        (10, "Inégalités réduites", "الحد من أوجه عدم المساواة", "#DD1367", "Réduire les inégalités dans les pays"),
        (11, "Villes et communautés durables", "مدن ومجتمعات محلية مستدامة", "#FD9D24", "Faire en sorte que les villes soient inclusives"),
        (12, "Consommation et production responsables", "الاستهلاك والإنتاج المسؤولان", "#BF8B2E", "Établir des modes de consommation durables"),
        (13, "Mesures relatives à la lutte contre les changements climatiques", "العمل المناخي", "#3F7E44", "Prendre des mesures pour lutter contre le climat"),
        (14, "Vie aquatique", "الحياة تحت الماء", "#0A97D9", "Conserver et exploiter de manière durable les océans"),
        (15, "Vie terrestre", "الحياة في البر", "#56C02B", "Gérer durablement les forêts et la biodiversité"),
        (16, "Paix, justice et institutions efficaces", "السلام والعدل والمؤسسات القوية", "#00689D", "Promouvoir des sociétés pacifiques et inclusives"),
        (17, "Partenariats pour la réalisation des objectifs", "عقد الشراكات لتحقيق الأهداف", "#19486A", "Renforcer les moyens de mise en œuvre")
    ]
    
    created_count = 0
    for numero, nom_fr, nom_ar, couleur, description in odds_data:
        if not ODD.objects.filter(numero=numero).exists():
            ODD.objects.create(
                numero=numero,
                nom_fr=nom_fr,
                nom_ar=nom_ar,
                couleur=couleur,
                description=description
            )
            created_count += 1
    
    print(f"✅ {created_count} ODD créés ({ODD.objects.count()} total)")

def initialize_competences():
    """Initialiser les compétences de base"""
    print("5. Initialisation des compétences...")
    
    competences_data = [
        ("Communication", "مهارات التواصل", "Capacité à communiquer efficacement"),
        ("Leadership", "القيادة", "Compétences de direction et d'organisation"),
        ("Enseignement", "التدريس", "Capacité à enseigner et former"),
        ("Informatique", "المعلوماتية", "Compétences techniques et informatiques"),
        ("Santé", "الصحة", "Connaissances médicales et de premiers secours"),
        ("Environnement", "البيئة", "Protection et préservation de l'environnement"),
        ("Agriculture", "الفلاحة", "Techniques agricoles et développement rural"),
        ("Artisanat", "الحرف اليدوية", "Compétences artisanales traditionnelles"),
        ("Cuisine", "الطبخ", "Préparation de repas et nutrition"),
        ("Sport", "الرياضة", "Animation sportive et encadrement")
    ]
    
    created_count = 0
    for nom_fr, nom_ar, description in competences_data:
        if not Competence.objects.filter(nom_fr=nom_fr).exists():
            Competence.objects.create(
                nom_fr=nom_fr,
                nom_ar=nom_ar,
                description=description
            )
            created_count += 1
    
    print(f"✅ {created_count} compétences créées ({Competence.objects.count()} total)")

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Initialisation du Backend Django DZ-Volunteer")
    print("=" * 50)
    
    # 1. Créer la base de données PostgreSQL
    if not create_database():
        return False
    
    # 2. Appliquer les migrations
    if not migrate_database():
        return False
    
    # 3. Créer le super utilisateur
    create_superuser()
    
    # 4. Initialiser les données de base
    initialize_odds()
    initialize_competences()
    
    print("\n🎉 Base de données initialisée avec succès!")
    print("📍 Informations importantes:")
    print("   - Base de données: dz_volunteer (PostgreSQL)")
    print("   - Super utilisateur: admin@dzvolunteer.dz / admin123")
    print("   - Admin Django: http://127.0.0.1:8000/admin/")
    print("   - API: http://127.0.0.1:8000/api/")
    
    print("\n💻 Prochaines étapes:")
    print("   1. python manage.py runserver")
    print("   2. python test.py (pour tester l'API)")
    print("   3. Accéder à l'interface admin pour gérer les données")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Échec de l'initialisation")
        print("💡 Vérifications à faire:")
        print("   - PostgreSQL est installé et démarré")
        print("   - Mot de passe PostgreSQL: 20772077")
        print("   - Port PostgreSQL: 5432")
        exit(1)
    exit(0)