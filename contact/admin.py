from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'subject', 'priority', 'status', 
        'is_spam', 'created_at', 'response_time_display'
    ]
    list_filter = [
        'status', 'priority', 'subject', 'is_spam', 
        'created_at', 'responded_at'
    ]
    search_fields = [
        'name', 'email', 'organization', 'message', 
        'subject', 'admin_notes'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'responded_at', 
        'ip_address', 'user_agent', 'response_time_display'
    ]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'organization')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'priority')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_spam', 'admin_notes')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at', 'responded_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_responded', 'mark_as_closed', 'mark_as_spam', 'mark_as_not_spam']
    
    def response_time_display(self, obj):
        """Display response time in a readable format"""
        if obj.response_time:
            hours = obj.response_time
            if hours < 1:
                return f"{int(hours * 60)} minutes"
            elif hours < 24:
                return f"{hours:.1f} hours"
            else:
                days = hours / 24
                return f"{days:.1f} days"
        return "Not responded"
    response_time_display.short_description = "Response Time"
    
    def mark_as_responded(self, request, queryset):
        """Mark selected submissions as responded"""
        count = 0
        for submission in queryset:
            if submission.status != 'responded':
                submission.mark_as_responded()
                count += 1
        self.message_user(request, f"{count} submissions marked as responded.")
    mark_as_responded.short_description = "Mark as responded"
    
    def mark_as_closed(self, request, queryset):
        """Mark selected submissions as closed"""
        count = queryset.update(status='closed')
        self.message_user(request, f"{count} submissions marked as closed.")
    mark_as_closed.short_description = "Mark as closed"
    
    def mark_as_spam(self, request, queryset):
        """Mark selected submissions as spam"""
        count = queryset.update(is_spam=True)
        self.message_user(request, f"{count} submissions marked as spam.")
    mark_as_spam.short_description = "Mark as spam"
    
    def mark_as_not_spam(self, request, queryset):
        """Mark selected submissions as not spam"""
        count = queryset.update(is_spam=False)
        self.message_user(request, f"{count} submissions marked as not spam.")
    mark_as_not_spam.short_description = "Mark as not spam"
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related()
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete submissions"""
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields read-only for non-superusers"""
        if not request.user.is_superuser:
            return self.readonly_fields + ['is_spam']
        return self.readonly_fields