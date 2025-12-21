"""
URLs pour les ODD
"""

from django.urls import path
from rest_framework import generics, permissions
from .models import ODD
from accounts.serializers import ODDSerializer


class ODDListView(generics.ListAPIView):
    """Liste des 17 ODD"""
    serializer_class = ODDSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ODD.objects.filter(is_active=True)


class ODDDetailView(generics.RetrieveAPIView):
    """Détail d'un ODD"""
    serializer_class = ODDSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ODD.objects.filter(is_active=True)


app_name = 'odd'

urlpatterns = [
    path('', ODDListView.as_view(), name='odd_list'),
    path('<int:pk>/', ODDDetailView.as_view(), name='odd_detail'),
]
