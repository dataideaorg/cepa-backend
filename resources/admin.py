from django.contrib import admin
from .models import BlogPost, NewsArticle, Publication, Event, BlogComment, NewsComment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'views_count', 'created_at']
    list_filter = ['category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'content']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'date', 'category', 'featured')
        }),
        ('Content', {
            'fields': ('description', 'content', 'image'),
            'classes': ('wide',)
        }),
        ('Advanced', {
            'fields': ('slug', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author_name', 'body']
    readonly_fields = ['created_at']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'views_count', 'created_at']
    list_filter = ['category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'content']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'date', 'category', 'featured')
        }),
        ('Content', {
            'fields': ('description', 'content', 'image'),
            'classes': ('wide',)
        }),
        ('Advanced', {
            'fields': ('slug', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author_name', 'body']
    readonly_fields = ['created_at']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'category', 'date', 'featured', 'created_at']
    list_filter = ['type', 'category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'type', 'category', 'date', 'featured')
        }),
        ('Content', {
            'fields': ('description', 'url', 'pdf', 'image'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'time', 'location', 'status', 'featured', 'created_at']
    list_filter = ['category', 'status', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['featured', 'status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
