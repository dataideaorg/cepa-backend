from django.contrib import admin
from .models import BlogPost, NewsArticle, Publication, Event


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'created_at']
    list_filter = ['category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'content']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'created_at']
    list_filter = ['category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'content']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'category', 'date', 'featured', 'created_at']
    list_filter = ['type', 'category', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'time', 'location', 'status', 'featured', 'created_at']
    list_filter = ['category', 'status', 'featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['featured', 'status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
