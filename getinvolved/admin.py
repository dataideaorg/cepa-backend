from django.contrib import admin
from .models import CareerOpportunity, Announcement


@admin.register(CareerOpportunity)
class CareerOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'location', 'status', 'deadline', 'featured', 'posted_date']
    list_filter = ['type', 'status', 'featured', 'location', 'posted_date', 'deadline']
    search_fields = ['title', 'description', 'requirements', 'responsibilities']
    list_editable = ['featured', 'status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'posted_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'type', 'location', 'department', 'status', 'featured')
        }),
        ('Dates', {
            'fields': ('posted_date', 'deadline')
        }),
        ('Details', {
            'fields': ('description', 'responsibilities', 'requirements', 'how_to_apply')
        }),
        ('Media & SEO', {
            'fields': ('image', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'priority', 'is_active', 'published_date', 'expiry_date', 'featured']
    list_filter = ['type', 'priority', 'is_active', 'featured', 'published_date', 'expiry_date']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['featured', 'is_active', 'priority']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'type', 'priority', 'is_active', 'featured')
        }),
        ('Dates', {
            'fields': ('published_date', 'expiry_date')
        }),
        ('Content', {
            'fields': ('summary', 'content')
        }),
        ('Media & Links', {
            'fields': ('image', 'slug', 'external_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
