
from django.db import models
from django.utils import timezone
import uuid


def generate_uuid():
    """Generate a unique UUID string for model primary keys"""
    return str(uuid.uuid4())


class Cohort(models.Model):
    """Model for fellowship cohorts"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=200, help_text='e.g., 2025 Cohort')
    year = models.IntegerField()
    image = models.ImageField(upload_to='cohorts/', blank=True, null=True)
    overview = models.TextField(help_text='Overview description of this cohort')
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year']
        verbose_name = 'Cohort'
        verbose_name_plural = 'Cohorts'

    def __str__(self):
        return self.name


class Fellow(models.Model):
    """Model for fellowship cohort members"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='fellows')
    name = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='cohorts/fellows/', blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True, help_text='e.g., Research Fellow')
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Fellow'
        verbose_name_plural = 'Fellows'

    def __str__(self):
        return f"{self.name} - {self.cohort.name}"


class CohortProject(models.Model):
    """Model for cohort projects"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='cohorts/projects/', blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cohort Project'
        verbose_name_plural = 'Cohort Projects'

    def __str__(self):
        return f"{self.title} - {self.cohort.name}"


class CohortEvent(models.Model):
    """Model for cohort events"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Cohort Event'
        verbose_name_plural = 'Cohort Events'

    def __str__(self):
        return f"{self.title} - {self.cohort.name}"


class CohortGalleryImage(models.Model):
    """Model for cohort gallery images"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='cohorts/gallery/')
    caption = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"Gallery Image - {self.cohort.name}"
