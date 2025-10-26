from django.contrib import admin
from .models import Podcast, Video, GalleryGroup, GalleryImage


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'guest', 'duration', 'featured', 'date']
    list_filter = ['category', 'featured', 'date']
    search_fields = ['title', 'description', 'guest']
    list_editable = ['featured']
    ordering = ['-date', '-created_at']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'featured', 'date']
    list_filter = ['category', 'featured', 'date']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    ordering = ['-date', '-created_at']


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['title', 'alt_text', 'image', 'caption', 'order']
    show_change_link = True


@admin.register(GalleryGroup)
class GalleryGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_count', 'featured', 'date']
    list_filter = ['featured', 'date']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    inlines = [GalleryImageInline]
    ordering = ['-date', '-created_at']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'order', 'created_at']
    list_filter = ['group', 'created_at']
    search_fields = ['title', 'alt_text', 'caption']
    list_editable = ['order']
    ordering = ['group', 'order', '-created_at']