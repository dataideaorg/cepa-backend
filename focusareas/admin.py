from django.contrib import admin
from .models import (
    FocusArea, FocusAreaObjective, FocusAreaActivity,
    FocusAreaOutcome, FocusAreaPartner, FocusAreaMilestone, FocusAreaBasicInformation
)


class FocusAreaBasicInformationInline(admin.StackedInline):
    model = FocusAreaBasicInformation
    extra = 0
    fields = ['description', 'image', 'overview_summary', 'order',]
    # readonly_fields = ('created', 'modified')
    show_change_link = True


class FocusAreaObjectiveInline(admin.TabularInline):
    model = FocusAreaObjective
    extra = 0
    fields = ['text', 'order']
    can_delete = True
    show_change_link = True


class FocusAreaActivityInline(admin.TabularInline):
    model = FocusAreaActivity
    extra = 0
    fields = ['text', 'order']
    can_delete = True
    show_change_link = True


class FocusAreaOutcomeInline(admin.TabularInline):
    model = FocusAreaOutcome
    extra = 0
    fields = ['title', 'description', 'metric', 'order']
    can_delete = True
    show_change_link = True


class FocusAreaPartnerInline(admin.TabularInline):
    model = FocusAreaPartner
    extra = 0
    fields = ['name', 'type', 'role', 'order']
    can_delete = True
    show_change_link = True


class FocusAreaMilestoneInline(admin.TabularInline):
    model = FocusAreaMilestone
    extra = 0
    fields = ['year', 'event', 'order']
    can_delete = True
    show_change_link = True


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']
    list_editable = ['order']
    readonly_fields = ['created_at']
    prepopulated_fields = {'slug': ('title',)}
    show_change_link = True

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        FocusAreaBasicInformationInline,
        FocusAreaObjectiveInline,
        FocusAreaActivityInline,
        FocusAreaOutcomeInline,
        FocusAreaPartnerInline,
        FocusAreaMilestoneInline,
    ]

@admin.register(FocusAreaBasicInformation)
class FocusAreaBasicInformationAdmin(admin.ModelAdmin):
    list_display = ['focus_area']
    list_filter = ['focus_area']
    search_fields = ['focus_area__title']

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
