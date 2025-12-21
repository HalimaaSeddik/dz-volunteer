from django.contrib import admin

from .models import Skill, VolunteerSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "requires_verification", "icon", "is_active")
    list_filter = ("requires_verification", "is_active")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(VolunteerSkill)
class VolunteerSkillAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "skill", "status", "created_at", "validated_at")
    list_filter = ("status", "skill__requires_verification", "created_at")
    search_fields = ("volunteer__user__email", "volunteer__user__first_name", "skill__name")
    ordering = ("-created_at",)
    actions = ["validate_skills", "reject_skills"]

    def validate_skills(self, request, queryset):
        from django.utils import timezone

        queryset.update(status="VALIDATED", validated_by=request.user, validated_at=timezone.now())
        self.message_user(request, f"{queryset.count()} compétences validées.")

    validate_skills.short_description = "Valider les compétences sélectionnées"

    def reject_skills(self, request, queryset):
        queryset.update(status="REJECTED")
        self.message_user(request, f"{queryset.count()} compétences refusées.")

    reject_skills.short_description = "Refuser les compétences sélectionnées"
