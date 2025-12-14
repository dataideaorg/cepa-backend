from django.contrib import admin
from .models import Document, ChatSession, ChatMessage


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin interface for Document model"""
    list_display = ['name', 'file_type', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['id', 'file_type', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Document Information', {
            'fields': ('name', 'file', 'description', 'is_active')
        }),
        ('Metadata', {
            'fields': ('id', 'file_type', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ChatMessageInline(admin.TabularInline):
    """Inline admin for displaying messages within a chat session"""
    model = ChatMessage
    extra = 0
    readonly_fields = ['id', 'message_type', 'content', 'source_document_name',
                      'source_document_url', 'source_document_type', 'confidence', 'created_at']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Admin interface for ChatSession model"""
    list_display = ['session_title', 'started_at', 'last_activity',
                   'is_active', 'message_count']
    list_filter = ['is_active', 'started_at', 'last_activity']
    search_fields = ['session_title', 'id']
    list_editable = ['is_active']
    readonly_fields = ['id', 'started_at', 'created_at', 'updated_at', 'message_count']
    ordering = ['-last_activity']
    inlines = [ChatMessageInline]

    fieldsets = (
        ('Session Information', {
            'fields': ('session_title', 'is_active')
        }),
        ('Activity', {
            'fields': ('started_at', 'last_activity', 'message_count')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def message_count(self, obj):
        """Display the number of messages in the session"""
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin interface for ChatMessage model"""
    list_display = ['session', 'message_type', 'content_preview',
                   'source_document_name', 'created_at']
    list_filter = ['message_type', 'source_document_type', 'created_at']
    search_fields = ['content', 'source_document_name', 'session__session_title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Message Information', {
            'fields': ('session', 'message_type', 'content')
        }),
        ('AI Response Metadata', {
            'fields': ('source_document_name', 'source_document_url',
                      'source_document_type', 'confidence'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        """Display a preview of the message content"""
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
