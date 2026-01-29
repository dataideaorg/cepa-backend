from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import URLValidator
from ckeditor.fields import RichTextField
import uuid
import os


def generate_uuid():
    """Generate a unique UUID string for model primary keys"""
    return str(uuid.uuid4())


def upload_to_blog_images(instance, filename):
    """Generate upload path for blog post images"""
    return os.path.join('blog', 'images', filename)


def upload_to_event_images(instance, filename):
    """Generate upload path for event images"""
    return os.path.join('events', 'images', filename)


def upload_to_news_images(instance, filename):
    """Generate upload path for news article images"""
    return os.path.join('news', 'images', filename)


def upload_to_publication_pdfs(instance, filename):
    """Generate upload path for publication PDFs"""
    return os.path.join('publications', 'pdfs', filename)


def upload_to_publication_images(instance, filename):
    """Generate upload path for publication images"""
    return os.path.join('publications', 'images', filename)

class BlogPost(models.Model):
    """Model for blog posts and analysis articles"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.TextField()
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_blog_images, blank=True, null=True)
    slug = models.CharField(max_length=500, unique=True, blank=True)
    featured = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
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
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.TextField()
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_news_images, blank=True, null=True)
    slug = models.CharField(max_length=500, unique=True, blank=True)
    featured = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    """Model for comments on blog posts"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"


class NewsComment(models.Model):
    """Model for comments on news articles"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Comment'
        verbose_name_plural = 'News Comments'

    def __str__(self):
        return f"Comment by {self.author_name} on {self.article.title}"


class Publication(models.Model):
    """Model for research publications, policy briefs, and reports"""
    PUBLICATION_TYPES = [
        ('Policy Brief', 'Policy Brief'),
        ('Policy Paper', 'Policy Paper'),
        ('Research Report', 'Research Report'),
        ('Analysis', 'Analysis'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.TextField()
    type = models.CharField(max_length=100, choices=PUBLICATION_TYPES)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    category = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    pdf = models.FileField(upload_to=upload_to_publication_pdfs, blank=True, null=True)
    image = models.ImageField(upload_to=upload_to_publication_images, blank=True, null=True)
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

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_event_images, blank=True, null=True)
    slug = models.CharField(
        max_length=500,
        unique=True,
        blank=True,
        help_text="Leave blank to auto-generate from title (normal text).",
    )
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='upcoming')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def _get_unique_slug(self, base_slug):
        """Generate a unique slug; append number if base_slug is taken."""
        slug = base_slug[:500]
        queryset = Event.objects.filter(slug=slug).exclude(pk=self.pk)
        if not queryset.exists():
            return slug
        for i in range(1, 10000):
            candidate = f"{base_slug[:495]}-{i}" if len(base_slug) > 495 else f"{base_slug}-{i}"
            if not Event.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                return candidate
        return f"{base_slug[:490]}-{uuid.uuid4().hex[:8]}"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = f"event-{self.id or uuid.uuid4().hex[:8]}"
            self.slug = self._get_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
