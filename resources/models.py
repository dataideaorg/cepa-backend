from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator


class BlogPost(models.Model):
    """Model for blog posts and analysis articles"""
    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField()
    date = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True)
    featured = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    """Model for news articles and updates"""
    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField()
    date = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True)
    featured = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title


class Publication(models.Model):
    """Model for research publications, policy briefs, and reports"""
    PUBLICATION_TYPES = [
        ('Policy Brief', 'Policy Brief'),
        ('Policy Paper', 'Policy Paper'),
        ('Research Report', 'Research Report'),
        ('Analysis', 'Analysis'),
    ]

    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField()
    type = models.CharField(max_length=100, choices=PUBLICATION_TYPES)
    date = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    pdf = models.CharField(max_length=500, blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return self.title


class Event(models.Model):
    """Model for events, conferences, workshops, and meetings"""
    EVENT_STATUS = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='upcoming')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title
