from django.contrib import admin
from .models import (
    FocusArea, FocusAreaObjective, FocusAreaActivity,
    FocusAreaOutcome, FocusAreaPartner, FocusAreaMilestone
)


class FocusAreaObjectiveInline(admin.TabularInline):
    model = FocusAreaObjective
    extra = 1
    fields = ['text', 'order']


class FocusAreaActivityInline(admin.TabularInline):
    model = FocusAreaActivity
    extra = 1
    fields = ['text', 'order']


class FocusAreaOutcomeInline(admin.TabularInline):
    model = FocusAreaOutcome
    extra = 1
    fields = ['title', 'description', 'metric', 'order']


class FocusAreaPartnerInline(admin.TabularInline):
    model = FocusAreaPartner
    extra = 1
    fields = ['name', 'type', 'role', 'order']


class FocusAreaMilestoneInline(admin.TabularInline):
    model = FocusAreaMilestone
    extra = 1
    fields = ['year', 'event', 'order']


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'start_date', 'order', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'overview_summary']
    list_editable = ['order', 'status']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image', 'order')
        }),
        ('Overview', {
            'fields': ('overview_summary',)
        }),
        ('Timeline', {
            'fields': ('status', 'start_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        FocusAreaObjectiveInline,
        FocusAreaActivityInline,
        FocusAreaOutcomeInline,
        FocusAreaPartnerInline,
        FocusAreaMilestoneInline,
    ]


@admin.register(FocusAreaObjective)
class FocusAreaObjectiveAdmin(admin.ModelAdmin):
    list_display = ['focus_area', 'text', 'order']
    list_filter = ['focus_area']
    search_fields = ['text']
    list_editable = ['order']


@admin.register(FocusAreaActivity)
class FocusAreaActivityAdmin(admin.ModelAdmin):
    list_display = ['focus_area', 'text', 'order']
    list_filter = ['focus_area']
    search_fields = ['text']
    list_editable = ['order']


@admin.register(FocusAreaOutcome)
class FocusAreaOutcomeAdmin(admin.ModelAdmin):
    list_display = ['focus_area', 'title', 'metric', 'order']
    list_filter = ['focus_area']
    search_fields = ['title', 'description']
    list_editable = ['order']


@admin.register(FocusAreaPartner)
class FocusAreaPartnerAdmin(admin.ModelAdmin):
    list_display = ['focus_area', 'name', 'type', 'order']
    list_filter = ['focus_area', 'type']
    search_fields = ['name', 'role']
    list_editable = ['order']


@admin.register(FocusAreaMilestone)
class FocusAreaMilestoneAdmin(admin.ModelAdmin):
    list_display = ['focus_area', 'year', 'event', 'order']
    list_filter = ['focus_area', 'year']
    search_fields = ['event']
    list_editable = ['order']
