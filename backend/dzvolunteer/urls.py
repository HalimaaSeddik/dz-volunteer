"""
URLs principales du projet
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin Django
    path("admin/", admin.site.urls),
    # API
    path("api/auth/", include("accounts.urls")),
    path("api/missions/", include("missions.urls")),
    path("api/skills/", include("skills.urls")),
    path("api/odd/", include("odd.urls")),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Configuration du site admin
admin.site.site_header = "DZ-Volunteer Administration"
admin.site.site_title = "DZ-Volunteer Admin"
admin.site.index_title = "Bienvenue dans l'administration DZ-Volunteer"
