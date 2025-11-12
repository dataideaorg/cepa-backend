from django.contrib import admin
from .models import Cohort, Fellow, CohortProject, CohortEvent, CohortGalleryImage


class FellowInline(admin.TabularInline):
    model = Fellow
    extra = 1
    fields = ['name', 'position', 'profile_image']
    show_change_link = True


class CohortProjectInline(admin.TabularInline):
    model = CohortProject
    extra = 1
    fields = ['title', 'description', 'project_url']
    show_change_link = True


class CohortEventInline(admin.TabularInline):
    model = CohortEvent
    extra = 1
    fields = ['title', 'event_date', 'location']
    show_change_link = True


class CohortGalleryImageInline(admin.TabularInline):
    model = CohortGalleryImage
    extra = 1
    fields = ['image', 'caption']
    show_change_link = True


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'is_active', 'created_at']
    list_filter = ['year', 'is_active']
    search_fields = ['name', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [FellowInline, CohortProjectInline, CohortEventInline, CohortGalleryImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'year', 'image', 'slug', 'is_active', 'overview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fellow)
class FellowAdmin(admin.ModelAdmin):
    list_display = ['name', 'cohort', 'position', 'created_at']
    list_filter = ['cohort']
    search_fields = ['name', 'bio', 'position']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('cohort', 'name', 'position', 'profile_image')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CohortProject)
class CohortProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'cohort', 'created_at']
    list_filter = ['cohort']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('cohort', 'title', 'image')
        }),
        ('Details', {
            'fields': ('description', 'project_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CohortEvent)
class CohortEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'cohort', 'event_date', 'location']
    list_filter = ['cohort', 'event_date']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'event_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('cohort', 'title', 'event_date', 'location')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CohortGalleryImage)
class CohortGalleryImageAdmin(admin.ModelAdmin):
    list_display = ['cohort', 'caption', 'created_at']
    list_filter = ['cohort']
    search_fields = ['caption']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('cohort', 'image', 'caption')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
