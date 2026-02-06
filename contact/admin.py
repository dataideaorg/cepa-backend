from django.contrib import admin
from .models import Contact, Newsletter, Feedback


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'created_at')
    list_filter = ('inquiry_type', 'created_at')
    search_fields = ('name', 'email', 'subject', 'organization')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    ordering = ('-created_at',)


# customize admin panel 
admin.site.site_header = "CEPA Admin Panel"
admin.site.site_title = "CEPA Admin Panel"
admin.site.index_title = "Welcome to CEPA Admin Panel"

