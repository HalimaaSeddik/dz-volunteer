"""
Vues pour l'authentification et les comptes
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import (
    RegisterVolunteerSerializer, 
    RegisterOrganizationSerializer,
    UserSerializer,
    VolunteerProfileSerializer,
    OrganizationSerializer
)
from .models import User, Volunteer, Organization


class RegisterVolunteerView(generics.CreateAPIView):
    """Inscription bénévole"""
    serializer_class = RegisterVolunteerSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Inscription réussie !',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class RegisterOrganizationView(generics.CreateAPIView):
    """Inscription organisation"""
    serializer_class = RegisterOrganizationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Inscription réussie ! Votre organisation sera vérifiée prochainement.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Connexion"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email et mot de passe requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Identifiants incorrects'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Compte désactivé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class VolunteerProfileView(generics.RetrieveUpdateAPIView):
    """Profil du bénévole connecté"""
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.volunteer_profile


class OrganizationProfileView(generics.RetrieveUpdateAPIView):
    """Profil de l'organisation connectée"""
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.organization_profile
