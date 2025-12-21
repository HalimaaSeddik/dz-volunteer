from django.contrib import admin
from .models import ODD


@admin.register(ODD)
class ODDAdmin(admin.ModelAdmin):
    list_display = ('number', 'title_fr', 'color', 'mission_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title_fr', 'title_ar', 'description_fr')
    ordering = ('number',)
    readonly_fields = ('mission_count',)
