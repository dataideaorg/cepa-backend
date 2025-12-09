from django.db import models
from django.utils import timezone
import uuid
import os


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def upload_to_hero_slides(instance, filename):
    """Generate upload path for hero slide images"""
    return os.path.join('home', 'hero_slides', filename)


class HeroSlide(models.Model):
    """Model for homepage hero slider images"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    image = models.ImageField(upload_to=upload_to_hero_slides, help_text="Hero slide image")
    title = models.CharField(max_length=255, help_text="Slide title/alt text")
    is_active = models.BooleanField(default=True, help_text="Display this slide in the slider")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title
