from django.contrib import admin
from .models import Mission, MissionSkillRequirement, Application, Participation, Review, Report


class MissionSkillRequirementInline(admin.TabularInline):
    model = MissionSkillRequirement
    extra = 1


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date', 'status', 'wilaya', 'accepted_volunteers', 'required_volunteers', 'get_fill_percentage')
    list_filter = ('status', 'mission_type', 'wilaya', 'date', 'odd')
    search_fields = ('title', 'organization__name', 'full_description')
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    inlines = [MissionSkillRequirementInline]
    readonly_fields = ('view_count', 'application_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('organization', 'title', 'short_description', 'full_description', 'mission_type', 'status')
        }),
        ('ODD et Causes', {
            'fields': ('odd', 'causes')
        }),
        ('Date et Horaires', {
            'fields': ('date', 'start_time', 'end_time', 'duration_hours')
        }),
        ('Localisation', {
            'fields': ('wilaya', 'commune', 'full_address', 'meeting_point', 'latitude', 'longitude')
        }),
        ('Accessibilité', {
            'fields': ('accessible_by_car', 'accessible_by_transport', 'accessible_on_foot', 'pmr_accessible')
        }),
        ('Bénévoles', {
            'fields': ('required_volunteers', 'accepted_volunteers')
        }),
        ('Prérequis', {
            'fields': ('additional_requirements', 'experience_level', 'items_to_bring', 'provided_equipment')
        }),
        ('Contact', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
        ('Statistiques', {
            'fields': ('view_count', 'application_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'mission', 'status', 'has_required_skills', 'applied_at')
    list_filter = ('status', 'has_required_skills', 'applied_at')
    search_fields = ('volunteer__user__email', 'mission__title')
    ordering = ('-applied_at',)
    actions = ['accept_applications', 'reject_applications']
    
    def accept_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='ACCEPTED', responded_at=timezone.now())
        self.message_user(request, f"{queryset.count()} candidatures acceptées.")
    accept_applications.short_description = "Accepter les candidatures sélectionnées"
    
    def reject_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='REJECTED', responded_at=timezone.now())
        self.message_user(request, f"{queryset.count()} candidatures refusées.")
    reject_applications.short_description = "Refuser les candidatures sélectionnées"


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'mission', 'was_present', 'hours_completed', 'hours_validated', 'organization_rating', 'volunteer_rating')
    list_filter = ('was_present', 'hours_validated', 'organization_rating')
    search_fields = ('volunteer__user__email', 'mission__title')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'organization', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('volunteer__user__email', 'organization__name', 'comment')
    ordering = ('-created_at',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('reporter__email', 'reason')
    ordering = ('-created_at',)
    actions = ['mark_as_reviewed', 'mark_as_resolved']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='REVIEWED')
        self.message_user(request, f"{queryset.count()} signalements marqués comme examinés.")
    mark_as_reviewed.short_description = "Marquer comme examiné"
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='RESOLVED', resolved_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} signalements résolus.")
    mark_as_resolved.short_description = "Marquer comme résolu"
