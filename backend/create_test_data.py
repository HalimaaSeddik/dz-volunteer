"""
Script pour créer des données de test
Usage: python manage.py shell < create_test_data.py
"""

from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model

from accounts.models import Organization, Volunteer
from missions.models import Mission
from odd.models import ODD
from skills.models import Skill, VolunteerSkill

User = get_user_model()

print("Création des données de test...")

# ========== UTILISATEURS DE TEST ==========
print("\n1. Création des utilisateurs...")

# Admin
admin, created = User.objects.get_or_create(
    email="admin@dzvolunteer.dz",
    defaults={
        "first_name": "Admin",
        "last_name": "DZV",
        "user_type": "ADMIN",
        "is_staff": True,
        "is_superuser": True,
    },
)
if created:
    admin.set_password("admin123")
    admin.save()
    print("✓ Admin créé : admin@dzvolunteer.dz / admin123")

# Bénévole 1 - Amira (Argent)
user1, created = User.objects.get_or_create(
    email="amira.benali@email.dz",
    defaults={
        "first_name": "Amira",
        "last_name": "Benali",
        "phone": "0555123456",
        "user_type": "VOLUNTEER",
    },
)
if created:
    user1.set_password("password123")
    user1.save()
    volunteer1 = Volunteer.objects.create(
        user=user1,
        date_of_birth=datetime(1995, 5, 15).date(),
        gender="F",
        wilaya="19",
        commune="Sétif",
        total_hours=Decimal("67.5"),
        completed_missions=12,
        average_rating=Decimal("4.8"),
        badge_level="SILVER",
        motivation="Je suis passionnée par l'aide aux autres et je souhaite contribuer au développement de ma communauté.",
        interests=["ENVIRONMENT", "EDUCATION"],
    )
    print("✓ Bénévole 1 créé : amira.benali@email.dz / password123 (Badge Argent)")

# Bénévole 2 - Karim (Bronze)
user2, created = User.objects.get_or_create(
    email="karim.mansouri@email.dz",
    defaults={
        "first_name": "Karim",
        "last_name": "Mansouri",
        "phone": "0666234567",
        "user_type": "VOLUNTEER",
    },
)
if created:
    user2.set_password("password123")
    user2.save()
    volunteer2 = Volunteer.objects.create(
        user=user2,
        date_of_birth=datetime(1998, 3, 20).date(),
        gender="M",
        wilaya="19",
        commune="El Eulma",
        total_hours=Decimal("32.0"),
        completed_missions=5,
        average_rating=Decimal("4.5"),
        badge_level="BRONZE",
        motivation="Je veux acquérir de l'expérience et rencontrer de nouvelles personnes.",
        interests=["SOCIAL", "HEALTH"],
    )
    print("✓ Bénévole 2 créé : karim.mansouri@email.dz / password123 (Badge Bronze)")

# Bénévole 3 - Sarah (Or)
user3, created = User.objects.get_or_create(
    email="sarah.khelifi@email.dz",
    defaults={
        "first_name": "Sarah",
        "last_name": "Khelifi",
        "phone": "0777345678",
        "user_type": "VOLUNTEER",
    },
)
if created:
    user3.set_password("password123")
    user3.save()
    volunteer3 = Volunteer.objects.create(
        user=user3,
        date_of_birth=datetime(1992, 8, 10).date(),
        gender="F",
        wilaya="16",
        commune="Alger",
        total_hours=Decimal("215.0"),
        completed_missions=48,
        average_rating=Decimal("4.9"),
        badge_level="GOLD",
        motivation="Le bénévolat fait partie de ma vie. J'adore aider et voir l'impact positif de mes actions.",
        interests=["ENVIRONMENT", "SOCIAL", "CULTURE"],
    )
    print("✓ Bénévole 3 créé : sarah.khelifi@email.dz / password123 (Badge Or)")

# Organisation 1 - Croissant Rouge Algérien
org_user1, created = User.objects.get_or_create(
    email="contact@cra.dz",
    defaults={
        "first_name": "CRA",
        "last_name": "Algeria",
        "phone": "0213123456",
        "user_type": "ORGANIZATION",
    },
)
if created:
    org_user1.set_password("password123")
    org_user1.save()
    org1 = Organization.objects.create(
        user=org_user1,
        name="Croissant Rouge Algérien",
        organization_type="ASSOCIATION",
        registration_number="CRA-001",
        email="info@cra.dz",
        phone="0213123456",
        website="https://www.croissant-rouge.dz",
        wilaya="16",
        address="12 Rue Larbi Ben M'hidi, Alger",
        representative_name="Ahmed Benali",
        representative_position="Président",
        representative_email="ahmed@cra.dz",
        description="Le Croissant Rouge Algérien est une association humanitaire à but non lucratif qui œuvre depuis sa création pour venir en aide aux populations en difficulté, promouvoir les valeurs humanitaires et contribuer au développement social en Algérie. Nos missions couvrent l'aide d'urgence, le soutien aux personnes vulnérables, et la sensibilisation aux principes humanitaires."
        * 3,
        mission_values="Humanité, Impartialité, Neutralité, Indépendance, Volontariat",
        is_verified=True,
        total_missions=45,
        total_volunteers=230,
        average_rating=Decimal("4.8"),
    )
    print("✓ Organisation 1 créée : contact@cra.dz / password123 (Vérifiée)")

# Organisation 2 - Green Algeria
org_user2, created = User.objects.get_or_create(
    email="contact@greenalgeria.dz",
    defaults={
        "first_name": "Green",
        "last_name": "Algeria",
        "phone": "0555987654",
        "user_type": "ORGANIZATION",
    },
)
if created:
    org_user2.set_password("password123")
    org_user2.save()
    org2 = Organization.objects.create(
        user=org_user2,
        name="Green Algeria",
        organization_type="NGO",
        registration_number="GA-002",
        email="info@greenalgeria.dz",
        phone="0555987654",
        website="https://www.greenalgeria.dz",
        wilaya="31",
        address="Avenue de l'Environnement, Oran",
        representative_name="Fatima Zerrouki",
        representative_position="Directrice",
        representative_email="fatima@greenalgeria.dz",
        description="Green Algeria est une ONG environnementale dédiée à la protection de l'environnement et à la promotion du développement durable en Algérie. Nous organisons des campagnes de nettoyage, de reboisement, et de sensibilisation à l'écologie. Notre objectif est de créer une société plus verte et plus consciente des enjeux environnementaux."
        * 3,
        mission_values="Protection de l'environnement, Développement durable, Éducation écologique",
        is_verified=True,
        total_missions=28,
        total_volunteers=145,
        average_rating=Decimal("4.6"),
    )
    print("✓ Organisation 2 créée : contact@greenalgeria.dz / password123 (Vérifiée)")

# ========== COMPÉTENCES DES BÉNÉVOLES ==========
print("\n2. Attribution des compétences...")

try:
    # Amira
    animation = Skill.objects.get(name="Animation")
    informatique = Skill.objects.get(name="Informatique")
    premiers_secours = Skill.objects.get(name="Premiers Secours")

    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer1, skill=animation, defaults={"status": "VALIDATED"}
    )
    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer1, skill=informatique, defaults={"status": "VALIDATED"}
    )
    vs, created = VolunteerSkill.objects.get_or_create(
        volunteer=volunteer1, skill=premiers_secours, defaults={"status": "VALIDATED"}
    )

    # Karim
    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer2, skill=animation, defaults={"status": "VALIDATED"}
    )

    # Sarah
    cuisine = Skill.objects.get(name="Cuisine")
    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer3, skill=animation, defaults={"status": "VALIDATED"}
    )
    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer3, skill=premiers_secours, defaults={"status": "VALIDATED"}
    )
    VolunteerSkill.objects.get_or_create(
        volunteer=volunteer3, skill=cuisine, defaults={"status": "VALIDATED"}
    )

    print("✓ Compétences attribuées")
except Exception as e:
    print(f"⚠ Erreur compétences : {e}")

# ========== MISSIONS ==========
print("\n3. Création des missions...")

try:
    odd1 = ODD.objects.get(number=1)  # Pas de pauvreté
    odd14 = ODD.objects.get(number=14)  # Vie aquatique
    odd4 = ODD.objects.get(number=4)  # Éducation de qualité

    # Mission 1 - Distribution alimentaire (Croissant Rouge)
    mission1, created = Mission.objects.get_or_create(
        title="Distribution alimentaire - Ramadan 2025",
        organization=org1,
        defaults={
            "short_description": "Distribution de colis alimentaires aux familles nécessiteuses durant le mois de Ramadan.",
            "full_description": """Nous organisons une grande distribution de colis alimentaires pour venir en aide aux familles en difficulté durant le mois béni de Ramadan.

Vos tâches seront :
- Préparation et emballage des colis
- Accueil et orientation des bénéficiaires
- Distribution des colis
- Aide au rangement

Cette mission s'inscrit dans notre programme annuel de solidarité. Rejoignez-nous pour faire une différence !""",
            "mission_type": "ONE_TIME",
            "odd": odd1,
            "causes": ["SOCIAL"],
            "date": (datetime.now() + timedelta(days=10)).date(),
            "start_time": "09:00:00",
            "end_time": "13:00:00",
            "duration_hours": Decimal("4.0"),
            "wilaya": "19",
            "commune": "Sétif",
            "full_address": "Place centrale, El Eulma, Sétif",
            "meeting_point": "Devant la mairie d'El Eulma",
            "required_volunteers": 10,
            "accepted_volunteers": 7,
            "accessible_by_car": True,
            "accessible_by_transport": True,
            "accessible_on_foot": False,
            "pmr_accessible": True,
            "items_to_bring": ["Casquette", "Bouteille d'eau", "Masque"],
            "provided_equipment": {"meal": True, "transport": False},
            "additional_requirements": "Être ponctuel et motivé",
            "experience_level": "BEGINNER",
            "status": "PUBLISHED",
            "contact_name": "Ahmed Benali",
            "contact_email": "ahmed@cra.dz",
            "contact_phone": "0213123456",
        },
    )
    if created:
        # Ajouter compétence requise
        mission1.required_skills.add(
            premiers_secours, through_defaults={"verification_required": True}
        )
        mission1.required_skills.add(animation, through_defaults={"verification_required": False})
        print("✓ Mission 1 créée : Distribution alimentaire")

    # Mission 2 - Nettoyage de plage (Green Algeria)
    mission2, created = Mission.objects.get_or_create(
        title="Nettoyage environnemental - Plage des Andalouses",
        organization=org2,
        defaults={
            "short_description": "Grande opération de nettoyage de la plage des Andalouses pour préserver notre littoral.",
            "full_description": """Rejoignez-nous pour une journée de nettoyage de la magnifique plage des Andalouses à Oran.

Objectifs :
- Ramasser les déchets sur la plage et dans l'eau
- Sensibiliser le public à la protection de l'environnement
- Trier les déchets collectés

Nous fournirons : gants, sacs poubelles, gilets, rafraîchissements.

Ensemble, protégeons notre littoral !""",
            "mission_type": "ONE_TIME",
            "odd": odd14,
            "causes": ["ENVIRONMENT"],
            "date": (datetime.now() + timedelta(days=20)).date(),
            "start_time": "08:00:00",
            "end_time": "12:00:00",
            "duration_hours": Decimal("4.0"),
            "wilaya": "31",
            "commune": "Oran",
            "full_address": "Plage des Andalouses, Oran",
            "meeting_point": "Parking principal de la plage",
            "required_volunteers": 8,
            "accepted_volunteers": 5,
            "accessible_by_car": True,
            "accessible_by_transport": True,
            "accessible_on_foot": False,
            "pmr_accessible": False,
            "items_to_bring": ["Chapeau", "Crème solaire", "Eau"],
            "provided_equipment": {"meal": False, "material": True},
            "additional_requirements": "Savoir nager est un plus",
            "experience_level": "BEGINNER",
            "status": "PUBLISHED",
            "contact_name": "Fatima Zerrouki",
            "contact_email": "fatima@greenalgeria.dz",
            "contact_phone": "0555987654",
        },
    )
    if created:
        print("✓ Mission 2 créée : Nettoyage de plage")

    # Mission 3 - Soutien scolaire
    mission3, created = Mission.objects.get_or_create(
        title="Soutien scolaire - Mathématiques",
        organization=org1,
        defaults={
            "short_description": "Aide aux devoirs et soutien en mathématiques pour élèves du collège.",
            "full_description": """Venez aider des élèves en difficulté en mathématiques.

Vous aiderez les collégiens avec :
- Les devoirs
- Les exercices de mathématiques
- La préparation des contrôles

Bonne ambiance garantie !""",
            "mission_type": "RECURRING",
            "odd": odd4,
            "causes": ["EDUCATION"],
            "date": (datetime.now() + timedelta(days=15)).date(),
            "start_time": "14:00:00",
            "end_time": "17:00:00",
            "duration_hours": Decimal("3.0"),
            "wilaya": "19",
            "commune": "Sétif",
            "full_address": "Lycée Mohamed Kerouani, Sétif",
            "meeting_point": "Hall du lycée",
            "required_volunteers": 5,
            "accepted_volunteers": 3,
            "accessible_by_car": True,
            "accessible_by_transport": True,
            "accessible_on_foot": True,
            "pmr_accessible": True,
            "items_to_bring": [],
            "provided_equipment": {},
            "additional_requirements": "Niveau bac +2 minimum en mathématiques",
            "experience_level": "INTERMEDIATE",
            "status": "PUBLISHED",
            "contact_name": "Ahmed Benali",
            "contact_email": "ahmed@cra.dz",
            "contact_phone": "0213123456",
        },
    )
    if created:
        print("✓ Mission 3 créée : Soutien scolaire")

    print("✓ Missions créées avec succès")

except Exception as e:
    print(f"⚠ Erreur missions : {e}")

print("\n✅ Données de test créées avec succès !")
print("\n" + "=" * 60)
print("COMPTES DE TEST CRÉÉS")
print("=" * 60)
print("\n👨‍💼 ADMIN")
print("  Email    : admin@dzvolunteer.dz")
print("  Password : admin123")
print("\n👤 BÉNÉVOLES")
print("  1. Amira Benali (Badge Argent - 67.5h)")
print("     Email    : amira.benali@email.dz")
print("     Password : password123")
print("\n  2. Karim Mansouri (Badge Bronze - 32h)")
print("     Email    : karim.mansouri@email.dz")
print("     Password : password123")
print("\n  3. Sarah Khelifi (Badge Or - 215h)")
print("     Email    : sarah.khelifi@email.dz")
print("     Password : password123")
print("\n🏢 ORGANISATIONS")
print("  1. Croissant Rouge Algérien (Vérifiée)")
print("     Email    : contact@cra.dz")
print("     Password : password123")
print("\n  2. Green Algeria (Vérifiée)")
print("     Email    : contact@greenalgeria.dz")
print("     Password : password123")
print("\n" + "=" * 60)
print("\nVous pouvez maintenant tester l'API avec ces comptes !")
print("Interface admin : http://127.0.0.1:8000/admin/")
print("=" * 60)
