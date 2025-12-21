"""
Modèles pour la gestion des compétences
"""

from django.db import models
from accounts.models import Volunteer


class Skill(models.Model):
    """
    Compétences disponibles sur la plateforme
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom de la compétence')
    requires_verification = models.BooleanField(default=False, verbose_name='Nécessite une vérification')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icône (emoji)')
    description = models.TextField(blank=True, verbose_name='Description')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Compétence'
        verbose_name_plural = 'Compétences'
        ordering = ['name']
    
    def __str__(self):
        verification = "⚠️" if self.requires_verification else ""
        return f"{self.icon} {self.name} {verification}"


class VolunteerSkill(models.Model):
    """
    Compétences d'un bénévole avec validation
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('VALIDATED', 'Validée'),
        ('REJECTED', 'Refusée'),
    ]
    
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='volunteer_skills')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VALIDATED', verbose_name='Statut')
    
    # Pour les compétences nécessitant une vérification
    document = models.FileField(upload_to='skill_documents/', null=True, blank=True, verbose_name='Document justificatif')
    rejection_reason = models.TextField(blank=True, verbose_name='Raison du refus')
    
    # Validation par l'admin
    validated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_skills')
    validated_at = models.DateTimeField(null=True, blank=True, verbose_name='Date de validation')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Compétence de bénévole'
        verbose_name_plural = 'Compétences des bénévoles'
        unique_together = ['volunteer', 'skill']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.volunteer.user.get_full_name()} - {self.skill.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Si la compétence ne nécessite pas de vérification, valider automatiquement
        if not self.skill.requires_verification and self.status == 'PENDING':
            self.status = 'VALIDATED'
        
        # Si nécessite vérification mais pas de document, mettre en attente
        if self.skill.requires_verification and not self.document:
            self.status = 'PENDING'
        
        super().save(*args, **kwargs)
