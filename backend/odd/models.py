"""
Modèles pour les Objectifs de Développement Durable (ODD)
"""

from django.db import models


class ODD(models.Model):
    """
    Les 17 Objectifs de Développement Durable de l'ONU
    """
    number = models.IntegerField(unique=True, verbose_name='Numéro')
    title_fr = models.CharField(max_length=200, verbose_name='Titre (Français)')
    title_ar = models.CharField(max_length=200, verbose_name='Titre (Arabe)', blank=True)
    description_fr = models.TextField(verbose_name='Description (Français)')
    description_ar = models.TextField(verbose_name='Description (Arabe)', blank=True)
    color = models.CharField(max_length=7, verbose_name='Couleur (Hex)', help_text='Ex: #E5243B')
    icon = models.ImageField(upload_to='odd_icons/', verbose_name='Icône', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    
    # Statistiques
    mission_count = models.IntegerField(default=0, verbose_name='Nombre de missions')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ODD'
        verbose_name_plural = 'ODD'
        ordering = ['number']
    
    def __str__(self):
        return f"ODD {self.number} - {self.title_fr}"
