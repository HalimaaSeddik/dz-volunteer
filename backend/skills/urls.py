"""
URLs pour les compétences
"""

from django.urls import path
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Skill, VolunteerSkill
from accounts.serializers import SkillSerializer, VolunteerSkillSerializer


class SkillListView(generics.ListAPIView):
    """Liste de toutes les compétences disponibles"""
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Skill.objects.filter(is_active=True)


class VolunteerSkillListView(generics.ListCreateAPIView):
    """Compétences d'un bénévole"""
    serializer_class = VolunteerSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return VolunteerSkill.objects.filter(
            volunteer=self.request.user.volunteer_profile
        ).select_related('skill')
    
    def perform_create(self, serializer):
        serializer.save(volunteer=self.request.user.volunteer_profile)


class VolunteerSkillDeleteView(generics.DestroyAPIView):
    """Supprimer une compétence"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return VolunteerSkill.objects.filter(
            volunteer=self.request.user.volunteer_profile
        )


class ValidateSkillView(APIView):
    """Admin: Valider ou refuser une compétence"""
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request, skill_id):
        from django.utils import timezone
        
        try:
            volunteer_skill = VolunteerSkill.objects.get(id=skill_id)
        except VolunteerSkill.DoesNotExist:
            return Response(
                {'error': 'Compétence non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        action = request.data.get('action')  # 'validate' ou 'reject'
        
        if action == 'validate':
            volunteer_skill.status = 'VALIDATED'
            volunteer_skill.validated_by = request.user
            volunteer_skill.validated_at = timezone.now()
        elif action == 'reject':
            volunteer_skill.status = 'REJECTED'
            volunteer_skill.rejection_reason = request.data.get('reason', '')
        else:
            return Response(
                {'error': 'Action invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        volunteer_skill.save()
        
        return Response(VolunteerSkillSerializer(volunteer_skill).data)


class PendingSkillsView(generics.ListAPIView):
    """Admin: Liste des compétences en attente de validation"""
    serializer_class = VolunteerSkillSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = VolunteerSkill.objects.filter(status='PENDING').select_related('volunteer__user', 'skill')


app_name = 'skills'

urlpatterns = [
    path('', SkillListView.as_view(), name='skill_list'),
    path('my-skills/', VolunteerSkillListView.as_view(), name='my_skills'),  # Page 10
    path('my-skills/<int:pk>/', VolunteerSkillDeleteView.as_view(), name='delete_skill'),
    
    # Admin
    path('admin/validate/<int:skill_id>/', ValidateSkillView.as_view(), name='validate_skill'),  # Page 25
    path('admin/pending/', PendingSkillsView.as_view(), name='pending_skills'),
]
