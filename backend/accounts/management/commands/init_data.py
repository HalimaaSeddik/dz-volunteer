"""
Script pour initialiser les données de base (ODD, compétences, etc.)
"""

from django.core.management.base import BaseCommand
from odd.models import ODD
from skills.models import Skill


class Command(BaseCommand):
    help = 'Initialise les données de base (ODD et compétences)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initialisation des données de base...')
        
        # ========== CRÉATION DES 17 ODD ==========
        self.stdout.write('Création des 17 ODD...')
        
        odd_data = [
            (1, 'Pas de pauvreté', 'القضاء على الفقر', '#E5243B'),
            (2, 'Faim zéro', 'القضاء التام على الجوع', '#DDA63A'),
            (3, 'Bonne santé et bien-être', 'الصحة الجيدة والرفاه', '#4C9F38'),
            (4, 'Éducation de qualité', 'التعليم الجيد', '#C5192D'),
            (5, 'Égalité entre les sexes', 'المساواة بين الجنسين', '#FF3A21'),
            (6, 'Eau propre et assainissement', 'المياه النظيفة والنظافة الصحية', '#26BDE2'),
            (7, 'Énergie propre et d\'un coût abordable', 'طاقة نظيفة وبأسعار معقولة', '#FCC30B'),
            (8, 'Travail décent et croissance économique', 'العمل اللائق ونمو الاقتصاد', '#A21942'),
            (9, 'Industrie, innovation et infrastructure', 'الصناعة والابتكار والهياكل الأساسية', '#FD6925'),
            (10, 'Inégalités réduites', 'الحد من أوجه عدم المساواة', '#DD1367'),
            (11, 'Villes et communautés durables', 'مدن ومجتمعات محلية مستدامة', '#FD9D24'),
            (12, 'Consommation et production responsables', 'الاستهلاك والإنتاج المسؤولان', '#BF8B2E'),
            (13, 'Mesures relatives à la lutte contre les changements climatiques', 'العمل المناخي', '#3F7E44'),
            (14, 'Vie aquatique', 'الحياة تحت الماء', '#0A97D9'),
            (15, 'Vie terrestre', 'الحياة في البر', '#56C02B'),
            (16, 'Paix, justice et institutions efficaces', 'السلام والعدل والمؤسسات القوية', '#00689D'),
            (17, 'Partenariats pour la réalisation des objectifs', 'عقد الشراكات لتحقيق الأهداف', '#19486A'),
        ]
        
        for number, title_fr, title_ar, color in odd_data:
            ODD.objects.get_or_create(
                number=number,
                defaults={
                    'title_fr': title_fr,
                    'title_ar': title_ar,
                    'color': color,
                    'description_fr': f'Objectif {number}: {title_fr}',
                    'description_ar': title_ar,
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'{len(odd_data)} ODD créés'))
        
        # ========== CRÉATION DES COMPÉTENCES ==========
        self.stdout.write('Création des compétences...')
        
        skills_data = [
            # Compétences sans vérification
            ('Animation', '🎭', False),
            ('Informatique', '💻', False),
            ('Cuisine', '🍳', False),
            ('Photographie', '📷', False),
            ('Menuiserie', '🔨', False),
            ('Électricité', '⚡', False),
            ('Plomberie', '🔧', False),
            ('Jardinage', '🌱', False),
            ('Couture', '🧵', False),
            ('Peinture', '🎨', False),
            ('Musique', '🎵', False),
            ('Sport', '⚽', False),
            ('Danse', '💃', False),
            ('Théâtre', '🎭', False),
            ('Écriture', '✍️', False),
            ('Traduction', '🌍', False),
            ('Gestion de foule', '👥', False),
            ('Communication', '📢', False),
            ('Marketing', '📊', False),
            ('Design graphique', '🎨', False),
            
            # Compétences nécessitant vérification
            ('Premiers Secours', '🚑', True),
            ('Langue des signes', '🧏', True),
            ('Psychologie', '🧠', True),
            ('Soins infirmiers', '💉', True),
            ('Enseignement', '👨‍🏫', True),
            ('Conduite de véhicules lourds', '🚛', True),
            ('Sécurité incendie', '🔥', True),
        ]
        
        for name, icon, requires_verification in skills_data:
            Skill.objects.get_or_create(
                name=name,
                defaults={
                    'icon': icon,
                    'requires_verification': requires_verification,
                    'description': f'Compétence: {name}',
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'{len(skills_data)} compétences créées'))
        
        self.stdout.write(self.style.SUCCESS('✅ Initialisation terminée avec succès !'))
