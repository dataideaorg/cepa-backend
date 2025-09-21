from django.db import models
from django.utils import timezone
import uuid


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def upload_to_podcast_thumbnails(instance, filename):
    """Upload path for podcast thumbnails"""
    return f'podcasts/thumbnails/{instance.id}/{filename}'


def upload_to_video_thumbnails(instance, filename):
    """Upload path for video thumbnails"""
    return f'videos/thumbnails/{instance.id}/{filename}'


def upload_to_gallery_images(instance, filename):
    """Upload path for gallery images"""
    return f'gallery/images/{instance.id}/{filename}'


class Podcast(models.Model):
    """Model for podcasts with YouTube integration"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField()
    youtube_id = models.CharField(max_length=100, help_text="YouTube video ID for embedding")
    youtube_url = models.URLField(blank=True, null=True, help_text="Full YouTube URL")
    thumbnail = models.ImageField(upload_to=upload_to_podcast_thumbnails, blank=True, null=True)
    duration = models.CharField(max_length=20, help_text="Duration in MM:SS format")
    category = models.CharField(max_length=100)
    guest = models.CharField(max_length=200, blank=True, null=True, help_text="Guest speaker or host")
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Generate YouTube embed URL"""
        return f"https://www.youtube.com/embed/{self.youtube_id}?autoplay=1&rel=0"


class Video(models.Model):
    """Model for videos with YouTube integration"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField()
    youtube_id = models.CharField(max_length=100, help_text="YouTube video ID for embedding")
    youtube_url = models.URLField(blank=True, null=True, help_text="Full YouTube URL")
    thumbnail = models.ImageField(upload_to=upload_to_video_thumbnails, blank=True, null=True)
    duration = models.CharField(max_length=20, help_text="Duration in MM:SS format")
    category = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Generate YouTube embed URL"""
        return f"https://www.youtube.com/embed/{self.youtube_id}?autoplay=1&rel=0"


class GalleryGroup(models.Model):
    """Model for organizing gallery images into groups/albums"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Gallery Group'
        verbose_name_plural = 'Gallery Groups'

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Model for individual gallery images"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    group = models.ForeignKey(GalleryGroup, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    alt_text = models.CharField(max_length=200, help_text="Alt text for accessibility")
    image = models.ImageField(upload_to=upload_to_gallery_images)
    caption = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order within the group")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group', 'order', '-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"{self.group.title} - {self.title}"