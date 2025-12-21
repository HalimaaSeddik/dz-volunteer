from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Volunteer, Organization

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'wilaya', 'total_hours', 'badge_level', 'average_rating')
    list_filter = ('badge_level', 'wilaya', 'user__is_active')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-total_hours',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'is_verified', 'wilaya', 'total_missions', 'average_rating')
    list_filter = ('is_verified', 'organization_type', 'wilaya')
    search_fields = ('name', 'email', 'user__email')
    ordering = ('-user__date_joined',)
    actions = ['verify_organizations']
    
    def verify_organizations(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} organisations vérifiées.")
    verify_organizations.short_description = "Vérifier les organisations sélectionnées"
