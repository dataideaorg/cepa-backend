from django.contrib import admin
from .widgets import QuillEditorWidget
from .models import BlogPost, NewsArticle, Publication, Event


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'created_at']
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
            'fields': ('slug',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Apply Quill editor only to the content field
        form.base_fields['content'].widget = QuillEditorWidget()
        return form


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'featured', 'created_at']
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
            'fields': ('slug',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Apply Quill editor only to the content field
        form.base_fields['content'].widget = QuillEditorWidget()
        return form


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
